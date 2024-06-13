const scroller = document.querySelector(".media-scroller");
const scrollLeftButton = document.getElementById("scroll-left");
const scrollRightButton = document.getElementById("scroll-right");

const scrollAmount = 170;

scrollLeftButton.addEventListener("click", function() {
    scroller.scrollBy({
        left: -scrollAmount,
        behavior: "smooth"
    });
});

scrollRightButton.addEventListener("click", function() {
    scroller.scrollBy({
        left: scrollAmount,
        behavior: "smooth"
    });
});