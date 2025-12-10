import { getProjects, getClients, submitContact, subscribeNewsletter } from './api.js';

// API URL - Works for both local development and Vercel deployment
const API_URL = window.location.origin.includes('vercel.app') || window.location.origin.includes('localhost') === false
    ? ''  // Use relative URL for production (Vercel)
    : 'http://localhost:5000';  // Use localhost for development

// Load projects on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadProjects();
    await loadClients();
    setupContactForm();
    setupNewsletterForm();
});

// Load and display projects
async function loadProjects() {
    const container = document.getElementById('projects-container');
    
    try {
        container.innerHTML = '<p class="loading">Loading projects...</p>';
        const projects = await getProjects();
        
        if (projects.length === 0) {
            container.innerHTML = '<p class="no-data">No projects available</p>';
            return;
        }
        
        container.innerHTML = projects.map(project => `
            <div class="project-card">
                <div class="project-image">
                    <img src="${project.image.startsWith('http') ? project.image : API_URL + project.image}" 
                         alt="${project.name}"
                         onerror="this.src='https://via.placeholder.com/450x350?text=Project+Image'">
                </div>
                <div class="project-info">
                    <h3 class="project-name">${project.name}</h3>
                    <p class="project-description">${project.description}</p>
                    <button class="read-more-btn">Read More</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<p class="error">Failed to load projects: ${error.message}</p>`;
        console.error('Error loading projects:', error);
    }
}

// Load and display clients
async function loadClients() {
    const container = document.getElementById('clients-container');
    
    try {
        container.innerHTML = '<p class="loading">Loading clients...</p>';
        const clients = await getClients();
        
        if (clients.length === 0) {
            container.innerHTML = '<p class="no-data">No clients available</p>';
            return;
        }
        
        container.innerHTML = clients.map(client => `
            <div class="client-card">
                <div class="client-image">
                    <img src="${client.image.startsWith('http') ? client.image : API_URL + client.image}" 
                         alt="${client.name}"
                         onerror="this.src='https://via.placeholder.com/150?text=Client'">
                </div>
                <div class="client-info">
                    <p class="client-description">"${client.description}"</p>
                    <h3 class="client-name">${client.name}</h3>
                    <p class="client-designation">${client.designation}</p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = `<p class="error">Failed to load clients: ${error.message}</p>`;
        console.error('Error loading clients:', error);
    }
}

// Setup contact form
function setupContactForm() {
    const form = document.getElementById('contact-form');
    const messageDiv = document.getElementById('contact-message');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            mobile: document.getElementById('mobile').value,
            city: document.getElementById('city').value
        };
        
        try {
            messageDiv.innerHTML = '';
            await submitContact(formData);
            messageDiv.innerHTML = '<div class="message success">Thank you! Your message has been submitted successfully.</div>';
            form.reset();
        } catch (error) {
            messageDiv.innerHTML = `<div class="message error">Error: ${error.message}</div>`;
        }
    });
}

// Setup newsletter form
function setupNewsletterForm() {
    const form = document.getElementById('newsletter-form');
    const messageDiv = document.getElementById('newsletter-message');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('newsletter-email').value;
        
        try {
            messageDiv.innerHTML = '';
            await subscribeNewsletter(email);
            messageDiv.innerHTML = '<div class="message success">Thank you for subscribing!</div>';
            form.reset();
        } catch (error) {
            messageDiv.innerHTML = `<div class="message error">Error: ${error.message}</div>`;
        }
    });
}

