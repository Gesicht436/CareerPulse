const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:8000' 
  : 'https://api.careerpulse.ai';

export const apiClient = {
  async post(endpoint, data) {
    const isFormData = data instanceof FormData;
    const headers = isFormData ? {} : { 'Content-Type': 'application/json' };
    
    const token = localStorage.getItem('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      body: isFormData ? data : JSON.stringify(data),
      headers: headers,
    });

    if (!response.ok) {
      let errorMsg = response.statusText;
      try {
        const errJson = await response.json();
        if (errJson.detail) errorMsg = errJson.detail;
      } catch (e) {}
      throw new Error(errorMsg);
    }
    return response.json();
  },

  async get(endpoint) {
    const headers = {};
    const token = localStorage.getItem('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: headers
    });

    if (!response.ok) {
      let errorMsg = response.statusText;
      try {
        const errJson = await response.json();
        if (errJson.detail) errorMsg = errJson.detail;
      } catch (e) {}
      throw new Error(errorMsg);
    }
    return response.json();
  },
};
