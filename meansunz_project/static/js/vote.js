$(document).ready(function() {
    $('.voteButton').click(function (event) {
        event.preventDefault();
        const url = $(this).parent("form").attr("action"); // get post url from form action
        create_post(url, this);
    });
});

function create_post(url, vote) {
    const h6 = $(vote).closest(".post").find(".rating h6");
    $.ajax({
        url: url,
        type: "POST",
        data: {
            vote:$(vote).val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        }, // data sent with the post request

        // handle a successful response
        success: function (response) {
            console.log(response); // log the response to the console
            h6.html(response + " RATING");
        },
    });
}