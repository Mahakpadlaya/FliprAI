from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'fullstack-task')

try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    projects_collection = db['projects']
    clients_collection = db['clients']
    contacts_collection = db['contacts']
    newsletters_collection = db['newsletters']
except Exception as e:
    print(f"MongoDB connection error: {e}")

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

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Server is running'})

# Projects routes
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
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        name = data.get('name')
        description = data.get('description')
        image_data = data.get('image')
        
        if not all([name, description, image_data]):
            return jsonify({'error': 'Name, description, and image are required'}), 400
        
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((450, 350), Image.Resampling.LANCZOS)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        project = {
            'name': name,
            'description': description,
            'image': f'data:image/png;base64,{img_str}',
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
        
        data = request.json
        update_data = {}
        
        if data.get('name'):
            update_data['name'] = data['name']
        if data.get('description'):
            update_data['description'] = data['description']
        if data.get('image'):
            image_data = data['image']
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            img = Image.open(io.BytesIO(image_bytes))
            img = img.resize((450, 350), Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            update_data['image'] = f'data:image/png;base64,{img_str}'
        
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

# Clients routes
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
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        name = data.get('name')
        description = data.get('description')
        designation = data.get('designation')
        image_data = data.get('image')
        
        if not all([name, description, designation, image_data]):
            return jsonify({'error': 'All fields are required'}), 400
        
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        client = {
            'name': name,
            'description': description,
            'designation': designation,
            'image': f'data:image/png;base64,{img_str}',
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
        
        data = request.json
        update_data = {}
        
        if data.get('name'):
            update_data['name'] = data['name']
        if data.get('description'):
            update_data['description'] = data['description']
        if data.get('designation'):
            update_data['designation'] = data['designation']
        if data.get('image'):
            image_data = data['image']
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            img = Image.open(io.BytesIO(image_bytes))
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            update_data['image'] = f'data:image/png;base64,{img_str}'
        
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

# Contacts routes
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

# Newsletter routes
@app.route('/api/newsletters', methods=['POST'])
def subscribe_newsletter():
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
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

# Export app for Vercel - this is what Vercel Python runtime expects
# Vercel automatically wraps Flask apps
handler = app
