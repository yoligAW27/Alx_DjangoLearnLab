document.addEventListener('DOMContentLoaded', function() {
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const strengthMeter = document.getElementById('strengthMeter');
    
    password1.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        
        if (password.length >= 8) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[a-z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^A-Za-z0-9]/)) strength++;
        
        strengthMeter.className = 'strength-meter-fill';
        if (strength <= 2) {
            strengthMeter.classList.add('strength-weak');
        } else if (strength <= 4) {
            strengthMeter.classList.add('strength-medium');
        } else {
            strengthMeter.classList.add('strength-strong');
        }
    });
    
    password2.addEventListener('input', function() {
        if (password1.value === password2.value) {
            this.style.borderColor = '#28a745';
        } else {
            this.style.borderColor = '#dc3545';
        }
    });
});