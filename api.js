// API Configuration - Works for both local development and Vercel deployment
const API_URL = window.location.origin.includes('vercel.app') || window.location.origin.includes('localhost') === false
    ? '/api'  // Use relative URL for production (Vercel)
    : 'http://localhost:5000/api';  // Use localhost for development

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
            }
        });
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        let data;
        
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            // If not JSON, try to get text and parse
            const text = await response.text();
            try {
                data = JSON.parse(text);
            } catch (e) {
                // If parsing fails, return error object
                data = { 
                    error: `Server returned non-JSON response: ${text.substring(0, 100)}`,
                    status: response.status
                };
            }
        }
        
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Helper function to convert FormData to JSON with base64 images
async function formDataToJson(formData) {
    const isVercel = window.location.origin.includes('vercel.app') || !window.location.origin.includes('localhost');
    
    if (!isVercel) {
        // For local development, return FormData as-is
        return formData;
    }
    
    // For Vercel, convert to JSON with base64 images
    const json = {};
    
    for (let [key, value] of formData.entries()) {
        if (value instanceof File) {
            // Convert file to base64
            const base64 = await new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(value);
            });
            json[key] = base64;
        } else {
            json[key] = value;
        }
    }
    
    return JSON.stringify(json);
}

// Projects API
export const getProjects = () => apiCall('/projects');
export const createProject = async (formData) => {
    const isVercel = window.location.origin.includes('vercel.app') || !window.location.origin.includes('localhost');
    const body = isVercel ? await formDataToJson(formData) : formData;
    const headers = isVercel ? { 'Content-Type': 'application/json' } : {};
    
    return apiCall('/projects', {
        method: 'POST',
        headers,
        body
    });
};
export const updateProject = async (id, formData) => {
    const isVercel = window.location.origin.includes('vercel.app') || !window.location.origin.includes('localhost');
    const body = isVercel ? await formDataToJson(formData) : formData;
    const headers = isVercel ? { 'Content-Type': 'application/json' } : {};
    
    return apiCall(`/projects/${id}`, {
        method: 'PUT',
        headers,
        body
    });
};
export const deleteProject = (id) => apiCall(`/projects/${id}`, {
    method: 'DELETE'
});

// Clients API
export const getClients = () => apiCall('/clients');
export const createClient = async (formData) => {
    const isVercel = window.location.origin.includes('vercel.app') || !window.location.origin.includes('localhost');
    const body = isVercel ? await formDataToJson(formData) : formData;
    const headers = isVercel ? { 'Content-Type': 'application/json' } : {};
    
    return apiCall('/clients', {
        method: 'POST',
        headers,
        body
    });
};
export const updateClient = async (id, formData) => {
    const isVercel = window.location.origin.includes('vercel.app') || !window.location.origin.includes('localhost');
    const body = isVercel ? await formDataToJson(formData) : formData;
    const headers = isVercel ? { 'Content-Type': 'application/json' } : {};
    
    return apiCall(`/clients/${id}`, {
        method: 'PUT',
        headers,
        body
    });
};
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

