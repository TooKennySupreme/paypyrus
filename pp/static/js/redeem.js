$(function () {
    $("#redeem-money").click(function () {
        if ($('#venmo-acct').val() === "") {
            $(".status").html("Please provide your Venmo information to redeem your paypyrus.");
            return;
        }
        $(".status").addClass("darken-3");
        $(".status").html("<i class='material-icons'>flight_land</i> Redeeming...");

		$.ajax({
            url: "/api/v1/redeem/{{ token | e }}/",
			data: {
				phone_email: $('#venmo-acct').val(),
                reason: $("#reason").val()
			},
			method: 'POST',
			error: function(xhr, status, error) {
				console.log(xhr);
				console.log(error);
			},
			success: function(data, status, xhr) {
                $(".status").removeClass("darken-3");
				console.log(data);
                if (data == "OK") {
                    $(".status").html("Your money has been redeemed! You should see the funds show up in your Venmo account soon. <i class='material-icons'>payment</i>");
                }
                else {
                    $(".status").html(data);
                }
			}
		});
    });
    $("#check-balance").click(function () {
        $(".status").addClass("darken-3");
        $(".status").html("<i class='material-icons'>flight_land</i> Checking your balance...");

		$.ajax({
			url: "/api/v1/check_balance/{{ token | e }}/",
			method: 'POST',
			error: function(xhr, status, error) {
				console.log(xhr);
				console.log(error);
			},
			success: function(data, status, xhr) {
                $(".status").removeClass("darken-3");
				console.log(data);
                if (data.length > 0) {
                    $(".status").html("The balance of this paypyrus is $"+data+"' <i class='material-icons'>redeem</i></a>");
                }
			}
		});
    });
});
