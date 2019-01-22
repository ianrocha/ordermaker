$(document).ready(function(){
    var productForm = $(".form-product-ajax")

    productForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var submitSpan = thisForm.find(".submit-span")
                if (data.added) {
                submitSpan.html("In Cart <button type='submit' class='btn btn-link'>Remove?</button>")
                } else {
                submitSpan.html("<button type='submit' class='btn btn-success'>Add to Cart</button>")
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)

                var currentPath = window.location.href
                if(currentPath.indexOf("cart") != -1){
                refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Oops!",
                    content: "An error occurred",
                    theme: "modern",
                })
            }
        })
    })

    function refreshCart(){
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        var productRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href


        var refreshCartUrl = '/api/cart/';
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                console.log("success")
                console.log(data)
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.length > 0){
                    productRows.html(" ")
                    i = data.length

                    $.each(data.products, function(index, value){
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope='row'>" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i--
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Oops!",
                    content: "An error occurred",
                    theme: "modern",
                })
            }
        })
    }

    var CartItemQuantity = $("#id_quantity");

    CartItemQuantity.blur(function(){
        var thisItemQuantity = $(this).val()
        var defaultQuantity = $('#id_default_quantity').val()
        if ((thisItemQuantity % defaultQuantity != 0) || (thisItemQuantity == 0)) {
            alert("This item can't be sold in that quantity!")
            var updateItem = $('#update_item')
            updateItem.attr('disabled', true)
        } else {
            var updateItem = $('#update_item')
            updateItem.attr('disabled', false)
        }
    })
})