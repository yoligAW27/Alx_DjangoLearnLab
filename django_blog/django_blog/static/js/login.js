console.log('Login page loaded');

document.querySelectorAll('.form-group input').forEach(input => {
    input.addEventListener('focus', function() {
        this.style.borderColor = '#007bff';
    });
    
    input.addEventListener('blur', function() {
        this.style.borderColor = '#e0e0e0';
    });
});