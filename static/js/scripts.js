function getQuote() {
    fetch('/get_quote')
        .then(response => response.json())
        .then(data => {
            document.getElementById('quote').innerText = data.quote;
            document.getElementById('author').innerText = data.author ? `- ${data.author}` : '';
        });
}
