document.addEventListener('DOMContentLoaded', () => {
    const analyzeButton = document.getElementById('analyze-button');
    const messageInput = document.getElementById('message-input');
    const scoreDisplay = document.getElementById('score');

    analyzeButton.addEventListener('click', () => {
        const text = messageInput.value;

        if (text) {
            fetch('/chatapp/get_sentiment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is sent
                },
                body: `text=${encodeURIComponent(text)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.score !== undefined) {
                    scoreDisplay.textContent = data.score.toFixed(2);
                } else {
                    scoreDisplay.textContent = 'Error: Unable to analyze sentiment.';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            alert('Please enter some text!');
        }
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
