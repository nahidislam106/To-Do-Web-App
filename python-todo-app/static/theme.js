document.addEventListener('DOMContentLoaded', function() {
    const themeSwitcher = document.querySelector('html');
    const themeButtons = document.querySelectorAll('.theme-btn');
    
    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme') || 'system';
    setTheme(savedTheme);
    
    // Set active button
    themeButtons.forEach(button => {
        if (button.dataset.theme === savedTheme) {
            button.classList.add('active');
        }
        
        button.addEventListener('click', () => {
            const theme = button.dataset.theme;
            setTheme(theme);
            localStorage.setItem('theme', theme);
            
            // Update active button
            themeButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });
    
    function setTheme(theme) {
        if (theme === 'system') {
            const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            themeSwitcher.dataset.theme = systemPrefersDark ? 'dark' : 'light';
            
            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                themeSwitcher.dataset.theme = e.matches ? 'dark' : 'light';
            });
        } else {
            themeSwitcher.dataset.theme = theme;
        }
    }
});