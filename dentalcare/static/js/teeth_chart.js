let currentMode = 'normal', editMode = false;
let deciduousCurrentMode = 'normal', deciduousEditMode = false;

const teethData = Array.from({ length: 32 }, (_, i) => ({ number: i + 1, status: 'normal' }));
const deciduousData = Array.from({ length: 20 }, (_, i) => ({ number: i + 1, status: 'normal' }));

function renderTeeth() {
    const upper = document.getElementById('upper-row');
    const lower = document.getElementById('lower-row');
    upper.innerHTML = lower.innerHTML = '';
    teethData.forEach((tooth, i) => {
        // Set initial saved status if available
        const savedStatus = initialTeethStatus[tooth.number];
        if (savedStatus) {
            tooth.status = savedStatus;
        }

        const div = document.createElement('div');
        div.className = 'tooth';
        div.dataset.index = i;
        div.innerHTML = `
            <img src="/static/images/teeth${tooth.number}.jpeg" 
                 class="${tooth.status === 'missing' ? 'hidden' : ''} ${tooth.status === 'impacted' ? 'impacted' : ''}">
            <span>${tooth.number}</span>`;
        div.onclick = () => editMode && toggleTooth(i);
        (i < 16 ? upper : lower).appendChild(div);
    });
}


function toggleTooth(i) {
    teethData[i].status = currentMode === teethData[i].status ? 'normal' : currentMode;
    renderTeeth();
}

function setMode(mode) {
    currentMode = mode;
    renderTeeth();
}

function renderDeciduousTeeth() {
    const upper = document.getElementById('decid-upper-row');
    const lower = document.getElementById('decid-lower-row');
    upper.innerHTML = lower.innerHTML = '';
    deciduousData.forEach((tooth, i) => {
        const div = document.createElement('div');
        div.className = 'tooth';
        div.dataset.index = i;
        div.innerHTML = `
            <img src="/static/images/decid${tooth.number}.jpeg"
                 class="${tooth.status === 'missing' ? 'hidden' : ''} ${tooth.status === 'impacted' ? 'impacted' : ''}">
            <span>${tooth.number}</span>`;
        div.onclick = () => deciduousEditMode && toggleDeciduousTooth(i);
        (i < 10 ? upper : lower).appendChild(div);
    });
}

function toggleDeciduousTooth(i) {
    deciduousData[i].status = deciduousCurrentMode === deciduousData[i].status ? 'normal' : deciduousCurrentMode;
    renderDeciduousTeeth();
}

function setDeciduousMode(mode) {
    deciduousCurrentMode = mode;
    renderDeciduousTeeth();
}

function toggleDeciduousSection() {
    const section = document.getElementById('deciduousSection');
    const checkbox = document.getElementById('deciduousToggle');
    section.style.display = checkbox.checked ? 'block' : 'none';
}

// Send data to Django backend
function saveTeethChart(patientId) {
    fetch(`/save_teeth_chart/${patientId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            permanent: teethData,
            deciduous: deciduousData,
        }),
    })
    .then(response => {
        if (!response.ok) throw new Error("Network error");
        return response.json();
    })
    .then(data => {
        alert("Teeth chart saved successfully!");
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to save.");
    });
}

// Helper to get CSRF token
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }
    return '';
}

function goBack() {
    window.history.back();
}

// Initial Render
renderTeeth();
renderDeciduousTeeth();
