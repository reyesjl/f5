const NavMenu = (() => {
    const openMenuButton = document.getElementById('toggle-open-menu');
    const closeMenuButton = document.getElementById('toggle-close-menu');
    const navMenu = document.querySelector('.navmenu');

    const toggleMenu = () => {
        navMenu.classList.toggle('open');
    };

    const bindEvents = () => {
        openMenuButton.addEventListener('click', toggleMenu);
        closeMenuButton.addEventListener('click', toggleMenu);
    };

    return {
        init: bindEvents
    };
})();

export default NavMenu;