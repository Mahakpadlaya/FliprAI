# Minimal Flask app for Vercel - Test if basic setup works
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Simple test route that always works
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'OK', 'message': 'Flask is working!'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'Server is running'})

# MongoDB and other routes will be added after we confirm Flask works
# For now, return helpful errors
@app.route('/api/projects', methods=['GET'])
def get_projects():
    mongodb_uri = os.getenv('MONGODB_URI', '')
    if not mongodb_uri:
        return jsonify({
            'error': 'MongoDB not configured',
            'message': 'Please set MONGODB_URI environment variable in Vercel'
        }), 500
    return jsonify({
        'error': 'MongoDB connection not implemented yet',
        'message': 'Basic Flask is working. MongoDB integration coming next.'
    }), 500

@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify({
        'error': 'Not implemented',
        'message': 'Basic Flask is working. MongoDB integration coming next.'
    }), 500

# Catch-all for any other routes
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    return jsonify({
        'error': 'Route not found',
        'path': path,
        'message': 'Basic Flask is working, but this route needs implementation'
    }), 404

# Error handlers
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({
        'error': str(e),
        'type': type(e).__name__
    }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

# Export for Vercel
handler = app
