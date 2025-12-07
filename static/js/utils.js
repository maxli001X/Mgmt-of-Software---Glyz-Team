// Toast notification system
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast ' + type;

    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };

    toast.innerHTML = `
<span class="toast-icon">${icons[type] || icons.info}</span>
<span class="toast-message">${message}</span>
<button class="toast-close" onclick="this.parentElement.remove()">×</button>
`;

    container.appendChild(toast);

    // Auto-remove after duration
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Make showToast globally available
window.showToast = showToast;

// Preserve scroll position across page reloads (for form submissions)
(function () {
    // Save scroll position before form submission
    document.addEventListener('submit', function (e) {
        // Only for non-AJAX forms (forms that will cause page reload)
        const form = e.target;
        if (form && form.tagName === 'FORM' && form.method.toLowerCase() === 'post') {
            // Check if it's not an AJAX form (doesn't have data-ajax attribute)
            if (!form.hasAttribute('data-ajax')) {
                // Save current scroll position
                sessionStorage.setItem('scrollPosition', window.scrollY.toString());
                // Also save the element that was focused (for comment forms)
                const activeElement = document.activeElement;
                if (activeElement && activeElement.tagName === 'TEXTAREA') {
                    sessionStorage.setItem('focusedElement', activeElement.name || activeElement.id || '');
                }
            }
        }
    });

    // Restore scroll position after page load
    function restoreScrollPosition() {
        const savedPosition = sessionStorage.getItem('scrollPosition');
        if (savedPosition) {
            const position = parseInt(savedPosition, 10);
            // Restore immediately, then again after a short delay to ensure it sticks
            window.scrollTo(0, position);

            // Restore again after DOM is fully ready (toasts might shift layout)
            setTimeout(function () {
                window.scrollTo(0, position);
                // Clear the saved position after restoring
                sessionStorage.removeItem('scrollPosition');
            }, 100);
        }
    }

    // Try to restore on DOMContentLoaded (faster)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', restoreScrollPosition);
    } else {
        // DOM already loaded, restore immediately
        restoreScrollPosition();
    }

    // Also restore on full page load as backup
    window.addEventListener('load', function () {
        const savedPosition = sessionStorage.getItem('scrollPosition');
        if (savedPosition) {
            window.scrollTo(0, parseInt(savedPosition, 10));
        }
    });
})();
