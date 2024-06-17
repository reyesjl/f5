// Get references to the elements
const toggleMenu = document.getElementById('togglemenu');
const sideMenu = document.querySelector('.sidemenu');
const closeBtn = document.querySelector('.closebutton');

function toggleSideMenu() {
    sideMenu.classList.toggle('open');
}

toggleMenu.addEventListener('click', toggleSideMenu);
closeBtn.addEventListener('click', toggleSideMenu);

/** Notification component */
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