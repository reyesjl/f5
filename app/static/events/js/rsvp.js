
function showToken() {
    var hiddenTextElement = document.querySelector('.hiddentext');
    var button = document.querySelector('#toggleTokenButton');
    if (hiddenTextElement.textContent === '*********************') {
        hiddenTextElement.textContent = hiddenTextElement.getAttribute('data');
        button.textContent = 'Hide My Token';
    } else {
        hiddenTextElement.textContent = '*********************';
        button.textContent = 'Show My Token';
    }
}

function copyToClipboard() {
    var hiddenTextElement = document.querySelector('.hiddentext');
    var token = hiddenTextElement.getAttribute('data');
    var url = window.location.origin + '/events/rsvp/' + token + '/receipt/';

    // Create a temporary input element to copy the URL
    var tempInput = document.createElement('input');
    tempInput.value = url;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    // Optional: Provide feedback to the user
    alert('Token link copied to clipboard!');
}