// API Configuration
const API_URL = 'http://localhost:5000/api';

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Projects API
export const getProjects = () => apiCall('/projects');
export const createProject = (formData) => apiCall('/projects', {
    method: 'POST',
    body: formData
});
export const updateProject = (id, formData) => apiCall(`/projects/${id}`, {
    method: 'PUT',
    body: formData
});
export const deleteProject = (id) => apiCall(`/projects/${id}`, {
    method: 'DELETE'
});

// Clients API
export const getClients = () => apiCall('/clients');
export const createClient = (formData) => apiCall('/clients', {
    method: 'POST',
    body: formData
});
export const updateClient = (id, formData) => apiCall(`/clients/${id}`, {
    method: 'PUT',
    body: formData
});
export const deleteClient = (id) => apiCall(`/clients/${id}`, {
    method: 'DELETE'
});

// Contacts API
export const submitContact = (data) => apiCall('/contacts', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
export const getContacts = () => apiCall('/contacts');
export const deleteContact = (id) => apiCall(`/contacts/${id}`, {
    method: 'DELETE'
});

// Newsletter API
export const subscribeNewsletter = (email) => apiCall('/newsletters', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email })
});
export const getSubscribers = () => apiCall('/newsletters');
export const deleteSubscriber = (id) => apiCall(`/newsletters/${id}`, {
    method: 'DELETE'
});

