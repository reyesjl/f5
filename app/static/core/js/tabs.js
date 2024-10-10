document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const targetContent = button.getAttribute('data-content');
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        button.classList.add('active');
        document.getElementById(targetContent).classList.add('active');
    });
});