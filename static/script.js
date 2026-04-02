// Drag and Drop File Upload
function initializeDragDrop() {
    const uploadArea = document.getElementById('upload-area');
    if (!uploadArea) return;

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            document.getElementById('file-input').files = files;
            handleFileSelect();
        }
    });

    const fileInput = document.getElementById('file-input');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
}

function handleFileSelect() {
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const file = fileInput.files[0];

    if (!file) return;

    const validTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        showAlert('Invalid file type. Please upload PNG, JPG, GIF, BMP, or WebP.', 'danger');
        return;
    }

    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showAlert('File too large. Maximum size is 16MB.', 'danger');
        return;
    }

    // Show file preview
    const reader = new FileReader();
    reader.onload = (e) => {
        if (filePreview) {
            filePreview.innerHTML = `
                <div class="alert alert-success">
                    <strong>File selected:</strong> ${file.name}
                    <br><small>${(file.size / 1024).toFixed(2)} KB</small>
                </div>
            `;
        }
    };
    reader.readAsDataURL(file);
}

// Alert System
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
        console.error('Alert container not found');
        return;
    }

    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    alertContainer.insertAdjacentHTML('beforeend', alertHTML);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const formData = new FormData(form);
    let isValid = true;

    // Check required fields
    form.querySelectorAll('[required]').forEach((field) => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    // Password confirmation
    const password = form.querySelector('[name="password"]');
    const passwordConfirm = form.querySelector('[name="password_confirm"]');
    if (password && passwordConfirm && password.value !== passwordConfirm.value) {
        passwordConfirm.classList.add('is-invalid');
        showAlert('Passwords do not match.', 'danger');
        isValid = false;
    }

    // Email validation
    const email = form.querySelector('[name="email"]');
    if (email && !isValidEmail(email.value)) {
        email.classList.add('is-invalid');
        showAlert('Please enter a valid email address.', 'danger');
        isValid = false;
    }

    return isValid;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Form submission handler
function handleFormSubmit(formId, url, method = 'POST') {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateForm(formId)) {
            return;
        }

        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Processing...';

        try {
            const response = await fetch(url, {
                method: method,
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showAlert(data.message || 'Success!', 'success');
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1000);
                }
            } else {
                showAlert(data.message || 'An error occurred.', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('An unexpected error occurred.', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

// Copy to Clipboard
function copyToClipboard(text, buttonId) {
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById(buttonId);
        if (btn) {
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        }
    });
}

// Format Numbers
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Format Percentage
function formatPercentage(num) {
    return (num * 100).toFixed(2) + '%';
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Load and display results
async function loadResults(imageId) {
    const container = document.getElementById('results-container');
    if (!container) return;

    container.innerHTML = '<div class="text-center"><span class="spinner"></span> Loading results...</div>';

    try {
        const response = await fetch(`/detection/analyze/${imageId}`);
        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            container.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
    } catch (error) {
        console.error('Error loading results:', error);
        container.innerHTML = '<div class="alert alert-danger">Failed to load results</div>';
    }
}

function displayResults(data) {
    const container = document.getElementById('results-container');
    if (!container) return;

    const blurTypeColors = {
        'Gaussian': 'primary',
        'Motion': 'warning',
        'Defocus': 'info',
        'Lens': 'danger',
        'Sharp': 'success'
    };

    const color = blurTypeColors[data.blur_type] || 'secondary';

    let html = `
        <div class="row">
            <div class="col-lg-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h5 class="mb-0">Analysis Result</h5>
                    </div>
                    <div class="card-body text-center">
                        <div class="mb-3">
                            <span class="badge badge-${color}" style="font-size: 1.2rem; padding: 0.5rem 1.5rem;">
                                ${data.blur_type}
                            </span>
                        </div>
                        <h3 class="mb-3">${formatPercentage(data.confidence)}</h3>
                        <p class="text-muted">${data.explanation}</p>
                        <div class="mt-4">
                            <small class="text-muted">Processing Time: ${data.processing_time.toFixed(3)}s</small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="card mb-3">
                    <div class="card-header">
                        <h5 class="mb-0">Image Preview</h5>
                    </div>
                    <div class="card-body text-center">
                        <img src="${data.image_path}" alt="Uploaded image" class="img-fluid rounded" style="max-height: 300px;">
                    </div>
                </div>
            </div>
        </div>
    `;

    if (data.model_comparisons && data.model_comparisons.length > 0) {
        html += `
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Model Comparison</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Model</th>
                                    <th>Blur Type</th>
                                    <th>Confidence</th>
                                    <th>Time (ms)</th>
                                </tr>
                            </thead>
                            <tbody>
        `;

        data.model_comparisons.forEach((model) => {
            const modelColor = blurTypeColors[model.blur_type] || 'secondary';
            html += `
                <tr>
                    <td><strong>${model.model_name}</strong></td>
                    <td><span class="badge badge-${modelColor}">${model.blur_type}</span></td>
                    <td>${formatPercentage(model.confidence)}</td>
                    <td>${(model.processing_time * 1000).toFixed(1)}</td>
                </tr>
            `;
        });

        html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
}

// Pagination
function goToPage(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeDragDrop();

    // Add event listeners to all forms with class 'auto-validate'
    document.querySelectorAll('form.auto-validate').forEach((form) => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form.id)) {
                e.preventDefault();
            }
        });
    });

    // Format all dates with class 'format-date'
    document.querySelectorAll('.format-date').forEach((elem) => {
        if (elem.textContent) {
            elem.textContent = formatDate(elem.textContent);
        }
    });

    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((elem) => {
            new bootstrap.Tooltip(elem);
        });
    }
});

// Export functions for use in templates
window.showAlert = showAlert;
window.handleFormSubmit = handleFormSubmit;
window.copyToClipboard = copyToClipboard;
window.formatNumber = formatNumber;
window.formatPercentage = formatPercentage;
window.formatDate = formatDate;
window.loadResults = loadResults;
window.goToPage = goToPage;
