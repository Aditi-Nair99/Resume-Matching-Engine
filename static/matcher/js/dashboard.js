function safeParse(value) {
    try { return JSON.parse((value || '').replace(/'/g, '"')); } catch (e) { return null; }
}

const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { labels: { color: '#eef4ff', font: { family: 'Inter' } } }
    },
    scales: {
        x: { ticks: { color: '#c7d3ee' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#c7d3ee' }, grid: { color: 'rgba(255,255,255,0.05)' } }
    }
};

function buildLineChart(canvas) {
    if (!canvas) return;
    const points = safeParse(canvas.dataset.points) || [];
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: points.map(p => p.label),
            datasets: [{
                label: 'Candidates',
                data: points.map(p => p.value),
                tension: 0.38,
                fill: true,
                borderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderColor: '#67f3ff',
                backgroundColor: 'rgba(103,243,255,0.12)'
            }]
        },
        options: {
            ...commonOptions,
            animation: { duration: 1500 },
        }
    });
}

function buildBarChart(canvas) {
    if (!canvas) return;
    const dataMap = safeParse(canvas.dataset.points) || {};
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: Object.keys(dataMap),
            datasets: [{
                label: 'Candidates',
                data: Object.values(dataMap),
                borderWidth: 1,
                borderRadius: 12,
                backgroundColor: ['rgba(72,180,255,0.75)','rgba(123,92,255,0.75)','rgba(103,243,255,0.75)','rgba(199,125,255,0.75)','rgba(135,245,209,0.75)']
            }]
        },
        options: {
            ...commonOptions,
            animation: { duration: 1400 },
        }
    });
}

function buildRadarChart(canvas) {
    if (!canvas) return;
    const points = safeParse(canvas.dataset.points) || [];
    new Chart(canvas, {
        type: 'radar',
        data: {
            labels: points.map(p => p.label),
            datasets: [{
                label: 'Best Score Distribution',
                data: points.map(p => p.value),
                borderWidth: 2,
                borderColor: '#c77dff',
                backgroundColor: 'rgba(199,125,255,0.2)',
                pointBackgroundColor: '#67f3ff'
            }]
        },
        options: {
            animation: { duration: 1800 },
            plugins: { legend: { labels: { color: '#eef4ff', font: { family: 'Inter' } } } },
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.08)' },
                    grid: { color: 'rgba(255,255,255,0.08)' },
                    pointLabels: { color: '#d6e3ff', font: { family: 'Inter' } },
                    ticks: { backdropColor: 'transparent', color: '#d6e3ff' }
                }
            }
        }
    });
}

function setupUploadInteractions() {
    const form = document.getElementById('resumeUploadForm');
    const dropzone = document.getElementById('dropzone');
    if (!form || !dropzone) return;

    const fileInput = dropzone.querySelector('input[type="file"]');
    const fileNameLabel = document.getElementById('fileNameLabel');
    const browseTrigger = document.getElementById('browseTrigger');
    const overlay = document.getElementById('analysisOverlay');

    if (browseTrigger && fileInput) {
        browseTrigger.addEventListener('click', () => fileInput.click());
    }

    if (fileInput) {
        fileInput.addEventListener('change', () => {
            const file = fileInput.files && fileInput.files[0];
            fileNameLabel.textContent = file ? file.name : 'No file selected';
        });
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, event => {
            event.preventDefault();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, event => {
            event.preventDefault();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', event => {
        const files = event.dataTransfer.files;
        if (files && files.length && fileInput) {
            fileInput.files = files;
            fileNameLabel.textContent = files[0].name;
        }
    });

    form.addEventListener('submit', event => {
        if (!fileInput || !fileInput.files || !fileInput.files.length) {
            return;
        }
        if (overlay) overlay.hidden = false;
    });
}

function resetOverlayOnPageLoad() {
    const overlay = document.getElementById('analysisOverlay');
    if (!overlay) return;
    overlay.hidden = true;
}

document.addEventListener('DOMContentLoaded', () => {
    resetOverlayOnPageLoad();
    buildLineChart(document.getElementById('growthChart'));
    buildBarChart(document.getElementById('roleChart'));
    buildRadarChart(document.getElementById('scoreChart'));
    setupUploadInteractions();
});

window.addEventListener('pageshow', resetOverlayOnPageLoad);
window.addEventListener('load', resetOverlayOnPageLoad);
