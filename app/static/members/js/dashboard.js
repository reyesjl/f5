function openTab(tabName, element) {
    // Hide all elements with class="actions"
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("actions");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove the active class from all tablinks
    tablinks = document.getElementsByClassName("action-item");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    // Show the specific tab content and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    element.classList.add("active");
}

// Optionally, you can set a default open tab
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('.action-item').click(); // Default open tab
});