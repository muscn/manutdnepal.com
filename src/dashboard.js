import "./js/_bootstrap"
import "./scss/dashboard.scss";

$(document).ready(function () {
    $(function () {

        $('.flip-container').mouseenter(function () {
            $(this).addClass('open');
        });
        $('.flip-container').mouseleave(function () {
            $(this).removeClass('open');
        });

        $('.btn.warning, .btn-danger').click(function (e) {
            var action = e.currentTarget.value.toLowerCase();
            if (confirm('Are you sure you want to ' + action + '?')) {
                return true;
            } else return false;
        });
    });
});