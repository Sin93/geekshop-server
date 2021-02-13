$(document).ready(function (){

  function current_value () {
    // Функция для обновления текущих значений количества каждого товара
    var inputs = $('.product_quantity')
    var current_values = {}
    inputs.each(function(index, element) {
      current_values[`${element.id}`] = element.value
    })

    return current_values
  }

  function send_ajax (input_id, input_value) {
    // функция для отправки ajax запроса на сервер
    $.ajax({
      url: `/basket/edit/${Number(input_id)}/${Number(input_value)}/`,
      success: function(data) {

        if (data.result == false) {
          // если сервер вернул false значит что-то пошло не так и алертим ошибку
          alert('Ошибка на сервере, значение не изменено!')
          $(`.basket_list#${input_id}`).value = current_input_value[input_id]
        } else if (data.result == 'delete') {
          // если сервер вернул delete и id, то удаляем соответствующий блок
          $(`.basket_record#${data.id}`).remove();
          // обновляем текущие значения количества товаров в словаре
          current_input_value = current_value()
          // обновляем общее количество и сумму
          $('.total_quantity').text(data.total_quantity)
          $('.total_cost').text(data.total_cost)
        } else {
          // если всё ок, сервер присылает нам новое значение, подставляем его в input
          $(`.product_quantity[id=${data.id}]`)[0].value = data.result
          // обновляем текущие значения количества товаров в словаре
          current_input_value = current_value()
          // обновляем общее количество и сумму
          $('.total_quantity').text(data.total_quantity)
          $('.total_cost').text(data.total_cost)
        }
      }
    });
  }

  // словарь с текущим количеством каждого товара в корзине
  var current_input_value = current_value()

  $('.basket_list').on('click', 'i', function () {
    // берём иконку на которую нажали
    var target_input = event.target;
    // берём по id иконки - Input в котором должно измениться значение
    target_input = $(`.product_quantity[id=${target_input.id}]`)

    if (event.target.attributes.name.value == 'plus') {
      // если иконка плюс то делаем ajax запрос на сервер
      send_ajax(Number(target_input.attr('id')), Number(target_input.val()) + 1)

    } else if (event.target.attributes.name.value == 'minus') {
      // если иконка минуса то делаем ajax запрос на сервер
      send_ajax(Number(target_input.attr('id')), Number(target_input.val()) - 1)
    }

    event.preventDefault();
  });

  $('.basket_list').on('change', 'input', function () {
    // берём элемент, который менялся
    var target_input = event.target;

    if (Number(target_input.value) <= 0) {
      // если значение <= 0, то спрашиваем удалить товар из корзины?
      confirm_deletion = confirm('Удалить товар из корзины?')
      if (confirm_deletion) {
        // если удаляем товар, то отправляем на сервер ajax с 0 товаров
        send_ajax(Number(target_input.id), 0)
      } else {
        // если не удаляем, то возвращаем в поле значение, какое было
        target_input.value = current_input_value[target_input.id]
      }
    } else {
      // если значение положительное, то просто отправляем его на сервер, чтоб обновилось
      send_ajax(Number(target_input.id), Number(target_input.value))
    }

    event.preventDefault();
  });
});
