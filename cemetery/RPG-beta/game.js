// Recuperer la zone de texte
let zoneDeTexte = document.querySelector('#zoneDeTexte');

// Generer du texte dans la zone de texte
// Creer la fonction pour generer le texte
// La fonction prend le texte a afficher en parametre 
// Etape : 
 // 1. Creer un nouvel élément (p)
 // 2. Ajouter le texte en parametre dans cet element 
 // 3. Afficher l'element dans la zone de texte
function genererTexte(texte) {
    let p = document.createElement('p');
    // <p></p>
    p.textContent = texte
    // <p>notre texte contenu dans le paramtre 'texte'</p>
    zoneDeTexte.appendChild(p)
}

// ---------------- 

// Ajuster barre de vie
// 1. Creer la fonction ajusterVie()
    // -> Parametres : 
        // - classe du personnage a qui on ajuste la vie
        // - Ses points vies actuelles 
        // - Son maximum de point de vie
function ajusterVie(classe, pointsDeVie, pointsDeVieMax){
    // 2. Recuperer l'ID de la bonne barre de vie, cad celle qui correspond au personnage dont on veut ajuste la vie 
        // -> Condition (if else) qui va dependre de la classe du perso 
        // Si on a la classe 'guerrier', alors on recupere l'ID correspondant a sa barre de vie 
    let id;
    if(classe == 'guerrier'){
        id = '#vieGuerrier';
    } else {
        id = '#vieMagicien'
    }
    // 3. Recuperer l'element correspondant a l'ID qu'on vient de recuperer
    let barreDeVie = document.querySelector(id)
    // let barreDeVie = document.querySelector('#vieGuerrier ou #vieMagicien')
    // 4. Modifier sa largeur (width) en fonction de la vie actuelle et maximum 
        // -> (vieActuelle * 100 / vieMaximum) + '%'
    if(pointsDeVie >= 0){
        barreDeVie.style.width = pointsDeVie * 100 / pointsDeVieMax + '%';
    } else {
        barreDeVie.style.width = '0%';
    }
}
// 5. (En dehors de la fonction) - Appeler la fonction dans la methode verifierSante()


function ajusterCharge(classe, energie, energieMax){
    // 2. Recuperer l'ID de la bonne barre de vie, cad celle qui correspond au personnage dont on veut ajuste la vie 
        // -> Condition (if else) qui va dependre de la classe du perso 
        // Si on a la classe 'guerrier', alors on recupere l'ID correspondant a sa barre de vie 
    let id;
    if(classe == 'guerrier'){
        id = '#energieGuerrier';
    } else {
        id = '#energieMagicien'
    } 
    // 3. Recuperer l'element correspondant a l'ID qu'on vient de recuperer

    let barreEnergie = document.querySelector(id)
if(energie < energieMax){
    barreEnergie.style.width = Math.ceil(energie) * 100 / energieMax + '%';

} else {
    barreEnergie.style.width = '100%'
}

if(energie == energieMax && classe == 'guerrier'){
    updateCoupSpecial()
}}

let boutonCoupSpecial = document.querySelector('#btnSpecial')

function updateCoupSpecial(){
    boutonCoupSpecial.classList.toggle('active')
}
// Class Personnage et ses enfants Magicien et Guerrier

class Personnage {
    constructor(pseudo, classe, pointsDeVie, attaque) {
        this.pseudo = pseudo;
        this.classe = classe;
        this.pointsDeVie = pointsDeVie;
        this.pointsDeVieMax = pointsDeVie;
        this.attaque = attaque;
        this.niveau = 1;
        this.energie = 0;
        this.energieMax = 100;
        // Ajouter les attributs energie et energieMax au constructeur
            // initialiser energie a 0 et energie max a 100
        // Creer la methode (fonction dans la classe) charger dans les class Guerrier et Magicien
    }

    
    evoluer() {
        this.niveau = this.niveau + 1;
        genererTexte(this.pseudo + " monte au niveau " + this.niveau)
    }

    
    verifierSante() {
        if (this.pointsDeVie <= 0) {
            genererTexte(this.pseudo + " a perdu...");
            genererTexte("GAME OVER")
        } else {
            genererTexte("Il reste " + this.pointsDeVie + " points de vie à " + this.pseudo);
        }
        ajusterVie(this.classe, this.pointsDeVie, this.pointsDeVieMax)
    }

    
    afficherInformations() {
        genererTexte(this.pseudo + " (" + this.classe + ") a " + this.pointsDeVie + " points de vie restants et est au niveau " + this.niveau)
    }

    coupCritique() {
        let cc = false;
        if((Math.floor(Math.random() * 10) + 1) === 10){
            cc = true;
        }
        return cc;
    }

}


class Magicien extends Personnage{
    constructor(pseudo){
        super(pseudo, "magicien", 300, 70)
    }
 
    attaquer(perso) {
        if(this.coupCritique()) {
            genererTexte("Coup Critique !")
            perso.pointsDeVie -= this.attaque * 3
            genererTexte(this.pseudo + " attaque " + perso.pseudo + " et lui inflige " + this.attaque * 3 + " dégats")
        } else {
            perso.pointsDeVie -= this.attaque
            genererTexte(this.pseudo + " attaque " + perso.pseudo + " et lui inflige " + this.attaque + " dégats")
        }
        perso.verifierSante()
    }

    charger() {
        this.energie += this.energieMax / 2;
        genererTexte(this.pseudo + " accumule de l'energie")
        ajusterCharge(this.classe, this.energie, this.energieMax)
    }

    coupSpecial(perso) {
        perso.pointsDeVie -= this.attaque * 3
        genererTexte(this.pseudo + " utilise son coup spécialle contre " + perso.pseudo + " et lui inflige " + this.attaque * 3 + " dégats")
        perso.verifierSante()
        this.energie = 0;
        ajusterCharge(this.classe, this.energie, this.energieMax)
    }
} 

class Guerrier extends Personnage {
    constructor(pseudo) {
        super(pseudo, "guerrier", 550, 40)
    }

    attaquer(perso){
        if(this.coupCritique()){
            perso.pointsDeVie -= this.attaque * 3
            genererTexte(this.pseudo + " attaque " + perso.pseudo + " et lui inflige " + this.attaque * 3 + " dégats")
        } else {
            perso.pointsDeVie -= this.attaque
            genererTexte(this.pseudo + " attaque " + perso.pseudo + " et lui inflige " + this.attaque + " dégats")
        }
        perso.verifierSante()
    }

    charger() {
        this.energie += this.energieMax / 3;
        genererTexte(this.pseudo + " accumule de l'energie")
        ajusterCharge(this.classe, this.energie, this.energieMax)
    }

    coupSpecial(perso) {
        perso.pointsDeVie -= this.attaque * 3
        genererTexte(this.pseudo + " utilise son coup spécialle contre " + perso.pseudo + " et lui inflige " + this.attaque * 3 + " dégats")
        perso.verifierSante()
        this.energie = 0;
        ajusterCharge(this.classe, this.energie, this.energieMax)
        updateCoupSpecial()
    }
    
}

// ---------------- 

// Jeu
// Creer nos deux personnages 
let joueur = new Guerrier('Pepito')
let bot = new Magicien('Sauron')

function actionBot(){
    let actionAleatoire = Math.ceil(Math.random() * 2)
    if(bot.energie == bot.energieMax){
        bot.coupSpecial(joueur)
    } else {
        switch(actionAleatoire){
            case 1:
                bot.attaquer(joueur)
                break;
    
            case 2:
                bot.charger()
                break;
        }
    }
    
}


// Afficher les informations des deux perso 
// 1. Récuperer le bouton d'informations (verifier l'ID dans l'HTML)
// 2. Ajouter un evenement au click du bouton 
// Dans la fonction qui va se déclencher lors du clique : 
    // A. Effacer le texte de la zone de texte -> "";
    // B. On utilise la méthode afficherInformations() pour chaque personnage

// 1. Récuperation du bouton infos
let btnInfos = document.querySelector("#btnInfos");

// 2. On ajoute l'evenement click sur notre bouton
btnInfos.addEventListener('click', function(){
    // A. Effacer le texte de la zone de texte -> Le redéfinir pour ""
    zoneDeTexte.textContent = ""
    // B. On utilise la méthode afficherInformations() pour chaque personnage
    joueur.afficherInformations()
    bot.afficherInformations()
})


// Attaquer 
// 1. Recuperer le bouton d'attaque (verifier l'ID dans l'HTML)
let btnAttaque = document.querySelector("#btnAttaque");
// 2. Ajouter un evenement au click du bouton
btnAttaque.addEventListener('click', function() {
// Dans l'evenement : 
    // A. Effacer le texte de la zone de texte -> "";
    zoneDeTexte.textContent = ""
    // B. Utiliser la méthode (fonction dans une class) attaquer du joueur contre le bot, puis du bot contre le joueur
    joueur.attaquer(bot)
    actionBot()
})

let boutonCharge = document.getElementById('btnEnergie');

boutonCharge.addEventListener('click', function() {
    zoneDeTexte.textContent = "";

    joueur.charger()
    actionBot()
})

boutonCoupSpecial.addEventListener('click', function(){
    zoneDeTexte.textContent = ""
    joueur.coupSpecial(bot);
    actionBot()
})