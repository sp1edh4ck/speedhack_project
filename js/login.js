$(function () {
    $(".button").click(function (e) {
        var value_click = $(this).find(".value-click");
        var val = parseInt(value_click.text());

        if ($(this).hasClass('clicked')) {
            value_click.text(val - 1);
            $(this).addClass('button').removeClass('button-clicked');
        } else {
            value_click.text(val + 1);
            $(this).addClass('button-clicked').removeClass('button');
        }

        $(this).toggleClass('clicked');

        e.prevendDefault();
    });
});