

// $('#dropdownMenu1').click(function() {
//     $('#dropdownMenu1').removeClass('play-btn');
//     $('#dropdownMenu1').addClass('pause-btn');
// });


// Remove div album card upon clicking the x button
$('.x-btn').click(function(evt) {
    var album_id = $(this).data('albumId');
    $('#card' + album_id ).remove();
});


// window.onbeforeunload = closingCode;
// function closingCode(){
//    // do something...
//    return null;
// }



// $( 'x-btn' {{ album.album_id }} ).click(function() {
//   $(  ).remove();
// });


// $( 'x-btn' {{ album.album_id }} ).click(function() {
//     $( 'album-card' {{ album.album_id }} ).remove();
//     });