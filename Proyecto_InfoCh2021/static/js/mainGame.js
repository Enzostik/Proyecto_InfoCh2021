function hideButton(btn) {
    const submit = document.querySelector(btn);
    submit.style.display = 'none';
    console.log('hide Submit');
}

function showButton(btn) {
    const submit = document.querySelector(btn);
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



function main() {
    let num = 1;
    // Variable que controla el número de preguntas
    const params = new URLSearchParams(location.search);
    console.log('LEVEL: ', params.get('level'));
    let questions = 5 + Number(params.get('level'));
    const btnsNext = document.querySelectorAll('.next');
    const btnsPrev = document.querySelectorAll('.prev');
    const btnPrevi = document.querySelector('.previous');
    // Oculta los botones
    hide(document.querySelectorAll('.pregunta'));
    hideButton('.final');
    hideButton('.prev');
    showCurrentContainer(num);

    // Botón para ir a la siguiente pregunta
    btnsNext.forEach(btnNext => {
        btnNext.addEventListener('click', function () {
            hide(document.querySelectorAll('.pregunta'));
            num++;
            console.log(num);
            if (num <= questions) {
                showCurrentContainer(num);
            } else {
                // Final del cuestionario
                showButton('.final');
            };
        });
    });

    // Botón para ir a la anterior pregunta durante el cuestionario
    btnsPrev.forEach(btnPrev => {
        btnPrev.addEventListener('click', function() {
            hide(document.querySelectorAll('.pregunta'));
            num--;
            showCurrentContainer(num);
            console.log('show previous');
        });
    });
    // Botón para retroceder una vez alcanzado el final
    btnPrevi.addEventListener('click', function() {
        hideButton('.final');
        hide(document.querySelectorAll('.pregunta'));
        num--;
        showCurrentContainer(num);
        console.log('show previous');
        console.log(num);
    });
};

main();

