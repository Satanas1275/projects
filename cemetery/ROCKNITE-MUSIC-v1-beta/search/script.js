document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const resultsContainer = document.getElementById('results');
    const audioPlayer = document.getElementById('audio-player');

    searchBar.addEventListener('input', () => {
        const query = searchBar.value.toLowerCase();
        fetch('musique.json')
            .then(response => response.json())
            .then(data => {
                const results = data.filter(music => 
                    music.titre.toLowerCase().includes(query) || 
                    music.artiste.toLowerCase().includes(query)
                );
                displayResults(results);
            });
    });

    function displayResults(results) {
        resultsContainer.innerHTML = '';
        if (results.length > 0) {
            results.forEach(music => {
                const div = document.createElement('div');
                div.classList.add('result-item');
                div.innerHTML = `
                    <img src="${music.image}" alt="${music.titre}">
                    <div class="result-info">
                        <h4>${music.titre}</h4>
                        <p>${music.artiste}</p>
                    </div>
                    <div class="result-duration">${music.duree}</div>
                `;
                div.addEventListener('click', () => {
                    playMusic(music.fichier);
                });
                resultsContainer.appendChild(div);
            });
        } else {
            resultsContainer.textContent = 'Aucun résultat trouvé';
        }
    }

    function playMusic(filename) {
        audioPlayer.src = `musique/${filename}`;
        audioPlayer.style.display = 'block';
        audioPlayer.play();
    }
});
