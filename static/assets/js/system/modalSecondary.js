$('#formAddAjaxS').on('submit',function(e){
  e.preventDefault();
  let form = $('#formAddAjaxS');
  $.ajax({
    url: form.attr('action'),
    type: form.attr('method'),
    data:  form.serializeArray(),
    dataType: 'json',
  }).done(function(response){
    if(response.state == 'error'){
      $.each(response.message, function(key, value){
        $(`#${key}`).addClass('is-invalid').attr('aria-invalid','true').attr('aria-describedby',`${key}-error`)
        let span=`<span id="${key}-error" class="error invalid-feedback">${value}</span>`
        $(`#${key}`).parent().append(span)
      })
      return false;
    }
    modalsecond.modal('hide');
    Swal.fire({
      title: '¡Éxito!',
      icon: 'success',
      text: response.message,
    });
    loadSelect();
  }).fail(function(jqXHR,textStatus,errorThrown){
    Swal.fire({
      title: '¡Error!',
      icon: 'error',
      text: textStatus+' '+errorThrown,
    });
  });
});