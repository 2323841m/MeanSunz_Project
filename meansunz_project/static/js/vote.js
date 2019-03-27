$(document).ready(function() {
    $('.voteButton').click(function (event) {
        event.preventDefault();
        const form = $(this).parent("form"); // find which form button belongs to
        create_post(form, this);
    });
});

function create_post(form, vote) {
    const h6 = $(vote).closest(".post").find(".rating h6"); // find the displayed rating html
    $.ajax({
        url: form.attr("action"),
        type: "POST",
        data: {
            vote:$(vote).val(),
            id:$(form.find('.id')).val(),  // id for comment voting
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        }, // data sent with the post request

        // handle a successful response
        success: function (json) {
            if(json.not_authenticated) {
                window.location.replace('/login')
            } else {
                h6.html(json.rating + " RATING")  // update displayed rating
            }
        },
    });
}