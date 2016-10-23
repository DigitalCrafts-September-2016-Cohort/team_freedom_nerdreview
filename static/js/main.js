$(document).ready(function(){
    // SLIDE NAVBAR MENU
    $('.js-slide').on('click', function(){
        if ($('.nav-menu').position().left === 0) {
            $('.nav-menu').animate({left: -320});
        } else {
            $('.nav-menu').animate({left: 0});
        }
    });

    //function(){
    //     $('navbar').animate({width: 320});
    //     $('main').animate({left: 320});
    // });

    // BACK BUTTON
    // Back button goes back one page on click
    // Doesn't work perfectly: if you come from a different website, it'll take you back there instead of down a level
    $('.js-back').on('click', function(){
        history.go(-1);
        return false;
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

    // INDIVIDUAL CONTENT
    // On individual content pages, set the height of the tiles in the main/header and main/body to be even
    // Script stops running if .img-list isn't on the page, so keep this part at bottom
    // var imgListTop = $('.img-list').position().top;
    // $('.content').css('top', imgListTop - 71);
});
