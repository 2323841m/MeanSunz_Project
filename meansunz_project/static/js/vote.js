$(document).ready(function () {
    $('.voteUpButton').click(function (event) {
        event.preventDefault();
        const form = $(this).parent("form"); // find which form button belongs to
        create_post(form, this);
    });
});

$(document).ready(function () {
    $('.voteDownButton').click(function (event) {
        event.preventDefault();
        const form = $(this).parent("form"); // find which form button belongs to
        create_post(form, this);
    });
});

function create_post(form, vote) {
    // get html elements that are to be updated on success
    const h6 = $(vote).closest(".post").find(".rating h6"); // find the displayed rating html
    const upBttn = $(form).find(".voteUpButton");  // find form's upvote button
    const downBttn = $(form).find(".voteDownButton");  // find form's downvote button
    $.ajax({
        url: form.attr("action"),
        type: "POST",
        data: {
            vote: $(vote).val(),
            id: $(form.find('.id')).val(),  // id for comment voting
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        }, // data sent with the post request

        // handle a successful response
        success: function (json) {
            if (json.not_authenticated) {
                window.location.replace('/login')
            } else {
                h6.html(json.rating + " RATING")  // update displayed rating
                // update buttons to reflect which vote has been chosen by the user
                switch (parseInt(json.voted)) {
                    case 0:
                        upBttn.attr("name", "notVoted");
                        downBttn.attr("name", "notVoted");
                        break;
                    case 1:
                        upBttn.attr("name", "voted");
                        downBttn.attr("name", "notVoted");
                        break;
                    case -1:
                        upBttn.attr("name", "notVoted");
                        downBttn.attr("name", "voted");
                        break;
                }
            }
        },
    });
}