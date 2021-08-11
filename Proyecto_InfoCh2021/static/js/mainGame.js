function hideCurrentContainer() {
    const div = document.querySelector('.pregunta');
    div.style.display = 'none';
    console.log('wop');
}

function showCurrentContainer() {
    const div = document.getElementsByClassName('mi-separador');
    div.style.display = 'block';
    console.log('wop');
}

function hide(elements) {
    elements = elements.length ? elements : [elements];
    for (var index = 0; index < elements.length; index++) {
        elements[index].style.display = 'none';
    }
}

function show(elements, specifiedDisplay) {
    elements = elements.length ? elements : [elements];
    for (var index = 0; index < elements.length; index++) {
        elements[index].style.display = specifiedDisplay || 'block';
    }
}

function main() {
    const button = document.querySelectorAll('.next');

    button.addEventListener('click', function(event) {
        console.log('Funciona!');
    })
}

document.querySelector('#prueba').addEventListener('click', hideCurrentContainer);

