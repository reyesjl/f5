// Get all elements with class "image"
var images = document.querySelectorAll('.image');

// Loop through each image element
images.forEach(function(image) {
    // Remove margin
    image.style.margin = '0';
});