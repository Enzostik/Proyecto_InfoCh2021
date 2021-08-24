function updateUrl() {
    const usuario = document.getElementById('user').value;
    const orden = document.getElementById('order').value;
    const atributo = document.getElementById('attribute').value;
    const fecha = document.getElementById('date').value;

    window.location.href = window.location.origin + window.location.pathname + `?search=${usuario}&ord=${orden}&atr=${atributo}&met=${fecha}`;
}

document.addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
        updateUrl();
    }
    console.log('ENTER');
});