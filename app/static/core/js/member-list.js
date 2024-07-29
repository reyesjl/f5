// Remove flip class from all images on initial load
const allImages = document.querySelectorAll('.member-avatar img');
allImages.forEach(img => img.classList.remove('flip'));

const links = document.querySelectorAll('.member-link');
let currentAnimatedImage = null;

links.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent immediate navigation

        const img = this.querySelector('img');

        // Remove the flip class from the previously animated image
        if (currentAnimatedImage && currentAnimatedImage !== img) {
            currentAnimatedImage.classList.remove('flip');
        }

        // Apply the flip animation to the current image
        img.classList.add('flip');
        currentAnimatedImage = img;

        // Delay navigation to allow the animation to complete
        setTimeout(() => {
            window.location.href = this.href;
        }, 600); // Matches the duration of the CSS transition
    });
});