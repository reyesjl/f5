const alerts = document.querySelectorAll('.alert');
const dismissButtons = document.querySelectorAll('.alertdismiss');
dismissButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const alert = e.target.closest('.alert');
        alert.classList.add('fade-out');
        alert.addEventListener('animationend', () => {
            alert.remove();
        });
    });
});