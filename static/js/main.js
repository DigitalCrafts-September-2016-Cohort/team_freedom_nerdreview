$(document).ready(function(){

    // SLIDE NAVBAR MENU
    $('.js-slide').on('click', function(){
        if ($('.nav-menu').position().left === 0) {
            $('.nav-menu').animate({left: -320});
        } else {
            $('.nav-menu').animate({left: 0});
        }
    });

    $(window).resize(function() {
        if ($(window).width() > 1000) {
            $('.nav-menu').css('left', '0');
        }
    });

    // BACK BUTTON
    // Back button goes back one page on click
    // Doesn't work perfectly: if you come from a different website, it'll take you back there instead of down a level
    $('.js-back').on('click', function(){
        history.go(-1);
        return false;
    });

    // SEE IMAGES BUTTON
    // Show/hide images on click for small screens to save space
    $('.js-images-btn').on('click', function(){
        $('.img-list > ul').slideToggle();
        // var btnText = $('.js-images-btn > h4').html();
        // if ($('.img-list > ul').is(':visible')) {
        //     $('.img-list > ul').css('display', 'inline-block');
        // }
        if ($('.js-images-btn > h4').html() === 'Show images') {
            $('.js-images-btn > h4').html('Hide images');
        } else {
            $('.js-images-btn > h4').html('Show images');
        }
    });

    // ADD NEW REViEW
    // Loops through the input/select tags and enables the Submit button when all fields are filled out
    (function() {
        $('.inputs input, select').keyup(function() {
            var empty = false;
            $('.inputs input, select').each(function() {
                if ($(this).val() == '') {
                    empty = true;
                }
            });
            if (empty) {
                $('.js-submit').attr('disabled', 'disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
            } else {
                $('.js-submit').removeAttr('disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
            }
        });
    })()

    // MODAL FORM VALIDATION
    $('#myForm').validator();

});
