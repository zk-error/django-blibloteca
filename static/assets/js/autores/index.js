//funcion para listar autores mediante ajax
function listadoUsuarios(){
    $.ajax({
        url: "/libro/listado_autor/", //la ruta que vamos a usar osea donde se encuentra el listado no podemos poner la ruta con el nombre de django tenemos que poner la ruta litelamente
        type:"get", // que tipo de peticion usaremos
        dataType: "json", //le decimos con que formato queremos trabajar 
        success: function(response){//aque decimos con success que si la respuesta que recibimos del servidor es correcta que va a pasar 
            
            //funcion directa del datatable que nos dice que si existe una instancia de ese data table simplemente destruyela
            if ($.fn.DataTable.isDataTable('#tabla_autores')) {
                $('#tabla_autores').DataTable().destroy();
            }

            //parte para agregar los datos a la tabla
            $('#tabla_autores tbody').html("");
            for(let i = 0;i < response.length;i++){
                let fila = '<tr>';
                fila += '<td>' + (i +1 ) + '</td>';
                fila += '<td>' + response[i]["fields"]['nombre'] + '</td>';
                fila += '<td>' + response[i]["fields"]['apellidos'] + '</td>';
                fila += '<td>' + response[i]["fields"]['nacionalidad'] + '</td>';
                fila += '<td>' + response[i]["fields"]['descripcion'] + '</td>';
             
                fila += '<td><button type = "button" class = "btn btn-primary btn-sm tableButton"';
                fila += ' onclick = "abrir_modal_edicion(\'/libro/editar_autor/' + response[i]['pk'] + '/\');"> EDITAR </button>';
                fila += '<button type = "button" class = "btn btn-danger tableButton  btn-sm" ';
                fila += 'onclick = "abrir_modal_eliminacion(\'/libro/eliminar_autor/' + response[i]['pk'] + '/\');"> ELIMINAR </buttton></td>'

                fila += '</tr>';
                $('#tabla_autores tbody').append(fila);
            }
            //parte para agregar los datos a la tabla

           //parte para traducir el data table
            $('#tabla_autores').DataTable({
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando START a END de TOTAL Entradas",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de MAX total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar MENU Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                      first: "Primero",
                      last: "Ultimo",
                      next: "Siguiente",
                      previous: "Anterior",
                    },
                  },
          
            });
            //parte para traducir el data table

        },


        error: function(error){
            console.log(error);
        }
    });
}




function registrar() {
    //activarBoton();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response) {
            //para poner un pop up de que todo salio bien 
             notificacionSuccess(response.mensaje);
			//si sale todo correto llama a al funcion listado para qu linte la tabla sin tener que recargar la pagina
            
            listadoUsuarios();

			// y que despues se cierre el formulario
            cerrar_modal_creacion();
		
        },
        error: function (error) {
             notificacionError(error.responseJSON.mensaje);
             mostrarErroresCreacion(error);
             //por si tenemos un error que el boton nos de otra chanse si no se va a bloquear
             activarBoton();
			
        }
    });
}





function editar() {
    activarBoton();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoUsuarios();
            cerrar_modal_edicion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBoton();
        }
    });
}


function eliminar(pk) {
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/libro/eliminar_autor/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listadoUsuarios();
            cerrar_modal_eliminacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
        }
    });
}

$(document).ready(function(){
    listadoUsuarios();
});



// $(document).ready(function () {
//     //listadoAutores();
//     $('#tabla_autores').DataTable({
//         "serverSide": true,
//         "processing": true,
//         "ajax": function(data,callback,settings){
//             var columna_filtro = data.columns[data.order[0].column].data.replace(/\./g,"__");
            
//             $.get('/libro/listado_autor/',{
//                 limite: data.length,
//                 inicio: data.start,
//                 filtro: data.search.value,
//                 order_by: columna_filtro
//             }, function(res){
//                     callback({
//                         recordsTotal:res.length,
//                         recordsFiltered:res.length,
//                         data:res.objects
//                     });
//                 },
//             );
//         },
//         "columns":[
//             { "data": "id" },
//             { "data": "nombre" },
//             { "data": "apellidos" },
//             { "data": "nacionalidad" },
//             { "data": "descripcion" },
//         ]
//     });
// });