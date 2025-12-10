from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://senrishabhdevpy_db_user:fYZnlmqpQWqUbK3o@flipkr.spwmyya.mongodb.net/?appName=Flipkr')
DB_NAME = os.getenv('DB_NAME', 'fullstack-task')
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Collections
projects_collection = db['projects']
clients_collection = db['clients']
contacts_collection = db['contacts']
newsletters_collection = db['newsletters']

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crop_image(input_path, output_path, width=450, height=350):
    """Crop image to specific dimensions"""
    try:
        img = Image.open(input_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img.save(output_path)
        # Remove original file
        if os.path.exists(input_path):
            os.remove(input_path)
        return True
    except Exception as e:
        print(f"Error cropping image: {e}")
        return False

# Helper function to convert MongoDB documents to JSON
def jsonify_mongo(data):
    if isinstance(data, list):
        return [jsonify_mongo(item) for item in data]
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = jsonify_mongo(value)
        return result
    return data

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Server is running'})

# ==================== PROJECTS ROUTES ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        projects = list(projects_collection.find().sort('createdAt', -1))
        return jsonify(jsonify_mongo(projects))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = projects_collection.find_one({'_id': ObjectId(project_id)})
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(jsonify_mongo(project))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Image is required'}), 400
        
        file = request.files['image']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid image file'}), 400
        
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name or not description:
            return jsonify({'error': 'Name and description are required'}), 400
        
        # Save original file
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp-{datetime.now().timestamp()}.{file_ext}')
        file.save(original_path)
        
        # Crop image
        cropped_filename = f'cropped-{datetime.now().timestamp()}.{file_ext}'
        cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename)
        crop_image(original_path, cropped_path)
        
        project = {
            'name': name,
            'description': description,
            'image': f'/uploads/{cropped_filename}',
            'createdAt': datetime.now()
        }
        
        result = projects_collection.insert_one(project)
        project['_id'] = str(result.inserted_id)
        return jsonify(jsonify_mongo(project)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        project = projects_collection.find_one({'_id': ObjectId(project_id)})
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        name = request.form.get('name')
        description = request.form.get('description')
        
        update_data = {}
        if name:
            update_data['name'] = name
        if description:
            update_data['description'] = description
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp-{datetime.now().timestamp()}.{file_ext}')
                file.save(original_path)
                
                cropped_filename = f'cropped-{datetime.now().timestamp()}.{file_ext}'
                cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename)
                crop_image(original_path, cropped_path)
                update_data['image'] = f'/uploads/{cropped_filename}'
        
        projects_collection.update_one({'_id': ObjectId(project_id)}, {'$set': update_data})
        updated_project = projects_collection.find_one({'_id': ObjectId(project_id)})
        return jsonify(jsonify_mongo(updated_project))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        result = projects_collection.delete_one({'_id': ObjectId(project_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify({'message': 'Project deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CLIENTS ROUTES ====================

@app.route('/api/clients', methods=['GET'])
def get_clients():
    try:
        clients = list(clients_collection.find().sort('createdAt', -1))
        return jsonify(jsonify_mongo(clients))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    try:
        client = clients_collection.find_one({'_id': ObjectId(client_id)})
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        return jsonify(jsonify_mongo(client))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients', methods=['POST'])
def create_client():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Image is required'}), 400
        
        file = request.files['image']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid image file'}), 400
        
        name = request.form.get('name')
        description = request.form.get('description')
        designation = request.form.get('designation')
        
        if not name or not description or not designation:
            return jsonify({'error': 'Name, description, and designation are required'}), 400
        
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp-{datetime.now().timestamp()}.{file_ext}')
        file.save(original_path)
        
        cropped_filename = f'cropped-{datetime.now().timestamp()}.{file_ext}'
        cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename)
        crop_image(original_path, cropped_path)
        
        client = {
            'name': name,
            'description': description,
            'designation': designation,
            'image': f'/uploads/{cropped_filename}',
            'createdAt': datetime.now()
        }
        
        result = clients_collection.insert_one(client)
        client['_id'] = str(result.inserted_id)
        return jsonify(jsonify_mongo(client)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/clients/<client_id>', methods=['PUT'])
def update_client(client_id):
    try:
        client = clients_collection.find_one({'_id': ObjectId(client_id)})
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        update_data = {}
        if request.form.get('name'):
            update_data['name'] = request.form.get('name')
        if request.form.get('description'):
            update_data['description'] = request.form.get('description')
        if request.form.get('designation'):
            update_data['designation'] = request.form.get('designation')
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp-{datetime.now().timestamp()}.{file_ext}')
                file.save(original_path)
                
                cropped_filename = f'cropped-{datetime.now().timestamp()}.{file_ext}'
                cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_filename)
                crop_image(original_path, cropped_path)
                update_data['image'] = f'/uploads/{cropped_filename}'
        
        clients_collection.update_one({'_id': ObjectId(client_id)}, {'$set': update_data})
        updated_client = clients_collection.find_one({'_id': ObjectId(client_id)})
        return jsonify(jsonify_mongo(updated_client))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/clients/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        result = clients_collection.delete_one({'_id': ObjectId(client_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Client not found'}), 404
        return jsonify({'message': 'Client deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CONTACTS ROUTES ====================

@app.route('/api/contacts', methods=['POST'])
def create_contact():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        city = data.get('city')
        
        if not all([name, email, mobile, city]):
            return jsonify({'error': 'All fields are required'}), 400
        
        contact = {
            'name': name,
            'email': email,
            'mobile': mobile,
            'city': city,
            'createdAt': datetime.now()
        }
        
        result = contacts_collection.insert_one(contact)
        contact['_id'] = str(result.inserted_id)
        return jsonify(jsonify_mongo(contact)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    try:
        contacts = list(contacts_collection.find().sort('createdAt', -1))
        return jsonify(jsonify_mongo(contacts))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        result = contacts_collection.delete_one({'_id': ObjectId(contact_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Contact not found'}), 404
        return jsonify({'message': 'Contact deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== NEWSLETTER ROUTES ====================

@app.route('/api/newsletters', methods=['POST'])
def subscribe_newsletter():
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if email already exists
        existing = newsletters_collection.find_one({'email': email})
        if existing:
            return jsonify({'error': 'Email already subscribed'}), 400
        
        newsletter = {
            'email': email,
            'createdAt': datetime.now()
        }
        
        result = newsletters_collection.insert_one(newsletter)
        newsletter['_id'] = str(result.inserted_id)
        return jsonify(jsonify_mongo(newsletter)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/newsletters', methods=['GET'])
def get_newsletters():
    try:
        newsletters = list(newsletters_collection.find().sort('createdAt', -1))
        return jsonify(jsonify_mongo(newsletters))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/newsletters/<newsletter_id>', methods=['DELETE'])
def delete_newsletter(newsletter_id):
    try:
        result = newsletters_collection.delete_one({'_id': ObjectId(newsletter_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Subscriber not found'}), 404
        return jsonify({'message': 'Subscriber deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

