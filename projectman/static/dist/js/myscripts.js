// $(document).ready(function () {
//Evitar varios Submit/envios de formularios
$("button[type=submit]").click(function (e) {
    // var icono = '<i class="fa fa-spinner fa-spin"></i> ';
    var valor = $(this).text();
    var puntos = '...';
    $(this).addClass(" noevent");
    $(this).html(valor + puntos);
    // $(this).html(icono+valor);
    // e.preventDefault();
});

var activar_clase = function () {
    var url = window.location;
    var element = $("ul.nav a").filter(function () {
        return this.href == url;
    });
    if (element) {
        var p = "li:has(a[href='" + url.pathname + "'])";
        $(p).addClass('active treeview');
    }
};
activar_clase();
// $(".sidebar").click(function (e) {
//     activar_clase();
// });

// Limpiar los formularios al salir de un modal
$('.modal:has(input)').on('hidden.bs.modal', function () {
    $(this).find('form')[0].reset(); //para borrar todos los datos que tenga los input, textareas, select.
});

origin = window.location.origin;
url_dataTable = origin + "/static/plugins/datatables/spanish.json";
$('.datatable-active').DataTable({
    responsive: true,
    language: {
        "url": url_dataTable
    }
});

$('.datatable-active-small').DataTable({
    responsive: true,
    language: {
        "url": url_dataTable
    },
    "displayLength": 1,
    "lengthMenu": [1, 3, 5, 10, 15],
    ordering: false
});

addCommentapi = function (task_id) {
    $('#modal-comment-api').modal('toggle');
    console.log(task_id);
    getTaskById(task_id).then(function (resp) {
        $('#task_title').text(resp.name)
        $('#task_id_add_comment_form').val('http://localhost:8000/api/task/' + resp.id + '/');
    });

    //Ajax-
    $("#btn_agregar_comment_modal").unbind('click').click(function (event) {
        console.log(event);
        event.preventDefault();
        let data = $("#add_comment_api_form").serialize()
        console.log(data)
        $.ajax({
            type: "POST",
            url: '/api/comment/',
            data: data,
            success: function (response) {
                $('#modal-comment-api').modal('hide');
                console.log(response)
                $.notify({message: 'comentario agregado con exito'},
                    {
                        type: 'success',
                        timer: 2500,
                        placement: {
                            from: 'top',
                            align: 'right'
                        }
                    }
                );
                // if (table_id) {
                //     if (table_id === 'tabla') {
                //         location.reload();
                //     } else {
                //         const urlHref = location.href + " #" + table_id + ">*";
                //         $("#" + table_id).load(urlHref, function () {
                //             if ($('#' + table_id).dataTable() != null) {
                //                 $('#' + table_id).dataTable().fnDestroy();
                //             }
                //             $('#' + table_id).DataTable({
                //                 responsive: true,
                //                 language: {
                //                     "url": url_dataTable
                //                 }
                //             });
                //         });
                //     }
                //     // Notificacion
                //     $.notify({message: message + ' fue eliminada con éxito'},
                //         {
                //             type: 'success',
                //             timer: 2500,
                //             placement: {
                //                 from: 'top',
                //                 align: 'right'
                //             }
                //         }
                //     );
                // }
            },
            error: function (response) {
                console.error(response);
                $.notify({message: response},
                    {
                        type: 'error',
                        timer: 2500,
                        placement: {
                            from: 'top',
                            align: 'right'
                        }
                    }
                );
                $('#modal-comment-api').modal('toggle');
            }
        });
    });

}


deleteModalForm = function (url, message, table_id = null, name = '', event) {
    console.log(event);
    $("#form-eliminar").attr("action", url);
    $("#span-ms").html(message + " <strong>" + name + "</strong>");
    $('#modal-eliminar').modal('toggle');

    //Ajax-
    $("#btn_eliminar_modal").unbind('click').click(function (event) {
        console.log(event);
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: url,
            data: $("#form-eliminar").serialize(),
            success: function (response) {
                $('#modal-eliminar').modal('hide');
                if (table_id) {
                    if (table_id === 'tabla') {
                        location.reload();
                    } else {
                        const urlHref = location.href + " #" + table_id + ">*";
                        $("#" + table_id).load(urlHref, function () {
                            if ($('#' + table_id).dataTable() != null) {
                                $('#' + table_id).dataTable().fnDestroy();
                            }
                            $('#' + table_id).DataTable({
                                responsive: true,
                                language: {
                                    "url": url_dataTable
                                }
                            });
                        });
                    }
                    // Notificacion
                    $.notify({message: message + ' fue eliminada con éxito'},
                        {
                            type: 'success',
                            timer: 2500,
                            placement: {
                                from: 'top',
                                align: 'right'
                            }
                        }
                    );
                }
            },
            error: function (response) {
                console.error(response);
                $('#modal-eliminar').modal('toggle');
            }
        });
    });
};

// });

function getTaskById(id) {
    return $.ajax({
        type: "GET",
        url: '/api/task/' + id + '/'
    });
}