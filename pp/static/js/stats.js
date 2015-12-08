$(".delete-bill").click(function () {
    var btoken = $(this).data("token");
    var current_element = $(this);
    $.ajax({
        url: "/api/v1/delete_bill/",
        data: {
            bill_token: btoken
        },
        method: 'POST',
        error: function(xhr, status, error) {
            console.log(xhr);
            console.log(error);
            $(".status").html("Error: "+ xhr.responseText);
        },
        success: function(data, status, xhr) {
            if (data == "OK") {
                current_element.removeClass("red");
                current_element.addClass("blue");
                current_element.attr("disabled", "true");
                current_element.html("Deleted");
            }
        }
    });
});
