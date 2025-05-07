document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const downloadForm = document.getElementById('download-form');
    if (downloadForm) {
        downloadForm.addEventListener('submit', function(e) {
            const urlInput = document.getElementById('id_url');
            if (!urlInput || !urlInput.value.trim()) {
                e.preventDefault();
                showAlert('danger', 'Vui lòng nhập URL YouTube hợp lệ.');
                return false;
            }

            // Basic URL validation
            const urlPattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
            if (!urlPattern.test(urlInput.value.trim())) {
                e.preventDefault();
                showAlert('danger', 'URL không hợp lệ. Vui lòng nhập URL YouTube.');
                return false;
            }

            // Show loading indicator
            document.getElementById('loading-indicator').style.display = 'block';
            document.getElementById('submit-btn').disabled = true;
        });
    }

    // Format selection
    const formatSelector = document.getElementById('id_format');
    if (formatSelector) {
        formatSelector.addEventListener('change', function() {
            updateFormatDescription(this.value);
        });
        // Initialize description
        updateFormatDescription(formatSelector.value);
    }

    // Close alert buttons
    const closeButtons = document.querySelectorAll('.alert .close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
});

// Helper functions
function updateFormatDescription(format) {
    const descriptionEl = document.getElementById('format-description');
    if (!descriptionEl) return;

    let description = '';
    switch(format) {
        case 'mp3':
            description = 'Tải xuống dưới dạng file âm thanh MP3 (chỉ âm thanh, không có video).';
            break;
        case 'mov':
            description = 'Tải xuống dưới dạng file MOV (định dạng video của Apple).';
            break;
        case 'mp4':
        default:
            description = 'Tải xuống dưới dạng file MP4 (định dạng video phổ biến nhất).';
            break;
    }

    descriptionEl.textContent = description;
}

function showAlert(type, message) {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <button type="button" class="close">&times;</button>
        ${message}
    `;

    // Add close functionality
    const closeButton = alert.querySelector('.close');
    closeButton.addEventListener('click', function() {
        alert.remove();
    });

    alertsContainer.appendChild(alert);

    // Auto close after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}
