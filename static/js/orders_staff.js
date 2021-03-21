$(document).ready(function (){

  function send_ajax (csrf, order_item_id, action) {
    $.ajax({
      method:'POST',
      url: '/admin-staff/change_order/',
      headers: {
         'X-CSRFToken': csrf
       },
      data: JSON.stringify({ action: action, order_item: order_item_id }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data) {
        if (data.result) {
          if (data.order_item_quantity > 0) {
            $(`#order_item_${order_item_id} > td#order_item_quantity`).html(data.order_item_quantity)
            $(`#order_item_${order_item_id} > td#order_item_sum`).html(data.order_item_cost)
            $(`#order_list${data.order} > td#order_sum`).html(data.order_sum)
          } else {
            $(`#order_item_${order_item_id}`).remove();
          }
        } else {
          alert(data.error)
        }
      }
    });
  }

  function delete_item(event) {
    let action = 'delete'
    let order_item_id = event.target.id
    let csrfToken = document.cookie.substring(document.cookie.indexOf('csrf') + 10)
    send_ajax(csrfToken, order_item_id, action);
    event.preventDefault();
  }

  $('.add_order_item').submit(function(event) {
    let form = event.target.elements;
    let order = form.order.value
    $.ajax({
      method:'POST',
      url: '/admin-staff/add_order_item/',
      headers: {
         'X-CSRFToken': form.csrfmiddlewaretoken.value
       },
      data: JSON.stringify({ order: order, product: form.product.value }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data) {
        if (data.result) {
          let empty_row = $(`#order${order} > div > table > tbody > tr.empty`)
          let new_row = $(
            `<tr class="order_item" id="order_item_${data.order_item_pk}">` +
              `<td id="product_name">${data.name}</td>` +
              `<td id="product_price">${data.price}</td>` +
              '<td id="order_item_quantity">1</td>' +
              `<td><i class="fa fa-minus-square-o fa-2x" name='minus' aria-hidden="true" id="${data.order_item_pk}"></i><i class="fa fa-plus-square-o fa-2x" name='plus' aria-hidden="true" id="${data.order_item_pk}"></i></td>` +
              `<td id="order_item_sum">${data.price}</td>` +
              `<td id="delete"><button type="button" class="btn btn-danger btn-sm delete" id="${data.order_item_pk}">Убрать из заказа</button></td>` +
            '</tr>'
          )
          new_row.insertBefore(empty_row)
        } else {
          alert(data.error)
        }
      }
    })
    event.preventDefault();
  });

  $('.order_list').on('click', 'i', function () {
    let action = event.target.attributes.name.value
    let order_item_id = event.target.id
    let csrfToken = document.cookie.substring(document.cookie.indexOf('csrf') + 10)
    send_ajax(csrfToken, order_item_id, action)
    event.preventDefault();
  });

  $('.order_list').on('click', 'button.delete', function () {
    delete_item(event)
  })
});
