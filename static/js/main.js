// Change play button to pause button or vice versa
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
//    $.post


// // #send an ajax request to sever and server send to database
//    pst to route
//    return null;
// }


// $('.playlist-choice').click(function (evt) {
//     // var playlist_id = $(this).data('playlistId');
//     // var album_id = $(this).data('albumId');

//     console.log($(this).data('playlistId'));
//     console.log($(this).data('albumId'));


//     // $.post('/add-to-playlist', 
//     //    playlist_id,
//     //    album_id
//     //    );    
// });


// #############################################################################
// A user can add all the tracks of an album to one of their playlists of choice.

function showFlashMessage(result) {

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







