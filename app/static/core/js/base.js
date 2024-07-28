function copyToClipboard() {
    const url = window.location.href;
    const shareData = {
        title: 'Check out this profile!',
        text: 'I found this profile interesting. Check it out!',
        url: url,
    };

    if (navigator.share) {
        navigator.share(shareData)
            .then(() => console.log('Thanks for sharing!'))
            .catch((error) => console.error('Error sharing:', error));
    } else {
        // Create a temporary input element
        const tempInput = document.createElement("input");
        tempInput.value = url;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand("copy");
        document.body.removeChild(tempInput);

        // Optional: Alert the user that the link has been copied
        alert("Profile link copied to clipboard!");
    }
}