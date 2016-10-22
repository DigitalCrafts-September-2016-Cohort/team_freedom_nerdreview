// // Back button goes back one page on click
// // Doesn't work perfectly: if you come from a different website, it'll take you back there instead of down a level
$('.js-back').on('click', function(){
    history.go(-1);
    return false;
});

// On individual content pages, set the height of the tiles in the main/header and main/body to be even

// console.log('imgList top: ' + $('.img-list').position().top);
// console.log('body top: ' + $('.content').position().top);

var imgListTop = $('.img-list').position().top;
// console.log('imgList top var: ' + imgListTop);
$('.content').css('top', imgListTop - 68);

// console.log('body top: ' + $('.content').position().top);
