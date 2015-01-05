$(document).ready(function () {
    $(function () {

        $('.flip-container').mouseenter(function () {
            $(this).addClass('open');
        });
        $('.flip-container').mouseleave(function () {
            $(this).removeClass('open');
        });

        $('.btn.warning').click(function (e) {
            var action = e.currentTarget.value.toLowerCase();
            if (confirm('Are you sure you want to ' + action + '?')) {
                return true;
            } else return false;
        });
        $('.btn-danger').click(function (e) {
            if (confirm('Are you sure you want to delete?')) {
                return true;
            } else return false;
        });


    });
});