
$(document).ready(function() {  
    let dato;
        
    $("#imagen1").on("click", function () {
      dato = $('.mi-imagen[data-id="1"]').attr("src");
      //alert(dato);
      $('#imagen').attr('src', dato);    
      $('#image').val(dato);
    });

    $("#imagen2").on("click", function () {
      let dato = $('.mi-imagen[data-id="2"]').attr("src");
      //alert(dato);
      $('#imagen').attr('src', dato);    
      $('#image').val(dato);
    });

    $("#imagen3").on("click", function () {
      let dato = $('.mi-imagen[data-id="3"]').attr("src");
      //alert(dato);
      $('#imagen').attr('src', dato);    
      $('#image').val(dato);
    });

    $("#imagen4").on("click", function () {
      let dato = $('.mi-imagen[data-id="4"]').attr("src");
      //alert(dato);
      $('#imagen').attr('src', dato);    
      $('#image').val(dato);
    });
});
  

