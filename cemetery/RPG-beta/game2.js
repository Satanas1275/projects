
// Generer du texte dans la zone de texte
let zoneDeTexte = document.querySelector('#zoneDeTexte')

function genererTexte(texte) {
    let p = document.createElement('p')
    p.textContent = texte
    zoneDeTexte.appendChild(p)
}

// ---------------- 

// Ajuster barre de vie
let barreDeVie = document.querySelector('viePerso2')

function ajuterVie(classe, pointsDeVie, pointsDeVieMax){
    let id;
    if(classe == 'guerrier'){
        id = '#vieGuerrier';
    } else {
        id = '#vieMagicien'
    }
    let barreDeVie = document.querySelector(id)

    if(pointsDeVie >= 0){
    barreDeVie.style.width = pointsDeVie * 100 / pointsDeVieMax + '%';
    } else {
        barreDeVie.style.width = '0%'
    }
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
        ajuterVie(this.classe, this.pointsDeVie, this.pointsDeVieMax)
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
    charge(){
        this.energie += this.energieMax / 3;
        genererTexte(this.pseudo + " accumule de l'energie")
    }
    
}


class Magicien extends Personnage {
    constructor(pseudo) {
        super(pseudo, "magicien", 300, 70);
    }

    // Méthode pour contrer-attaquer le joueur
    contreAttaquer(perso) {
        let degats = this.attaque; // Calcul des dégâts aléatoires
        perso.pointsDeVie -= degats; // Réduire les points de vie du joueur
        genererTexte(this.pseudo + " contre-attaque " + perso.pseudo + " et lui inflige " + degats + " dégâts");
        perso.verifierSante(); // Vérifier la santé du joueur
    }

    // Méthode pour attaquer le joueur
    attaquer(perso) {
        if (this.coupCritique()) {
            genererTexte("Coup Critique !");
            perso.pointsDeVie -= this.attaque * 3;
            genererTexte(this.pseudo + " attaque " + perso.pseudo + " et lui inflige " + this.attaque * 3 + " dégâts");
        } else {
            perso.pointsDeVie -= this.attaque;
            genererTexte(this.pseudo + " attaque " + perso.pseudo + " et lui inflige " + this.attaque + " dégâts");
        }
        perso.verifierSante();

        // Le bot contre-attaque après avoir été attaqué par le joueur
        this.contreAttaquer(perso);
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
}



// ---------------- 

// Jeu

// Creer nos deux personnages
let joueur = new Guerrier('Pepito')
let bot = new Magicien('Sauron')


// 1. Récupérer le bouton d'attaque
let boutonAttaque = document.getElementById('btnAttaque');

// 2. Ajouter un événement au clic sur le bouton
boutonAttaque.addEventListener('click', function() {
    // A. Effacer le texte de la zone de texte
    zoneDeTexte.textContent = "";
    
    // B. Utiliser la méthode (fonction dans une classe) attaquer du joueur contre le bot
    joueur.attaquer(bot);
    bot.contreAttaquer(joueur);
    
});


let boutonInfo = document.getElementById('btnInfos');

boutonInfo.addEventListener('click', function() {
    zoneDeTexte.textContent = "";

    joueur.afficherInformations()
    bot.afficherInformations()
    
})

let boutonCharge = document.getElementById('btnCharge');

boutonCharge.addEventListener('click', function() {
    zoneDeTexte.textContent = "";
    
})




// let specialCharge = 0;

// boutonSpecial.addEventListener('click', function() {
//     if (specialCharge === 0) {
//         // Charger le coup spécial
//         zoneDeTexte.textContent = "Guerrier charge sa capacité spéciale !";
//         boutonSpecial.textContent = "Charger";
//         specialCharge = 1;
//     } else if (specialCharge === 1) {
//         // Utiliser le coup spécial
//         zoneDeTexte.textContent = "Guerrier charge sa capacité spéciale !";
//         boutonSpecial.textContent = "Coup spécial";
//         specialCharge = 2;
//     } else {
//         zoneDeTexte.textContent = "Guerrier utilise capacité spéciale !";
//         boutonSpecial.textContent = "Charger";
//         // Réinitialiser le compteur après avoir utilisé le coup spécial deux fois
//         specialCharge = 0;
//     }

// });