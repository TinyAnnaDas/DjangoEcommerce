/*--------------------------
    Add Address
---------------------------*/


var total = '{{order.get_cart_total}}'

function newAddress() {
    document.getElementById("shipping-info").classList.remove('d-none')
    var radioButton = document.getElementsByClassName("radio-button");
        radioButton.checked = false;
    }
    
function cancelNewAddress() {
    document.getElementById("shipping-info").classList.add('d-none')
    }


var shippingform = document.getElementById('shippingform') 

newcsrftoken = shippingform.getElementsByTagName("input")[0].value
console.log('Newtoken :', form.getElementsByTagName("input")[0].value)




shippingform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log("Form Submitted... ")
    addAddress()
    document.getElementById('form-button').classList.add('d-none')
    document.getElementById('payment-info').classList.remove('d-none')
})

    function addAddress(){

        var shippingform = document.getElementById('form') 
    
        var shippingInfo = {
            
            'address': null,
            'city':null,
            'state':null,
            'zipcode':null,
            'shippingaddressId':null,
    
        }
    
        shippingInfo.address = shippingform.address.value
        shippingInfo.city = shippingform.city.value
        shippingInfo.state = shippingform.state.value
        shippingInfo.zipcode = shippingform.zipcode.value
        shippingInfo.shippingaddressId = shippingform.shippingaddressId.value

        console.log(shippingInfo.address)
    
        $.ajax({
            type: "POST",
            url: "/add_address/",
            data: {
                'address':shippingInfo.address,
                'city':shippingInfo.city,
                'state':shippingInfo.state,
                'zipcode':shippingInfo.zipcode,
                'CSRFToken': csrftoken
            },
            success: function (response) {
                console.log(response)
            }
        });
    
    }
	



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
                    submitFormData()
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





