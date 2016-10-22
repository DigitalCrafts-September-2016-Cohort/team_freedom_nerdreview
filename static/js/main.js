// // Back button goes back one page on click
// // Doesn't work perfectly: if you come from a different website, it'll take you back there instead of down a level
$('.js-back').on('click', function(){
    history.go(-1);
    return false;
});
