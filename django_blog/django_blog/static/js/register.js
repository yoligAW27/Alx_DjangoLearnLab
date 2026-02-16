// Register page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Register page loaded');
    
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const strengthMeter = document.getElementById('strengthMeter');
    const form = document.querySelector('.register-form');
    
    // Password strength checker
    if (password1) {
        password1.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            // Check requirements
            const lengthCheck = password.length >= 8;
            const upperCheck = /[A-Z]/.test(password);
            const lowerCheck = /[a-z]/.test(password);
            const numberCheck = /[0-9]/.test(password);
            const specialCheck = /[^A-Za-z0-9]/.test(password);
            
            // Update requirement list if it exists
            document.querySelectorAll('.requirement-item').forEach(item => {
                const req = item.dataset.requirement;
                if (req === 'length' && lengthCheck) item.classList.add('valid');
                if (req === 'upper' && upperCheck) item.classList.add('valid');
                if (req === 'lower' && lowerCheck) item.classList.add('valid');
                if (req === 'number' && numberCheck) item.classList.add('valid');
                if (req === 'special' && specialCheck) item.classList.add('valid');
            });
            
            // Calculate strength
            if (lengthCheck) strength++;
            if (upperCheck) strength++;
            if (lowerCheck) strength++;
            if (numberCheck) strength++;
            if (specialCheck) strength++;
            
            // Update strength meter
            if (strengthMeter) {
                strengthMeter.className = 'strength-meter-fill';
                if (strength <= 2) {
                    strengthMeter.classList.add('strength-weak');
                } else if (strength <= 4) {
                    strengthMeter.classList.add('strength-medium');
                } else {
                    strengthMeter.classList.add('strength-strong');
                }
            }
        });
    }
    
    // Password match checker
    if (password2) {
        password2.addEventListener('input', function() {
            if (password1.value === password2.value) {
                this.style.borderColor = '#28a745';
                document.getElementById('passwordMatch')?.classList.add('valid');
            } else {
                this.style.borderColor = '#dc3545';
                document.getElementById('passwordMatch')?.classList.remove('valid');
            }
        });
    }
    
    // Form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            const username = document.getElementById('id_username').value;
            const email = document.getElementById('id_email').value;
            const pass1 = password1.value;
            const pass2 = password2.value;
            
            if (!username || !email || !pass1 || !pass2) {
                e.preventDefault();
                alert('Please fill in all fields');
            } else if (pass1 !== pass2) {
                e.preventDefault();
                alert('Passwords do not match');
            }
        });
    }
});
