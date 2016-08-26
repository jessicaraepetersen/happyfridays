// #############################################################################
// Change play button to pause button or vice versa
// $('#dropdownMenu1').click(function() {
//     $('#dropdownMenu1').removeClass('play-btn');
//     $('#dropdownMenu1').addClass('pause-btn');
// });

// $('.play-btn').click(function(evt) {
//     var album_id = $(this).data('albumId');
//     if $('#intro-par').hasClass('fancy');
//     $('#card' + album_id ).remove();
// });


// #############################################################################
// Remove div album card upon clicking the x button


$('.x-btn').click(function(evt) {
    var album_id = $(this).data('albumId');
    $('#card' + album_id ).remove();
});


// #############################################################################
// A user can add all the tracks of an album to one of their playlists of choice
// and a message will appear at the top of the html page alerting the user of the
// event.


function showFlashMessage(result) {
    album_name = result['album_name']
    playlist_name = result['playlist_name']

    console.log(album_name);
    console.log(playlist_name);


    $('#album-added-message').html(album_name + ' was added to your playlist ' + playlist_name)
    $("#album-added-box").fadeIn(250);
    setTimeout(function() {$('#album-added-box').fadeOut(250);}, 3000);         
}


function addAlbumToPlaylist(evt) {
    evt.preventDefault();

    var playlist_id = $(this).data('playlistId');
    var album_id = $(this).data('albumId');

    console.log($(this).data('playlistId'));
    console.log($(this).data('albumId'));

    $.post('/add-to-playlist', 
           {'playlist_id': playlist_id, 'album_id': album_id}, 
           showFlashMessage);  
}

$('.playlist-choice').click(addAlbumToPlaylist);







