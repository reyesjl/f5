const nav = document.querySelector(".navlist");
const navToggle = document.querySelector(".mobile-nav-toggle");
navToggle.addEventListener('click', () => {
    const visibility = nav.getAttribute("data-visible");
    
    if (visibility === "false") {
        nav.setAttribute("data-visible", true);
        navToggle.setAttribute("aria-expanded", true);
    } else {
        nav.setAttribute("data-visible", false);
        navToggle.setAttribute("aria-expanded", false);
    }
});

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