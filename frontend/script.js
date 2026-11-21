// This script calls to a Web API to generate a new game URL and renders it in the HTML page
const baseApiUrl = 'http://127.0.0.1:8000/fraseMaleida/v1';
document.getElementById('generate-btn').addEventListener('click', async () => {
    const phrase = document.getElementById('phrase-input').value;
    const output = document.getElementById('game-url');
    try {
        const response = await fetch(`${baseApiUrl}/generate-game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ phrase })
        });
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        const data = await response.json();
        output.textContent = data.url;
    } catch (error) {
        console.error('Failed to generate game:', error);
        output.textContent = 'Could not generate the game. Please check the server and try again.';
    }
});
