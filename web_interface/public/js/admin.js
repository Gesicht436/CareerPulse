import { apiClient } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log('Admin Console Initialized');

    // DOM Elements
    const adminLoginView = document.getElementById('admin-login-view');
    const adminDashboardView = document.getElementById('admin-dashboard-view');
    const adminLoginForm = document.getElementById('admin-login-form');
    const adminEmailInput = document.getElementById('admin-email');
    const adminPasswordInput = document.getElementById('admin-password');
    const adminAlertBanner = document.getElementById('admin-alert-banner');
    const adminAlertMessage = document.getElementById('admin-alert-message');
    const adminLogoutBtn = document.getElementById('admin-logout-btn');

    // Control Elements
    const bannerInput = document.getElementById('banner-text-input');
    const bannerActiveToggle = document.getElementById('banner-active-toggle');
    const saveBannerBtn = document.getElementById('save-banner-btn');
    const maintenanceToggle = document.getElementById('maintenance-toggle');
    const expertCallsToggle = document.getElementById('toggle-expert-calls');
    const uploadToggle = document.getElementById('toggle-upload');
    const analyzerToggle = document.getElementById('toggle-analyzer');
    const clearLogsBtn = document.getElementById('clear-logs-btn');
    const refreshTelemetryBtn = document.getElementById('refresh-telemetry-btn');

    // Check existing admin token
    checkAdminAuth();

    async function checkAdminAuth() {
        const token = localStorage.getItem('admin_token');
        if (!token) {
            showLoginView();
            return;
        }

        try {
            // Verify admin token with backend
            const user = await apiClient.get('/api/v1/admin/me');
            if (user && user.role === 'admin') {
                showDashboardView();
                loadTelemetryData();
            } else {
                showLoginView();
            }
        } catch (e) {
            console.warn('Admin session expired or invalid:', e);
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            showLoginView();
        }
    }

    function showLoginView() {
        adminLoginView.classList.remove('hidden');
        adminDashboardView.classList.add('hidden');
    }

    function showDashboardView() {
        adminLoginView.classList.add('hidden');
        adminDashboardView.classList.remove('hidden');
    }

    // Handle Admin Login Submit
    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = adminEmailInput.value.trim();
            const password = adminPasswordInput.value.trim();

            if (!email || !password) {
                showAlert('Please enter both email and password.');
                return;
            }

            try {
                const response = await apiClient.post('/api/v1/admin/login', { email, password });
                
                localStorage.setItem('admin_token', response.access_token);
                localStorage.setItem('admin_user', JSON.stringify(response.user));
                
                hideAlert();
                showDashboardView();
                loadTelemetryData();
            } catch (err) {
                console.error('Admin Login Error:', err);
                showAlert(err.message || 'Admin authentication failed.');
            }
        });
    }

    // Logout Action
    if (adminLogoutBtn) {
        adminLogoutBtn.addEventListener('click', () => {
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            showLoginView();
        });
    }

    // Load Telemetry & Settings
    async function loadTelemetryData() {
        try {
            const telemetry = await apiClient.get('/api/v1/admin/telemetry');
            renderMetrics(telemetry.metrics, telemetry.total_registered_users, telemetry.system_stats);
            renderSettings(telemetry.settings);
            renderActivityLogs(telemetry.activity_logs);
            renderUsersTable();
        } catch (err) {
            console.error('Failed to load telemetry:', err);
        }
    }

    if (refreshTelemetryBtn) {
        refreshTelemetryBtn.addEventListener('click', () => {
            loadTelemetryData();
        });
    }

    function renderMetrics(metrics = {}, totalUsers = 0, systemStats = {}) {
        document.getElementById('metric-total-users').textContent = totalUsers;
        document.getElementById('metric-total-analyses').textContent = metrics.total_resume_analyses || 0;
        document.getElementById('metric-total-expert').textContent = metrics.total_expert_sessions || 0;
        document.getElementById('metric-total-searches').textContent = metrics.total_job_searches || 0;
        
        // System stats
        document.getElementById('stat-cpu').textContent = `${systemStats.cpu_usage_percent || 12}%`;
        document.getElementById('stat-ram').textContent = `${systemStats.ram_usage_percent || 42}% (${systemStats.ram_used_mb || 4096}MB)`;
        document.getElementById('stat-uptime').textContent = formatUptime(systemStats.uptime_seconds || 3600);
    }

    function renderSettings(settings = {}) {
        if (bannerInput) bannerInput.value = settings.announcement_banner || '';
        if (bannerActiveToggle) bannerActiveToggle.checked = !!settings.announcement_active;
        if (maintenanceToggle) maintenanceToggle.checked = !!settings.maintenance_mode;
        if (expertCallsToggle) expertCallsToggle.checked = settings.enable_expert_calls !== False;
        if (uploadToggle) uploadToggle.checked = settings.enable_resume_upload !== False;
        if (analyzerToggle) analyzerToggle.checked = settings.enable_jd_analyzer !== False;
    }

    // Save Website Banner Settings
    if (saveBannerBtn) {
        saveBannerBtn.addEventListener('click', async () => {
            try {
                saveBannerBtn.disabled = true;
                saveBannerBtn.textContent = 'Saving...';
                await apiClient.post('/api/v1/admin/settings', {
                    announcement_banner: bannerInput.value,
                    announcement_active: bannerActiveToggle.checked
                });
                alert('Website announcement banner settings updated successfully!');
            } catch (err) {
                alert('Failed to update banner: ' + err.message);
            } finally {
                saveBannerBtn.disabled = false;
                saveBannerBtn.textContent = 'Publish Live Banner';
            }
        });
    }

    // Toggle Toggles Event Handlers
    const setupToggleListener = (el, settingKey) => {
        if (el) {
            el.addEventListener('change', async () => {
                try {
                    await apiClient.post('/api/v1/admin/settings', { [settingKey]: el.checked });
                    console.log(`Setting ${settingKey} updated to ${el.checked}`);
                } catch (e) {
                    alert('Failed to update setting: ' + e.message);
                    el.checked = !el.checked;
                }
            });
        }
    };

    setupToggleListener(maintenanceToggle, 'maintenance_mode');
    setupToggleListener(expertCallsToggle, 'enable_expert_calls');
    setupToggleListener(uploadToggle, 'enable_resume_upload');
    setupToggleListener(analyzerToggle, 'enable_jd_analyzer');

    // Render Activity Audit Logs
    function renderActivityLogs(logs = []) {
        const container = document.getElementById('activity-logs-container');
        if (!container) return;

        if (!logs.length) {
            container.innerHTML = `<div class="p-6 text-center text-xs text-slate-500">No activity logs recorded yet.</div>`;
            return;
        }

        container.innerHTML = logs.map(log => {
            const timeStr = new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const dateStr = new Date(log.timestamp).toLocaleDateString();
            let badgeClass = 'bg-slate-800 text-slate-300';

            if (log.event_type.includes('ADMIN')) badgeClass = 'bg-violet-950 text-violet-300 border-violet-800';
            else if (log.event_type.includes('ANALYSIS') || log.event_type.includes('JD')) badgeClass = 'bg-teal-950 text-teal-300 border-teal-800';
            else if (log.event_type.includes('EXPERT')) badgeClass = 'bg-emerald-950 text-emerald-300 border-emerald-800';
            else if (log.event_type.includes('SEARCH')) badgeClass = 'bg-indigo-950 text-indigo-300 border-indigo-800';
            else if (log.event_type.includes('DELETED')) badgeClass = 'bg-rose-950 text-rose-300 border-rose-800';

            return `
                <div class="p-3 bg-slate-900/60 border-b border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                    <div class="flex items-center gap-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${badgeClass}">
                            ${log.event_type}
                        </span>
                        <span class="text-slate-200 font-medium">${log.description}</span>
                    </div>
                    <div class="text-[11px] text-slate-500 shrink-0 font-mono">
                        ${dateStr} ${timeStr}
                    </div>
                </div>
            `;
        }).join('');
    }

    // Render Users Table
    async function renderUsersTable() {
        const tableBody = document.getElementById('users-table-body');
        if (!tableBody) return;

        try {
            const data = await apiClient.get('/api/v1/admin/users');
            const users = data.users || [];

            if (!users.length) {
                tableBody.innerHTML = `<tr><td colspan="5" class="p-4 text-center text-xs text-slate-500">No registered users found.</td></tr>`;
                return;
            }

            tableBody.innerHTML = users.map(u => `
                <tr class="border-b border-slate-800/60 hover:bg-slate-900/40 transition-colors text-xs">
                    <td class="p-3 font-mono text-violet-400 font-bold">${u.id}</td>
                    <td class="p-3 font-bold text-slate-200">${u.full_name}</td>
                    <td class="p-3 text-slate-300">${u.email}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold ${u.role === 'admin' ? 'bg-violet-900 text-violet-300 border border-violet-700' : 'bg-slate-800 text-slate-400'}">
                            ${u.role.toUpperCase()}
                        </span>
                    </td>
                    <td class="p-3 text-right">
                        ${u.role !== 'admin' ? `
                            <button data-userid="${u.id}" class="btn-delete-user text-rose-400 hover:text-rose-300 font-bold px-2.5 py-1 rounded bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800/60 transition-colors">
                                Delete User
                            </button>
                        ` : '<span class="text-slate-600 italic">Protected Admin</span>'}
                    </td>
                </tr>
            `).join('');

            // Attach Delete Event Listeners
            document.querySelectorAll('.btn-delete-user').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const userId = e.target.getAttribute('data-userid');
                    if (confirm(`Are you sure you want to delete user account ${userId}?`)) {
                        try {
                            await apiClient.delete(`/api/v1/admin/users/${userId}`);
                            renderUsersTable();
                            loadTelemetryData();
                        } catch (err) {
                            alert('Failed to delete user: ' + err.message);
                        }
                    }
                });
            });

        } catch (e) {
            console.error('Failed to load user list:', e);
        }
    }

    // Clear Audit Logs
    if (clearLogsBtn) {
        clearLogsBtn.addEventListener('click', async () => {
            if (confirm('Clear all telemetry activity logs?')) {
                try {
                    await apiClient.post('/api/v1/admin/clear-logs');
                    loadTelemetryData();
                } catch (e) {
                    alert('Failed to clear logs: ' + e.message);
                }
            }
        });
    }

    function showAlert(msg) {
        if (adminAlertBanner && adminAlertMessage) {
            adminAlertMessage.textContent = msg;
            adminAlertBanner.classList.remove('hidden');
        }
    }

    function hideAlert() {
        if (adminAlertBanner) {
            adminAlertBanner.classList.add('hidden');
        }
    }

    function formatUptime(seconds) {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        return `${hrs}h ${mins}m`;
    }
});
