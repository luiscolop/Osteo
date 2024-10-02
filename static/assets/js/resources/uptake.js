$(function(){
  var selectHouse = $('#house_select');
  var houseSelect = $('#house');

  houseSelect.val(selectHouse.val()).change();
  houseSelect.select2({disabled:'readonly'});
});
  
const dtMaterial=$('#det_uptake').DataTable({
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
  
dtMaterial.on('click','button.deleteItem',function(e){
  let row = $(this).closest('tr');
  dtMaterial.row(row).remove().draw();
  validateRows();
  validateRowsDetail();
  $('.lst-material').focus();
});

dtMaterial.on('input','input#amount',function(e){
  if($(this).val() != ''){
    validateRows();
    validateRowsDetail();
  }
});

function clear_table(){
  var tableHeaderRowCount = 1;
  var table = document.getElementById('v_details');
  var rowCount = table.rows.length;
  for (var i = tableHeaderRowCount; i < rowCount; i++) {
      table.deleteRow(tableHeaderRowCount);
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

  