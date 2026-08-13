import { apiClient } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const signinTab = document.getElementById('tab-signin');
    const signupTab = document.getElementById('tab-signup');
    const signinForm = document.getElementById('form-signin');
    const signupForm = document.getElementById('form-signup');
    const alertBanner = document.getElementById('alert-banner');
    const alertMessage = document.getElementById('alert-message');

    // Check if already logged in
    const existingToken = localStorage.getItem('auth_token');
    const existingUser = localStorage.getItem('auth_user');
    if (existingToken && existingUser) {
        console.log('User already logged in:', JSON.parse(existingUser));
    }

    // Tab Switcher
    if (signinTab && signupTab) {
        signinTab.addEventListener('click', () => {
            signinTab.classList.add('bg-violet-600', 'text-white');
            signinTab.classList.remove('bg-gray-100', 'text-gray-600');
            signupTab.classList.add('bg-gray-100', 'text-gray-600');
            signupTab.classList.remove('bg-violet-600', 'text-white');
            
            signinForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
            hideAlert();
        });

        signupTab.addEventListener('click', () => {
            signupTab.classList.add('bg-violet-600', 'text-white');
            signupTab.classList.remove('bg-gray-100', 'text-gray-600');
            signinTab.classList.add('bg-gray-100', 'text-gray-600');
            signinTab.classList.remove('bg-violet-600', 'text-white');
            
            signupForm.classList.remove('hidden');
            signinForm.classList.add('hidden');
            hideAlert();
        });
    }

    // Handle Sign In Submit
    if (signinForm) {
        signinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlert();

            const email = document.getElementById('signin-email').value.trim();
            const password = document.getElementById('signin-password').value;

            if (!email || !password) {
                showAlert('Please fill in all fields.', 'error');
                return;
            }

            const btn = signinForm.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.textContent = 'Signing In...';

            try {
                const response = await apiClient.post('/api/v1/auth/login', { email, password });
                console.log('Login Successful:', response);

                localStorage.setItem('auth_token', response.access_token);
                localStorage.setItem('auth_user', JSON.stringify(response.user));

                showAlert(`Welcome back, ${response.user.full_name}! Redirecting...`, 'success');
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            } catch (err) {
                showAlert(err.message || 'Login failed. Please check your credentials.', 'error');
                btn.disabled = false;
                btn.textContent = 'Sign In';
            }
        });
    }

    // Handle Sign Up Submit
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlert();

            const fullName = document.getElementById('signup-fullname').value.trim();
            const email = document.getElementById('signup-email').value.trim();
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-confirm').value;

            if (!fullName || !email || !password) {
                showAlert('Please fill in all required fields.', 'error');
                return;
            }

            if (password.length < 6) {
                showAlert('Password must be at least 6 characters long.', 'error');
                return;
            }

            if (password !== confirmPassword) {
                showAlert('Passwords do not match.', 'error');
                return;
            }

            const btn = signupForm.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.textContent = 'Creating Account...';

            try {
                const response = await apiClient.post('/api/v1/auth/signup', {
                    full_name: fullName,
                    email: email,
                    password: password
                });

                console.log('Registration Successful:', response);
                localStorage.setItem('auth_token', response.access_token);
                localStorage.setItem('auth_user', JSON.stringify(response.user));

                showAlert(`Account created successfully! Welcome, ${response.user.full_name}. Redirecting...`, 'success');
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            } catch (err) {
                showAlert(err.message || 'Registration failed. Email may already be in use.', 'error');
                btn.disabled = false;
                btn.textContent = 'Create Account';
            }
        });
    }

    function showAlert(msg, type = 'error') {
        if (!alertBanner || !alertMessage) return;
        alertMessage.textContent = msg;
        alertBanner.classList.remove('hidden');
        if (type === 'success') {
            alertBanner.className = 'mb-6 p-4 rounded-xl text-sm font-medium bg-teal-50 border border-teal-200 text-teal-700';
        } else {
            alertBanner.className = 'mb-6 p-4 rounded-xl text-sm font-medium bg-rose-50 border border-rose-200 text-rose-700';
        }
    }

    function hideAlert() {
        if (alertBanner) alertBanner.classList.add('hidden');
    }
});
