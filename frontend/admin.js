import { 
    getProjects, createProject, updateProject, deleteProject,
    getClients, createClient, updateClient, deleteClient,
    getContacts, deleteContact,
    getSubscribers, deleteSubscriber
} from './api.js';

// API URL - Works for both local development and Vercel deployment
const API_URL = window.location.origin.includes('vercel.app') || window.location.origin.includes('localhost') === false
    ? ''  // Use relative URL for production (Vercel)
    : 'http://localhost:5000';  // Use localhost for development
let editingProjectId = null;
let editingClientId = null;

// Tab switching
document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    setupProjectForm();
    setupClientForm();
    loadProjects();
    loadClients();
    loadContacts();
    loadNewsletters();
});

function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Remove active class from all
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked
            button.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            // Load data when switching tabs
            if (tabId === 'projects') loadProjects();
            if (tabId === 'clients') loadClients();
            if (tabId === 'contacts') loadContacts();
            if (tabId === 'newsletters') loadNewsletters();
        });
    });
}

// Project Management
function setupProjectForm() {
    const form = document.getElementById('project-form');
    const addBtn = document.getElementById('add-project-btn');
    const cancelBtn = document.getElementById('cancel-project-btn');
    
    addBtn.addEventListener('click', () => {
        editingProjectId = null;
        form.style.display = 'block';
        form.reset();
        document.getElementById('project-image').required = true;
    });
    
    cancelBtn.addEventListener('click', () => {
        form.style.display = 'none';
        editingProjectId = null;
        form.reset();
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('name', document.getElementById('project-name').value);
        formData.append('description', document.getElementById('project-description').value);
        
        const imageFile = document.getElementById('project-image').files[0];
        if (imageFile) {
            formData.append('image', imageFile);
        }
        
        try {
            if (editingProjectId) {
                await updateProject(editingProjectId, formData);
                alert('Project updated successfully!');
            } else {
                await createProject(formData);
                alert('Project created successfully!');
            }
            form.style.display = 'none';
            form.reset();
            editingProjectId = null;
            loadProjects();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });
}

async function loadProjects() {
    const container = document.getElementById('projects-list');
    
    try {
        container.innerHTML = '<p class="loading">Loading projects...</p>';
        const projects = await getProjects();
        
        if (projects.length === 0) {
            container.innerHTML = '<p class="no-data">No projects available</p>';
            return;
        }
        
        container.innerHTML = projects.map(project => `
            <div class="item-card">
                <div class="item-image">
                    <img src="${project.image.startsWith('http') ? project.image : API_URL + project.image}" 
                         alt="${project.name}"
                         onerror="this.src='https://via.placeholder.com/450x350?text=Project+Image'">
                </div>
                <div class="item-info">
                    <h3>${project.name}</h3>
                    <p>${project.description}</p>
                    <div class="item-actions">
                        <button class="edit-button" onclick="editProject('${project._id}')">Edit</button>
                        <button class="delete-button" onclick="deleteProjectItem('${project._id}')">Delete</button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

window.editProject = function(id) {
    editingProjectId = id;
    getProjects().then(projects => {
        const project = projects.find(p => p._id === id);
        if (project) {
            document.getElementById('project-name').value = project.name;
            document.getElementById('project-description').value = project.description;
            document.getElementById('project-image').required = false;
            document.getElementById('project-form').style.display = 'block';
        }
    });
};

window.deleteProjectItem = async function(id) {
    if (confirm('Are you sure you want to delete this project?')) {
        try {
            await deleteProject(id);
            alert('Project deleted successfully!');
            loadProjects();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
};

// Client Management
function setupClientForm() {
    const form = document.getElementById('client-form');
    const addBtn = document.getElementById('add-client-btn');
    const cancelBtn = document.getElementById('cancel-client-btn');
    
    addBtn.addEventListener('click', () => {
        editingClientId = null;
        form.style.display = 'block';
        form.reset();
        document.getElementById('client-image').required = true;
    });
    
    cancelBtn.addEventListener('click', () => {
        form.style.display = 'none';
        editingClientId = null;
        form.reset();
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('name', document.getElementById('client-name').value);
        formData.append('description', document.getElementById('client-description').value);
        formData.append('designation', document.getElementById('client-designation').value);
        
        const imageFile = document.getElementById('client-image').files[0];
        if (imageFile) {
            formData.append('image', imageFile);
        }
        
        try {
            if (editingClientId) {
                await updateClient(editingClientId, formData);
                alert('Client updated successfully!');
            } else {
                await createClient(formData);
                alert('Client created successfully!');
            }
            form.style.display = 'none';
            form.reset();
            editingClientId = null;
            loadClients();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });
}

async function loadClients() {
    const container = document.getElementById('clients-list');
    
    try {
        container.innerHTML = '<p class="loading">Loading clients...</p>';
        const clients = await getClients();
        
        if (clients.length === 0) {
            container.innerHTML = '<p class="no-data">No clients available</p>';
            return;
        }
        
        container.innerHTML = clients.map(client => `
            <div class="item-card">
                <div class="item-image client-image-circle">
                    <img src="${client.image.startsWith('http') ? client.image : API_URL + client.image}" 
                         alt="${client.name}"
                         onerror="this.src='https://via.placeholder.com/150?text=Client'">
                </div>
                <div class="item-info">
                    <h3>${client.name}</h3>
                    <p class="designation">${client.designation}</p>
                    <p>${client.description}</p>
                    <div class="item-actions">
                        <button class="edit-button" onclick="editClient('${client._id}')">Edit</button>
                        <button class="delete-button" onclick="deleteClientItem('${client._id}')">Delete</button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

window.editClient = function(id) {
    editingClientId = id;
    getClients().then(clients => {
        const client = clients.find(c => c._id === id);
        if (client) {
            document.getElementById('client-name').value = client.name;
            document.getElementById('client-description').value = client.description;
            document.getElementById('client-designation').value = client.designation;
            document.getElementById('client-image').required = false;
            document.getElementById('client-form').style.display = 'block';
        }
    });
};

window.deleteClientItem = async function(id) {
    if (confirm('Are you sure you want to delete this client?')) {
        try {
            await deleteClient(id);
            alert('Client deleted successfully!');
            loadClients();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
};

// Contacts Management
async function loadContacts() {
    const container = document.getElementById('contacts-list');
    
    try {
        container.innerHTML = '<p class="loading">Loading contacts...</p>';
        const contacts = await getContacts();
        
        if (contacts.length === 0) {
            container.innerHTML = '<p class="no-data">No contact submissions</p>';
            return;
        }
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Mobile</th>
                        <th>City</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${contacts.map(contact => `
                        <tr>
                            <td>${contact.name}</td>
                            <td>${contact.email}</td>
                            <td>${contact.mobile}</td>
                            <td>${contact.city}</td>
                            <td>${new Date(contact.createdAt).toLocaleDateString()}</td>
                            <td>
                                <button class="delete-button" onclick="deleteContactItem('${contact._id}')">Delete</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

window.deleteContactItem = async function(id) {
    if (confirm('Are you sure you want to delete this contact?')) {
        try {
            await deleteContact(id);
            alert('Contact deleted successfully!');
            loadContacts();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
};

// Newsletter Management
async function loadNewsletters() {
    const container = document.getElementById('newsletters-list');
    
    try {
        container.innerHTML = '<p class="loading">Loading subscribers...</p>';
        const subscribers = await getSubscribers();
        
        if (subscribers.length === 0) {
            container.innerHTML = '<p class="no-data">No subscribers</p>';
            return;
        }
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Email</th>
                        <th>Date Subscribed</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${subscribers.map(sub => `
                        <tr>
                            <td>${sub.email}</td>
                            <td>${new Date(sub.createdAt).toLocaleDateString()}</td>
                            <td>
                                <button class="delete-button" onclick="deleteSubscriberItem('${sub._id}')">Delete</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        container.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

window.deleteSubscriberItem = async function(id) {
    if (confirm('Are you sure you want to delete this subscriber?')) {
        try {
            await deleteSubscriber(id);
            alert('Subscriber deleted successfully!');
            loadNewsletters();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
};

