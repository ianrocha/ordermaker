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

    var clientForm = $(".form-client-ajax")

    clientForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();
        var clientCurrentUrl = window.location.href;
        console.log(clientCurrentUrl)

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var submitSpan = thisForm.find(".submit-span")
                if (data.added) {
                submitSpan.html("Selected <button type='submit' class='btn btn-link'>Remove?</button>")
                } else {
                submitSpan.html("<button type='submit' class='btn btn-success'>Change client</button>")
                }
                window.location.href = clientCurrentUrl
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

    var CartItemQuantity = $("#id_quantity");

    CartItemQuantity.blur(function(){
        // Check if the quantity input by user is multiple of the default quantity
        var thisItemQuantity = $(this).val()
        var defaultQuantity = $('#id_default_quantity').val()
        var updateItem = $('#update_item')
        if ((thisItemQuantity % defaultQuantity != 0) || (thisItemQuantity == 0)) {
            alert("This item can only be sold in multiples of " + defaultQuantity)
            updateItem.attr('disabled', true)
        } else {
            updateItem.attr('disabled', false)
        }
    })

    var CartItemPrice = $('#id_price')

    CartItemPrice.blur(function(){
        refreshProfitability()
    })

    var CartItemProfitability = $('#id_profitability')

    CartItemProfitability.blur(function(){
        refreshProfitability()
    })

    function refreshProfitability(){
    //  Check the value for profitability
        var thisItemProfitability = CartItemProfitability
        var thisItemPrice = CartItemPrice.val()
        var defaultPrice = $('#id_default_price').val()
        var minGoodProfit = defaultPrice - (defaultPrice * 0.10)
        var updateItem = $('#update_item')

        if (thisItemPrice > defaultPrice){
        //  set to optimum profitability -> price greater than default price
            thisItemProfitability.val('Optimum');
            updateItem.attr('disabled', false);
        } else if ((thisItemPrice >= minGoodProfit)  && (thisItemPrice <= defaultPrice)) {
        //  set to good profitability -> price equal or less than default and greater or equal than default - 10%
            thisItemProfitability.val('Good');
            updateItem.attr('disabled', false)
        } else {
        //  set to bad profitability ->  price less than default - 10%;
        //  disable update button and show alert
            thisItemProfitability.val('Bad');
            alert("Bad profitable items can't be added to cart!")
            updateItem.attr('disabled', true);

        }
    }
})