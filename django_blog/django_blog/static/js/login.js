// Login page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Login page loaded');
    
    // Add focus effects to inputs
    const inputs = document.querySelectorAll('.login-form input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#007bff';
            this.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
        });
        
        input.addEventListener('blur', function() {
            this.style.borderColor = '#e0e0e0';
            this.style.boxShadow = 'none';
        });
    });
    
    // Form submission handling
    const form = document.querySelector('.login-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const username = document.getElementById('id_username').value;
            const password = document.getElementById('id_password').value;
            
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in all fields');
            }
        });
    }
});
