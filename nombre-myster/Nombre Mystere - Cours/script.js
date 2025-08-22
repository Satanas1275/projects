
// Recuperation des elements
let formulaire = document.querySelector('#formulaire')
let input = document.querySelector('input')
let button = document.querySelector('button')
let evolution = document.querySelector('.evolution')
// Generation du nombre aléatoire
let nombreAleatoire = Math.floor(Math.random() * 1000)
let tentative = 0;
console.log (nombreAleatoire)
// Créer l'evenement du formulaire (submit)
formulaire.addEventListener('submit', function(event) {
    event.preventDefault()
    tentative++;

// Recuperer ce qu'a envoyer l'utilisateur]
let nombreChoisi = input.value;
// Créer une nouvelle balise qu'on ajoutera ensuite dans l'HTML
let newElement = document.createElement('div')

newElement.classList.add('reponse')
// Comparer le nombre de l'utilisateur avec le nombre aléatoire
// Modifier le nouvel élément en fonction de la réponse

if (nombreChoisi > nombreAleatoire) {
    newElement.textContent = "#" + tentative + " C'est moins ! (" + nombreChoisi + ")"
    newElement.classList.add ('moins')
} else if (nombreChoisi < nombreAleatoire) {
    newElement.textContent = "#" + tentative + " C'est plus ! (" + nombreChoisi + ")"
    newElement.classList.add ('plus')
} else {
    newElement.textContent = "#" + tentative + " C'est gagné ! (" + nombreChoisi + ")"
    newElement.classList.add ('gagne')
}

console.log("nombre de tentative = " + tentative)

// Ajout du nouvel élément dans l'HTML, dans la balise <div class="evolution"></div>
evolution.prepend(newElement);
evolution.prepend(tentative);
})