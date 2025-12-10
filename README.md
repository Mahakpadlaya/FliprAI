# Full Stack Application - HTML/CSS/JavaScript + Python

A complete full-stack application built with vanilla HTML, CSS, JavaScript for the frontend and Python Flask for the backend.

## Features

### Landing Page
- **Our Projects Section**: Displays all projects with images, names, and descriptions
- **Happy Clients Section**: Shows client testimonials with images, names, and designations
- **Contact Form**: Submit contact information (Full Name, Email, Mobile Number, City)
- **Newsletter Subscription**: Subscribe to newsletter with email address

### Admin Panel
- **Project Management**: Add, edit, and delete projects with images
- **Client Management**: Manage client information with images
- **Contact Form Details**: View all contact form submissions
- **Newsletter Subscribers**: View all subscribed email addresses

### Additional Features
- **Image Cropping**: Images automatically cropped to 450x350 ratio (for projects) and 150x150 (for clients)
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Tech Stack

### Backend
- Python 3.8+
- Flask (Web framework)
- Flask-CORS (Cross-origin resource sharing)
- PyMongo (MongoDB driver)
- Pillow (Image processing)
- MongoDB (Database)

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript (ES6 Modules)
- Fetch API for HTTP requests

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account (free tier) or local MongoDB installation
- pip (Python package manager)

## Setup Instructions

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
PORT=5000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=fullstack-task
NODE_ENV=development
```

Replace the `MONGODB_URI` with your MongoDB Atlas connection string.

### 2. Frontend Setup

The frontend files are static HTML/CSS/JS files. You can:
- Open them directly in a browser (with CORS limitations)
- Use a simple HTTP server (recommended)

**Option 1: Using Python HTTP Server**
```bash
cd frontend
python -m http.server 3000
```

**Option 2: Using Node.js http-server**
```bash
cd frontend
npx http-server -p 3000
```

**Option 3: Using VS Code Live Server Extension**
- Install "Live Server" extension in VS Code
- Right-click on `index.html` and select "Open with Live Server"

### 3. Running the Application

#### Start Backend Server
```bash
cd backend
python app.py
```

The backend server will run on `http://localhost:5000`

#### Start Frontend Server
Use one of the methods mentioned above. The frontend will run on `http://localhost:3000`

### 4. Access the Application

- **Landing Page**: http://localhost:3000/index.html (or http://localhost:3000/)
- **Admin Panel**: http://localhost:3000/admin.html

## Project Structure

```
javascriptandbackend/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/              # Uploaded images (created automatically)
│   └── .env                  # Environment variables (create this)
├── frontend/
│   ├── index.html            # Landing page
│   ├── admin.html            # Admin panel
│   ├── styles.css            # Landing page styles
│   ├── admin.css             # Admin panel styles
│   ├── api.js                # API functions
│   ├── app.js                # Landing page JavaScript
│   └── admin.js              # Admin panel JavaScript
└── README.md                 # This file
```

## API Endpoints

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/:id` - Get single project
- `POST /api/projects` - Create project (Admin)
- `PUT /api/projects/:id` - Update project (Admin)
- `DELETE /api/projects/:id` - Delete project (Admin)

### Clients
- `GET /api/clients` - Get all clients
- `GET /api/clients/:id` - Get single client
- `POST /api/clients` - Create client (Admin)
- `PUT /api/clients/:id` - Update client (Admin)
- `DELETE /api/clients/:id` - Delete client (Admin)

### Contacts
- `POST /api/contacts` - Submit contact form
- `GET /api/contacts` - Get all contacts (Admin)
- `DELETE /api/contacts/:id` - Delete contact (Admin)

### Newsletter
- `POST /api/newsletters` - Subscribe to newsletter
- `GET /api/newsletters` - Get all subscribers (Admin)
- `DELETE /api/newsletters/:id` - Delete subscriber (Admin)

## MongoDB Setup

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (free tier M0)
3. Create a database user
4. Whitelist your IP address (0.0.0.0/0 for development)
5. Get your connection string
6. Update the `MONGODB_URI` in your `.env` file

## Troubleshooting

### CORS Issues
- Make sure Flask-CORS is installed and enabled in `app.py`
- Check that backend is running on port 5000
- Verify frontend is making requests to the correct API URL

### Image Upload Issues
- Ensure the `uploads` directory exists in the backend folder
- Check file size limits (5MB max)
- Verify image file formats (png, jpg, jpeg, gif, webp)

### MongoDB Connection Issues
- Verify your MongoDB Atlas cluster is running
- Check that your IP address is whitelisted
- Verify your connection string is correct in `.env`

### Module Import Errors
- Make sure you're using a web server (not opening HTML files directly)
- Check browser console for CORS or module errors
- Verify all JavaScript files are in the same directory

## Development Tips

1. **Backend Development**: Use `python app.py` - Flask runs in debug mode by default
2. **Frontend Development**: Use a local server (not file://) to avoid CORS issues
3. **Database**: MongoDB collections are created automatically on first insert
4. **Images**: Uploaded images are automatically cropped and stored in `backend/uploads/`

## License

This project is created for educational purposes.

