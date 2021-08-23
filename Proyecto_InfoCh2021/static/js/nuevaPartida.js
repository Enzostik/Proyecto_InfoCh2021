function changeValue() {
    const rangeValue = document.getElementById('RangeNivel').value;
    var preguntas = document.getElementById('preguntas');

    console.log(Number(rangeValue)+ 5);
    preguntas.textContent = `${Number(rangeValue)+ 5}`;
}