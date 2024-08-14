$(function(){
  init();
});
  var total_input = $('.total_entry');
  var btnSaveEntry=$('#save-entry');
  const dtEntry=$('#det_entry').DataTable({
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
          action: 'search_entry',
          q: request.term,
          type: 'list'
        },
        dataType:'json',
      }).done(function(data){
        let results = [];
        data.forEach(element => {
          row = {
            'value':element.code+' - '+element.name+' - '+element.description,
            'label':element.code+' - '+element.name+' - '+element.description,
            'id':element.id
          };
          results.push(row);
        });
        response(results);
      });
    },
    minLength: 1,
    select: function(event, ui){
      event.preventDefault();
      addItemToDetail(ui.item.id);
      $(this).autocomplete('close');
      $(this).val('');
    }
  });
  
  function addItemToDetail(id){
    $.ajax({
      url : '/material/select/',
      type : 'GET',
      data : {
        'action' : 'select',
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
          dtEntry.row.add({
            'DT_RowId':data[0].id, 
            '0':'<button class="btn btn-danger deleteItem" title="Eliminar"> <i class="fas fa-times"></i> </button>',
            '1':`<input type="hidden" id="material_name" value="${data[0].code+' / '+data[0].name+' - '+data[0].description}"><input type="hidden" name="material_id[]" id="material_id" value="${data[0].id}">`+data[0].code+' / '+data[0].name+' - '+data[0].description,
            '2':'<input type="number" class="form-control" style="text-align: center;" name="price_purchase[]" id="price_purchase" step="0.01" value="0">',
            '3':'<input type="number" class="form-control" style="text-align: center;" name="ammount[]" id="ammount" value="0">',
            '4':'<input type="number" class="form-control" style="text-align: center;" name="subtotal[]" id="subtotal" value="0" step="0.01" readonly>',
          }).draw();
          let rowNode = dtEntry.row(`#${data[0].id}`).node();
          $('#ammount',rowNode).on('keypress',function(e){
            if(e.keyCode==13 || e.keyCode==9){
              if($('#price_purchase',rowNode).val() == 0){
                Swal.fire({
                  title:'¡Advertencia!',
                  text: 'Debe agregar el precio unitario del material',
                  icon:'warning'
                });
                return false;
              }
              // changeAmountToDetail(data[0].id,$('#price_purchase',rowNode).val());
              validateRows();
              validateRowsDetail();
              $('.lst-material').focus();
            }
          });
          validateRows();
          validateRowsDetail();
          $('.lst-material').focus();
        }
      }
    });
  }

  function changeAmountToDetail(id,price){
    let row = dtEntry.row('#'+id).node();
    let total = total_input.val();
    let amount = parseFloat($('td:eq(3) input', row).val());
    let subtotal = $('td:eq(4) input', row);
    let new_subtotal = amount * price; 
    total -= parseFloat(subtotal.val());
    subtotal.val(new_subtotal.toFixed(2));
    total += new_subtotal;
    total_input.val(total.toFixed(2));
    $('.lst-material').focus();
  }
  
  dtEntry.on('click','button.deleteItem',function(e){
    let row = $(this).closest('tr');
    dtEntry.row(row).remove().draw();
    validateRows();
    validateRowsDetail();
    $('.lst-material').focus();
  });
  
  function init(){
    btnSaveEntry.hide();
  }
  
  function clear_table(){
    var tableHeaderRowCount = 1;
    var table = document.getElementById('v_details');
    var rowCount = table.rows.length;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
        table.deleteRow(tableHeaderRowCount);
    }
  }
  
  function validateRowsDetail(){
    let validate = dtEntry.rows().count();
    if(validate > 0){
      btnSaveEntry.show();
    }else{
      btnSaveEntry.hide();
    }
  }
  
  function validateRows(){
    let total=0;
    dtEntry.rows().iterator('row',function(context, index){
      let row = $(this.row(index).node());
      let subtotal = parseFloat(row.find('#ammount').val()) * parseFloat(row.find('#price_purchase').val());
      row.find('#subtotal').val(subtotal);
      total += subtotal;
    });
    total_input.val(total);
  }
  
  function searchItemToDetail(id){
    if(dtEntry.data().filter((item,index) => item.DT_RowId == id).any()){
      return true;
    }
    return false;
  }
  