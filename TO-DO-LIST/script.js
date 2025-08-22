document.addEventListener('DOMContentLoaded', function () {
    const formulaire = document.getElementById('formulaire');
    const zoneAFaire = document.getElementById('zoneAFaire');
    const zoneEnCours = document.getElementById('zoneEnCours');
    const zoneTermine = document.getElementById('zoneTermine');

    // Fonction pour sauvegarder les tâches dans le stockage local
    function sauvegarderTaches() {
        const taches = [];
        document.querySelectorAll('.tache').forEach(function (tache) {
            taches.push({
                intitule: tache.querySelector('.intitule').textContent,
                statut: tache.querySelector('.statut').value
            });
        });
        localStorage.setItem('taches', JSON.stringify(taches));
    }

    // Fonction pour charger les tâches depuis le stockage local
    function chargerTaches() {
        const taches = JSON.parse(localStorage.getItem('taches')) || [];
        taches.forEach(function (tache) {
            ajouterTache(tache.intitule, tache.statut);
        });
    }

    // Fonction pour ajouter une tâche avec les écouteurs d'événements appropriés
    function ajouterTache(intitule, statut = 'afaire') {
        const nouveauTemplate = document.getElementById('template').cloneNode(true);
        nouveauTemplate.style.display = 'block';
        nouveauTemplate.querySelector('.intitule').textContent = intitule;
        nouveauTemplate.querySelector('.statut').value = statut;

        // Attacher les écouteurs d'événements au modèle cloné
        nouveauTemplate.querySelector('.statut').addEventListener('change', sauvegarderTaches);
        nouveauTemplate.querySelector('.btnSupprimer').addEventListener('click', function () {
            nouveauTemplate.remove();
            sauvegarderTaches();
        });

        if (statut === 'afaire') {
            zoneAFaire.appendChild(nouveauTemplate);
        } else if (statut === 'encours') {
            zoneEnCours.appendChild(nouveauTemplate);
        } else {
            zoneTermine.appendChild(nouveauTemplate);
        }

        sauvegarderTaches();
    }

    // Charger les tâches au chargement de la page
    chargerTaches();

    formulaire.addEventListener('submit', function (event) {
        event.preventDefault(); // Empêcher le formulaire de se soumettre normalement

        const nouvelleTache = formulaire.elements.tache.value.trim(); // Récupérer la valeur saisie dans le champ

        if (nouvelleTache !== '') {
            ajouterTache(nouvelleTache);
            formulaire.reset();
        }
    });
});
