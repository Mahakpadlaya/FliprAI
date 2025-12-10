# Flask app for Vercel
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'OK', 'message': 'Flask is working!'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'Server is running'})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    mongodb_uri = os.getenv('MONGODB_URI', '')
    if not mongodb_uri:
        return jsonify({
            'error': 'MongoDB not configured',
            'message': 'Please set MONGODB_URI environment variable in Vercel'
        }), 500
    return jsonify({
        'error': 'MongoDB connection not implemented yet'
    }), 500

@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify({
        'error': 'Not implemented yet'
    }), 500

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({'error': str(e), 'type': type(e).__name__}), 500

# Vercel automatically wraps Flask apps - just export the app
# DO NOT export a handler function - Vercel detects Flask automatically
# The file name must be index.py in the api folder
