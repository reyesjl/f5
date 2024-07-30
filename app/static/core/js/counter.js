function calculateInitialViews() {
    const baseViews = 10; // The base number of views at startHour

    const now = new Date();
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
    const elapsedSeconds = Math.floor((now - startOfDay) / 4000);

    // Increase the base views proportionally to the seconds passed since startHour
    return baseViews + Math.floor(elapsedSeconds / 10); // Adjust the divisor for rate of increase
}

function formatViews(views) {
    if (views < 1000) {
        return views.toString();
    } else if (views < 1000000) {
        return (views / 1000).toFixed(1) + 'k';
    } else {
        return (views / 1000000).toFixed(1) + 'M';
    }
}

function updateViews() {
    const viewElement = document.getElementById('live-views');
    let views = parseInt(viewElement.textContent);

    // Increment views by a random number between 1 and 3
    views += Math.floor(Math.random() * 3) + 1;
    viewElement.textContent = views;
}

window.onload = function() {
    const initialViews = calculateInitialViews();
    const viewElement = document.getElementById('live-views');
    viewElement.textContent = initialViews;
    // viewElement.textContent = formatViews(initialViews);

    // Update views every 30 seconds
    setInterval(updateViews, 10000);
};