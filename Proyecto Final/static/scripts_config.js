var config = function () {
    var correoDestinatario = document.getElementById("correoDestinatario").value;
    var correoRemitente = document.getElementById("correoRemitente").value;
    var password = document.getElementById("password").value;

    $.ajax({
      url: '/cambiarFormulario',
      dataType: 'json',
      data: { "correoDestinatario": correoDestinatario, "correoRemitente" : correoRemitente, "password":password} ,
      success: function (data) {
      }
    });  
  
    
  
  }