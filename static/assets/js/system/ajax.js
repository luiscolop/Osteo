const modal=$('#modal');
const modalsecond=$('#modalsecond');
function openModal(url){
  modal.load(url, function() {
    $('.selectm2').select2({
      placeholder: 'Seleccione una opción',
      language: 'es'
    });
    $('.selectm2-mark').select2({
      placeholder:'Seleccione una marca',
      minimumInputLength: 1,
      ajax:{
        url:'/mark/select/',
        dataType:'json',
        type:'GET',
        data: function (params) {
          return {
            q: params.term
          };
        },
        processResults: function(data){
          return {
            results: $.map(data,function(item){
              return {id:item.id,text:item.name};
            })
          }
        },
      }
    });
    $('.selectm2-filing').select2({
      placeholder:'Seleccione una presentación',
      minimumInputLength: 1,
      ajax:{
        url:'/filing/select/',
        dataType:'json',
        type:'GET',
        data: function (params) {
          return {
            q: params.term
          };
        },
        processResults: function(data){
          return {
            results: $.map(data,function(item){
              return {id:item.id,text:item.name+' - '+item.category};
            })
          }
        },
      }
    });
    //Bootstrap customfile
    bsCustomFileInput.init();
    $(this).modal({backdrop: 'static', keyboard: false});
    $(this).modal('show');
    $('#image').change(function(){
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result); // Renderizamos la imagen
        }
        reader.readAsDataURL(this.files[0]);
      }
    });
  });
}

function openModalSecond(url){
  modalsecond.load(url, function() {
    $('.selects2').select2({
      placeholder: 'Seleccione una opción',
      language: 'es'
    });
    $(this).modal({backdrop: 'static', keyboard: false});
    $(this).modal('show');
  });
}

function formErrors(obj, action){
  $.each(obj, function(key, value){
    $(`#${key}`).addClass('is-invalid').attr('aria-invalid','true').attr('aria-describedby',`${key}-error`)
    let span=`<span id="${key}-error" class="error invalid-feedback">${value}</span>`
    $(`#${key}`).parent().append(span)
  })
}