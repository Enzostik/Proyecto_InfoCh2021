function updateUrl() {
    const usuario = document.getElementById('user').value;
    const orden = document.getElementById('order').value;
    const fecha = document.getElementById('date').value;

    window.location.href = window.location.origin + window.location.pathname + `?search=${usuario}&ord=${orden}&met=${fecha}`;

}
