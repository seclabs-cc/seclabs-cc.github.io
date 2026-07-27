document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('theme-toggle-sun');
    const moonIcon = document.getElementById('theme-toggle-moon');

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        document.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));

        if (theme === 'light') {
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        } else {
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        }
    }

    // Initialize theme based on preference or localStorage
    const savedTheme = localStorage.getItem('theme') || 'dark';
    applyTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(newTheme);
        });
    }
});
