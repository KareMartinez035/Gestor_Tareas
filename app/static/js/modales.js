$(document).ready(function()
{
    $("boton-actualizar", "Actualizar").click(function()
{

cargaus.load("templates/Modalusuarios");
cargamodal.load("templates/Modaltareas.html");

});

function cargaus(){
    $("Musuarios").load(ruta,function(){
        $("Musuarios").modal("show")
    });
};
function cargamodal(){
    $("#Mtareas").load(ruta,function(){
        $("Mtareas").modal("show")

    });
};

});

