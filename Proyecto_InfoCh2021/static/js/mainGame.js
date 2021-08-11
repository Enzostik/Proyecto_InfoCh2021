function hideSubmit() {
    const submit = document.querySelector('.btn-success');
    submit.style.display = 'none';
    console.log('hide Submit');
}

function showSubmit() {
    const submit = document.querySelector('.btn-success');
    submit.style.display = 'block';
    console.log('show Submit');
}

function showCurrentContainer(number) {
    const div = document.getElementById(`${number}`);
    div.style.display = 'block';
    console.log(`Display num: ${number}`);
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
    let num = 0;
    // Variable que controla el número de preguntas
    let questions = 4;
    const btns = document.querySelectorAll('.next');

    hide(document.querySelectorAll('.pregunta'));
    hideSubmit();
    showCurrentContainer(num);

    btns.forEach(btn => {
        btn.addEventListener('click', function () {
            hide(document.querySelectorAll('.pregunta'));
            num++;
            if (num <= questions) {
                showCurrentContainer(num);
            } else {
                showSubmit();
                console.log('Terminado');
            }
        });
    })
}

main();

