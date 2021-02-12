$(document).ready(function (){
  $('.basket_list').on('click', 'input[type="number"]', function () {
    var target_input = event.target;
    console.log(`/basket/edit/${target_input.name}/${target_input.value}`)

    $.ajax({
      url: `/basket/edit/${Number(target_input.name)}/${Number(target_input.value)}/`,
      success: function(data) {
        $('.basket_list').html(data.result)
      }
    });

    event.preventDefault();
  });
});
