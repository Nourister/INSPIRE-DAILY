function toggleMenu() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('active');
}

function getQuote() {
    fetch('/get_quote')
        .then(response => response.json())
        .then(data => {
            document.getElementById('quote').innerText = data.quote;
            document.getElementById('author').innerText = data.author ? `- ${data.author}` : '';
        });
}

// Function to handle automatic dismissal of alerts after a specified time
function dismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(function() {
            alert.remove();
        }, 3000); // Adjust timeout value as needed
    });
}

// Call dismissAlerts function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', dismissAlerts);