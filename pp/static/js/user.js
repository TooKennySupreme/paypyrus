$('#btn-qty-1').click(function () {
    $('#quantity_1').focus();
});
$('#btn-qty-5').click(function () {
    $('#quantity_5').focus();
});
$('#btn-qty-10').click(function () {
    $('#quantity_10').focus();
});

function create_payment(data) {
    $(".status").addClass("darken-3");
    $(".status").html("<i class='material-icons'>flight_land</i> Loading your papyrus(es)...");

    $.ajax({
        url: "/api/v1/get_bill/",
        data: data,
        method: 'POST',
        error: function(xhr, status, error) {
            $(".status").html("Error: "+ xhr.responseText);
        },
        success: function(data, status, xhr) {
            $(".status").removeClass("darken-3");
            var backnum = data.split(",").length;
            if (data.length > 0) {
                $(".status").html("Your bills have been created! <a target='_blank' href='/print/"+data+"'>  Bills</a> <i class='material-icons'>local_printshop</i> <a target='_blank' href='/backs/"+backnum+"'>Backs</a>");
            }
        }
    });
}

$("#submit-custom-monies").click(function () {
    var data = {
        custom_amount: $("#amount-custom").val()
    };
    create_payment(data);
});

$('#submit-monies').click(function () {
    var data = {
        quantity_1: $('#quantity_1').val(),
        quantity_5: $('#quantity_5').val(),
        quantity_10: $('#quantity_10').val()
    };
    create_payment(data);
});
