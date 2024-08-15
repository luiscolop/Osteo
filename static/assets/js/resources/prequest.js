$(function(){
  
});

const dtMaterial=$('#det_material').DataTable({
  "paging": false,
  "searching": false,
  "info": false,
  "scrollCollapse": true,
  "scrollY": '40vh',
  "sort": false,
  rowCallback(row, data, displayNum, displayIndex, dataIndex) {
    $('td:eq(0)', row).attr('style','text-align:center;');
  }
});

var selectHouse = $('#house'); 

const btnValidatePrequest = $('#btn-validate-prequest');

$('.lst-material').autocomplete({
  autoFocus: true,
  classes: {
    "ui-autocomplete": "highlight"
  },
  source: function (request, response){
    $.ajax({
      url:'/material/select/',
      type:'GET',
      data: {
        action: 'search',
        q: request.term
      },
      dataType:'json',
    }).done(function(data){
      let results = [];
      data.forEach(element => {
        if(element.type == 'stock'){
          row = {
            'value':`${element.code} - ${element.name} - ${element.description}`,
            'label':`${element.code} - ${element.name} // STOCK: ${element.stock} / CASA MÉDICA: ${element.mhouse}`,
            'mhouse': element.house,
            'type': element.type,
            'id': element.id
          };
          results.push(row);
        }else{
          row = {
            'value':`${element.code} - ${element.name} - ${element.description}`,
            'label': element.code+' - '+element.name+' - '+element.description,
            'type': element.type,
            'id': element.id
          };
          results.push(row);
        }
      });
      response(results);
    });
  },
  minLength: 1,
  select: function(event, ui){
    event.preventDefault();
    addItemToDetail(ui.item.id,ui.item.type);
    $(this).autocomplete('close');
    $(this).val('');
  }
});

function addItemToDetail(id,type){
  $.ajax({
    url : '/material/select/',
    type : 'GET',
    data : {
      'action' : 'select',
      'type' : type,
      'id' : id
    },
    dataType: 'json',
    success : function(data){
      let validate = searchItemToDetail(data[0].id)
      if(validate){
        Swal.fire({
          title:'¡Advertencia!',
          text: 'El material seleccionado ya se ecuentra en el detalle',
          icon:'warning'
        });
        return false;
      }else{
        if(type=='stock'){
          dtMaterial.row.add({
            'DT_RowId':data[0].id,
            '0':'<button class="btn btn-danger deleteItem" title="Eliminar"> <i class="fas fa-times"></i> </button>',
            '1':`<input type="hidden" id="material_name" value="${data[0].code} // ${data[0].name} - ${data[0].description}"><input type="hidden" id="house_id" name="house_id[]" value="${data[0].house}"/><input type="hidden" name="lot_id[]" id="lot_id" value="${data[0].id}">`+data[0].code+' // '+data[0].name+' - '+data[0].description,
            '2':'<input type="number" style="text-align: center;" class="form-control" name="amount[]" id="amount" value="1">',
          }).draw();
          selectHouse.val(data[0].house).change();
          selectHouse.prop('disabled',true);
          $('.lst-material').prop('disabled',true);
        }else{
          dtMaterial.row.add({
            'DT_RowId':data[0].id,
            '0':'<button class="btn btn-danger deleteItem" title="Eliminar"> <i class="fas fa-times"></i> </button>',
            '1':`<input type="hidden" id="material_name" value="${data[0].code} // ${data[0].name} - ${data[0].description}"><input type="hidden" name="material_id[]" id="material_id" value="${data[0].id}">`+data[0].code+' // '+data[0].name+' - '+data[0].description,
            '2':'<input type="number" style="text-align: center;" class="form-control" name="amount[]" id="amount" value="1">',
          }).draw();
        }
        let rowNode = dtMaterial.row(`#${data[0].id}`).node();
        $('#amount',rowNode).on('keypress',function(e){
          if(e.keyCode==13 || e.keyCode==9){
            validateRows();
            validateRowsDetail();
          }
        });
        validateRows();
        validateRowsDetail();
      }
    }
  });
}

dtMaterial.on('click','button.deleteItem',function(e){
  let row = $(this).closest('tr');
  dtMaterial.row(row).remove().draw();
  validateRows();
  validateRowsDetail();
  $('.lst-material').focus();
});

btnValidatePrequest.on('click',function(e){
  e.preventDefault();
  clear_table();
  $('#v_diagnosis').val($('#diagnosis').val());
  $('#v_procedure').val($('#procedure').val());
  $('#v_service').val($('#service').val());
  $('#v_bed').val($('#bed').val());
  $('#v_operation').val($('#operation').val());
  $('#v_patient').val($('#patient option:selected').text());
  $('#v_mhouse').val($('#house option:selected').text());
  let total = 0;
  var valideDetails = document.getElementById('v_details').getElementsByTagName('tbody')[0];
  dtMaterial.rows().iterator('row',function(context, index){
    let row = $(this.row(index).node());
    let amount = row.find('#amount').val();
    let material = row.find('#material_name').val();
    let newRow = valideDetails.insertRow(-1);
    let newCell0 = newRow.insertCell(0);
    let newCell1 = newRow.insertCell(1);
    total += parseInt(amount);
    newCell0.innerHTML = material;
    newCell1.innerHTML = amount;
  });
  $('#total-materials').val(total);
  $('#modal_valide').modal('show');
});

function clear_table(){
  var tableHeaderRowCount = 1;
  var table = document.getElementById('v_details');
  var rowCount = table.rows.length;
  for (var i = tableHeaderRowCount; i < rowCount; i++) {
      table.deleteRow(tableHeaderRowCount);
  }
}

function validateRowsDetail(){
  let validate = dtMaterial.rows().count();
  if(validate > 0){
    btnValidatePrequest.show();
  }else{
    selectHouse.prop('disabled',false);
    $('.lst-material').prop('disabled',false);
    btnValidatePrequest.hide();
  }
}

function validateRows(){
  let total=0;
  dtMaterial.rows().iterator('row',function(context, index){
    let row = $(this.row(index).node());
    row.find('#amount').val();
    total += parseInt(row.find('#amount').val());
  });
  $('.total_material').val(total);
}

function searchItemToDetail(id){
  if(dtMaterial.data().filter((item,index) => item.DT_RowId == id).any()){
    return true;
  }
  return false;
}
