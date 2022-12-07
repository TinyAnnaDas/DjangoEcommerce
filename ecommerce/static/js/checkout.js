
/*--------------------------
    Coupon Management 
---------------------------*/


couponform = document.getElementById('coupon-form')

console.log(couponform)

couponform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log("Coupon Submitted... ")
    addCoupon()

    })

function addCoupon(){

    let total = document.getElementById('carttotal').value
    let orderid = document.getElementById('orderid').value
    console.log(total)
    console.log(orderid)

    var couponcode = couponform.couponcode.value

    console.log(couponcode)

    var csrftoken =  $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: "POST",
        url: "/add_coupon/",
        data: {
            'couponcode':couponcode,
            'total': total,
            'orderid': orderid,
            csrfmiddlewaretoken: csrftoken
        },
        success: function (response) {
            console.log(response)

            if (response.error_message){
                document.getElementById('coupon-success-msg').hidden = true
                document.getElementById('coupon-error-msg').hidden = false
                document.getElementById('coupon-error-msg').innerHTML = response.error_message
            }

            if (response.coupon_discount){

                document.getElementById('coupon-error-msg').hidden = true
                document.getElementById('coupon-success-msg').hidden = false
                document.getElementById('coupon-success-msg').innerHTML = response.coupon_discount + '% discount applied'
                document.getElementById('coupon-cart-total').innerHTML = '&#8377; '+response.discounted_price
                document.getElementById('discounted_amount').hidden = false
                document.getElementById('discounted_amount').firstElementChild.innerHTML = '&#8377; '+response.discounted_amount

            }


            
        }
    });

}

/*--------------------------
    Add Address
---------------------------*/
function deliverHere(){
    document.getElementById("payment-info").classList.remove('d-none')
}

function newAddress() {
    document.getElementById("shipping-info").classList.remove('d-none')
    var radioButton = document.getElementsByClassName("radio-button");
        radioButton.checked = false;
    }
    
function cancelNewAddress() {
    document.getElementById("shipping-info").classList.add('d-none')
    }


var shippingform = document.getElementById('shippingform') 

shippingform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log("Form Submitted... ")
    addAddress()
    document.getElementById('shipping-info').classList.add('d-none')
    document.getElementById('payment-info').classList.remove('d-none')
    })

function addAddress(){
    console.log('sending data.. ')
    var shippingInfo = {
        'name':null,
        'phone':null,
        'address': null,
        'city':null,
        'state':null,
        'zipcode':null,
        'shippingaddressId':null,

    }
    shippingInfo.name = shippingform.name.value
    shippingInfo.phone = shippingform.phone.value
    shippingInfo.address = shippingform.address.value
    shippingInfo.city = shippingform.city.value
    shippingInfo.state = shippingform.state.value
    shippingInfo.zipcode = shippingform.zipcode.value
    shippingInfo.shippingaddressId = shippingform.shippingaddressId.value


    var csrftoken =  $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: "POST",
        url: "/add_address/",
        data: {
            'name':shippingInfo.name,
            'phone':shippingInfo.phone,
            'address':shippingInfo.address,
            'city':shippingInfo.city,
            'state':shippingInfo.state,
            'zipcode':shippingInfo.zipcode,
            csrfmiddlewaretoken: csrftoken
        },

        success: function (response) {
            console.log(response)
            console.log(response[0].fields.name)
            console.log(response[0].fields.phone)
            console.log(response[0].fields.address)
            console.log(response[0].fields.city)
            console.log(response[0].fields.state)
            console.log(response[0].fields.zipcode)
            value = response[0].pk


            

            var x = document.createElement("INPUT");
            x.setAttribute("type", "radio");
            x.setAttribute("class", "radio-button");
            x.setAttribute("name", "shippingaddressId");
            x.setAttribute('checked', true);
            x.setAttribute("value", value);
            
            const addresses = document.getElementById("addresses");
            addresses.appendChild(x);


            var mybr = document.createElement('br');
            addresses.appendChild(mybr);

           
            var label = document.createElement("Label");
            addresses.appendChild(label);
            var card_body = document.createElement("div")
            card_body.setAttribute("class", "card-body")
            label.appendChild(card_body)
            

            var card_title =  document.createElement("div")
            card_title.setAttribute("class", "card-title")
            card_body.appendChild(card_title)
            const name = document.createTextNode(response[0].fields.name);
            card_title.appendChild(name)


            var card_subtitle = document.createElement("div")
            card_subtitle.setAttribute("class", "card-subtitle")
            card_body.appendChild(card_subtitle)

            const phone = document.createTextNode(response[0].fields.phone)
            card_subtitle.appendChild(phone)


            var card_text = document.createElement("div")
            card_text.setAttribute("class", "card-text")
            card_body.appendChild(card_text)

            const address1 = document.createTextNode(response[0].fields.address+", ");
            card_text.appendChild(address1)
            const city = document.createTextNode(response[0].fields.city+", ")
            card_text.appendChild(city)
            const state = document.createTextNode(response[0].fields.state+", ")
            card_text.appendChild(state)
            const zipcode = document.createTextNode(response[0].fields.zipcode)
            card_text.appendChild(zipcode)

            // const para = document.createElement("p");
            // const node = document.createTextNode("This is new.");
            // para.appendChild(node);
            // const element = document.getElementById("addresses");
            // element.appendChild(para);
        }
    });

    }

/*--------------------------
    COD Payment
---------------------------*/



document.getElementById('make-payment').addEventListener('click', function(e){
    processOrder()
})

/*--------------------------
    Paypal Integration
---------------------------*/


    // Render the PayPal button into #paypal-button-container
    paypal_sdk.Buttons({

        // Set up the transaction
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: parseFloat(total/84).toFixed(2)
                    }
                }]
            });
        },

        // Finalize the transaction
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(orderData) {
                // Successful capture! For demo purposes:
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                var transaction = orderData.purchase_units[0].payments.captures[0];
                alert('Transaction '+ transaction.status + ': ' + transaction.id + '\n\nSee console for all available details');

                processOrder()

                // Replace the above to show a success message within this page, e.g.
                // const element = document.getElementById('paypal-button-container');
                // element.innerHTML = '';
                // element.innerHTML = '<h3>Thank you for your payment!</h3>';
                // Or go to another URL:  actions.redirect('thank_you.html');
            });
        }


    }).render('#paypal-button-container');


/*--------------------------
    Rarzorpay Integration
---------------------------*/

$(document).ready(function(){

    $('.payWithRazorpay').click(function(e){
        e.preventDefault();

        var name = $("[name='name']").val()
        var email = $("[email='email']").val()
        var address = $("[address='address']").val()
        var address1 = $("[address1='address1']").val()
        var city = $("[city='city']").val()
        var state = $("[state='state']").val()
        var country = $("[country='country']").val()
        var zipcode = $("[zipcode='zipcode']").val()
        console.log(name)

        if (name == "" || email == "" || address == "" || address1 == "" || city == "" || state == "" || country == "" || zipcode == "" ){
        
            swal("Alert", "All fields are mandatory!", "error");
            return false
        } else {

            var options = {
                "key": "rzp_test_3wusM93Kj6imwz", // Enter the Key ID generated from the Dashboard
                "amount": total * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Treehouse",
                "description": "Test Transaction",
                "image": "https://example.com/your_logo",
                // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){
                    // alert(response.razorpay_payment_id);
                    processOrder()
                },
                "prefill": {
                    "name": name,
                    "email": email,
                    
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);
            rzp1.open();
        }

    })

});

var total = document.getElementById('carttotal').value

console.log('total: ', total)

function processOrder(){
    console.log('payment button clicked')

    var orderData = {
        'shippingaddressId': document.getElementById('shippingaddressid').value,
        'total':total,
    }

    var url = '/process_order/'

    fetch (url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'orderdata':orderData})
    })

    .then((response) => response.json())
    .then((data) => { 
        alert('Transaction completed')
    })



}




