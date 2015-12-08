// after we have got access to the users webcam
var videoSuccess = function(video) {
    $('#reader').html(video);$("#reader").find("video").attr("width", "100%").attr("height", "auto");
};

var videoError = function(e) {console.log("error");};
//if we have successfully found a QR code
var qrSuccess = function(data) {window.location = data;};
//if we didn't find a QR code
var qrError = function(e) { /* console.log(e);*/ };
//call the miniqr-reader function
Miniqr.reader(videoSuccess, videoError, qrSuccess, qrError);
