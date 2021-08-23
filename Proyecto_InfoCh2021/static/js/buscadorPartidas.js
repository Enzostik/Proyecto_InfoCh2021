function updateUrl() {
    const usuario = document.getElementById('user').value;
    const orden = document.getElementById('order').value;
    const fecha = document.getElementById('date').value;

    var url = window.location.href;
    var searchParams = url.searchParams;

    if (searchParams !== null) {
        console.log('NULL');
        window.location.href = window.location.href + `?search=${usuario}&ord=${orden}&met=${fecha}`;
    } else {
        searchParams.set('search', usuario);
        searchParams.set('ord', orden);
        searchParams.set('met', fecha);

        var new_url = url.toString();
        window.location.href = new_url;
    }
}
