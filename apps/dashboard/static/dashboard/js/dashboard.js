$(document).ready(function () {
            $(function () {
                $('.flip-container').mouseenter(function () {
                    $(this).addClass('open');
                });
                $('.flip-container').mouseleave(function () {
                    $(this).removeClass('open');
                });
            });

        });