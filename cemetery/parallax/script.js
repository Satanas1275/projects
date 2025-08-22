let montagne = document.querySelector('#montagne');
let titre = document.querySelector('#titre')

window.addEventListener('scroll', function(){
    let value = window.scrollY;

    montagne.style.top = value * 0.5 + 'px';
    titre.style.top = value * 0.9 + 'px';
})

let centerX = titre.offsetLeft + titre.offsetWidth / 2;
let centerY = titre.offsetTop + titre.offsetHeight / 2;

console.log(centerX, centerY)

let invertionX = false;
let invertionY = false;
let pourcentageX, pourcentageY
let translateValeurX, translateY
window.addEventListener('mousemove', function(e){
    if(e.clientX > centerX ){
        invertionX = true;
    }

    if(e.clientY > centerY ){
        invertionY = true;
    }
    
    if(invertionX === false ){
        pourcentageX = centerX * 100 / e.clientX;
    } else {
        pourcentageX = e.clientX * 100 / centerX
    }

    if(invertionY === false ){
        pourcentageY = centerY * 100 / e.clientY;
    } else {
        pourcentageY = e.clientY * 100 / centerY
    }


    //console.log(e.clientX, e.clientY);
    if(invertionX === false){
        translateValeurX = (100 - pourcentageX) * -1;
    } else {
        translateValeurX = 100 - pourcentageX;
    }

    if(invertionY === false){
        translateValeurY = (100 - pourcentageY) * -1;
    } else {
        translateValeurY = 100 - pourcentageY;
    }

    decoration.style.transform = `scale(1.25) translateX(${translateValeurX/10}%) translateY(${translateValeurY/10}%)`
})