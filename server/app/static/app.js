const API = '/api';
let token = localStorage.getItem('mototrack_token') || '';
let motorcycles = [];

const authSection = document.getElementById('authSection');
const appSection = document.getElementById('appSection');
const logoutBtn = document.getElementById('logoutBtn');
const toast = document.getElementById('toast');
const motorcycleList = document.getElementById('motorcycleList');
const dashboardList = document.getElementById('dashboardList');
const maintenanceMotorcycle = document.getElementById('maintenanceMotorcycle');

function showToast(message) {
  toast.textContent = message;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), 3000);
}

async function api(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || data.message || 'Something went wrong');
  }
  return data;
}

function setAuthState(isLoggedIn) {
  authSection.classList.toggle('hidden', isLoggedIn);
  appSection.classList.toggle('hidden', !isLoggedIn);
  logoutBtn.classList.toggle('hidden', !isLoggedIn);
}

function populateMotorcycleOptions() {
  maintenanceMotorcycle.innerHTML = '<option value="">Select motorcycle</option>';
  motorcycles.forEach((m) => {
    const option = document.createElement('option');
    option.value = m.id;
    option.textContent = `${m.nickname} — ${m.year} ${m.make} ${m.model}`;
    maintenanceMotorcycle.appendChild(option);
  });
}

function renderMotorcycles() {
  motorcycleList.innerHTML = '';
  if (!motorcycles.length) {
    motorcycleList.innerHTML = '<p>No motorcycles added yet.</p>';
    return;
  }

  motorcycles.forEach((m) => {
    const card = document.createElement('div');
    card.className = 'item';
    card.innerHTML = `
      <h3>${m.nickname}</h3>
      <p>${m.year} ${m.make} ${m.model}</p>
      <p>Current mileage: ${m.current_mileage.toLocaleString()}</p>
      ${m.vin ? `<p>VIN: ${m.vin}</p>` : ''}
      ${m.notes ? `<p>${m.notes}</p>` : ''}
      <span class="badge">Bike profile</span>
      <div class="inline-actions">
        <button data-id="${m.id}" class="view-logs">View Logs</button>
        <button data-id="${m.id}" class="danger delete-motorcycle">Delete</button>
      </div>
      <div id="logs-${m.id}" class="stack" style="margin-top:0.8rem;"></div>
    `;
    motorcycleList.appendChild(card);
  });

  document.querySelectorAll('.view-logs').forEach((btn) => {
    btn.addEventListener('click', () => loadLogs(btn.dataset.id));
  });
  document.querySelectorAll('.delete-motorcycle').forEach((btn) => {
    btn.addEventListener('click', () => deleteMotorcycle(btn.dataset.id));
  });
}

function renderDashboard(data) {
  dashboardList.innerHTML = '';
  if (!data.length) {
    dashboardList.innerHTML = '<p>Your dashboard will appear after you add motorcycles.</p>';
    return;
  }

  data.forEach((entry) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'item';

    const dueHtml = entry.due_services.length
      ? entry.due_services.map((service) => `
          <div class="item" style="margin-top:0.6rem;">
            <h4>${service.service_type}</h4>
            <p>Last service: ${service.last_service_date} at ${service.last_service_mileage.toLocaleString()} mi</p>
            ${service.next_due_mileage ? `<p>Due mileage: ${service.next_due_mileage.toLocaleString()} mi</p>` : ''}
            ${service.next_due_date ? `<p>Due date: ${service.next_due_date}</p>` : ''}
            <span class="badge due">${service.status}</span>
          </div>
        `).join('')
      : '<p>No overdue services right now.</p>';

    const recentHtml = entry.recent_logs.length
      ? entry.recent_logs.map((log) => `<p>• ${log.service_type} — ${log.service_date} @ ${log.mileage_at_service.toLocaleString()} mi</p>`).join('')
      : '<p>No maintenance history yet.</p>';

    wrapper.innerHTML = `
      <h3>${entry.motorcycle.nickname}</h3>
      <p>${entry.motorcycle.year} ${entry.motorcycle.make} ${entry.motorcycle.model}</p>
      <p>Current mileage: ${entry.motorcycle.current_mileage.toLocaleString()}</p>
      <h4>Due Services</h4>
      ${dueHtml}
      <h4>Recent Logs</h4>
      ${recentHtml}
    `;

    dashboardList.appendChild(wrapper);
  });
}

async function loadMotorcycles() {
  motorcycles = await api('/motorcycles');
  populateMotorcycleOptions();
  renderMotorcycles();
}

async function loadDashboard() {
  const data = await api('/dashboard');
  renderDashboard(data);
}

async function loadLogs(motorcycleId) {
  const logs = await api(`/maintenance/motorcycle/${motorcycleId}`);
  const target = document.getElementById(`logs-${motorcycleId}`);
  if (!logs.length) {
    target.innerHTML = '<p>No logs yet.</p>';
    return;
  }

  target.innerHTML = logs.map((log) => `
    <div class="item">
      <h4>${log.service_type}</h4>
      <p>Date: ${log.service_date}</p>
      <p>Mileage: ${log.mileage_at_service.toLocaleString()}</p>
      ${log.cost ? `<p>Cost: $${Number(log.cost).toFixed(2)}</p>` : ''}
      ${log.next_due_mileage ? `<p>Next due mileage: ${log.next_due_mileage.toLocaleString()}</p>` : ''}
      ${log.next_due_date ? `<p>Next due date: ${log.next_due_date}</p>` : ''}
      ${log.notes ? `<p>${log.notes}</p>` : ''}
    </div>
  `).join('');
}

async function deleteMotorcycle(id) {
  await api(`/motorcycles/${id}`, { method: 'DELETE' });
  showToast('Motorcycle deleted.');
  await refreshApp();
}

async function refreshApp() {
  await loadMotorcycles();
  await loadDashboard();
}

document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target).entries());
  try {
    const result = await api('/auth/register', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
    token = result.access_token;
    localStorage.setItem('mototrack_token', token);
    setAuthState(true);
    e.target.reset();
    showToast('Account created.');
    await refreshApp();
  } catch (err) {
    showToast(err.message);
  }
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target).entries());
  try {
    const result = await api('/auth/login', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
    token = result.access_token;
    localStorage.setItem('mototrack_token', token);
    setAuthState(true);
    e.target.reset();
    showToast('Logged in.');
    await refreshApp();
  } catch (err) {
    showToast(err.message);
  }
});

document.getElementById('motorcycleForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target).entries());
  try {
    await api('/motorcycles', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
    e.target.reset();
    showToast('Motorcycle saved.');
    await refreshApp();
  } catch (err) {
    showToast(err.message);
  }
});

document.getElementById('maintenanceForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target).entries());
  try {
    await api('/maintenance', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
    e.target.reset();
    showToast('Maintenance log saved.');
    await refreshApp();
  } catch (err) {
    showToast(err.message);
  }
});

logoutBtn.addEventListener('click', () => {
  token = '';
  localStorage.removeItem('mototrack_token');
  setAuthState(false);
  showToast('Logged out.');
});

(async function init() {
  if (token) {
    setAuthState(true);
    try {
      await refreshApp();
    } catch {
      token = '';
      localStorage.removeItem('mototrack_token');
      setAuthState(false);
    }
  } else {
    setAuthState(false);
  }
})();
