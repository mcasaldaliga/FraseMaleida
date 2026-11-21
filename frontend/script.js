// This script calls to a Web API to generate a new game URL and renders it in the HTML page
const baseApiUrl = 'http://localhost:3000/fraseMaleida/v1';
document.getElementById('generate-btn').addEventListener('click', async () => {
    const phrase = document.getElementById('phrase-input').value;
    const response = await fetch(`${baseApiUrl}/generate-game`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ phrase })
    });
    const data = await response.json();
    document.getElementById('game-url').textContent = data.url;
});

