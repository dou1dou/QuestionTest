let imageIndex = 0;
const images = [
    "static/app/img/welcome.png",
    "static/app/img/welcome2.png",
    "static/app/img/welcome3.png"
];
$(document).ready(function() {
    $(".goto-login").click(function() {
        window.location.href = "/login/";
    });

    $(".goto-register").click(function() {
        window.location.href = "/register/";
    });

    function changeImage() {
        $('#imageToChange').attr('src', images[imageIndex]);
    }

    $('#prevImageBtn').click(function() {
        imageIndex--;
        if (imageIndex < 0) {
            imageIndex = images.length - 1;
        }
        changeImage();
    });

    $('#nextImageBtn').click(function() {
        imageIndex++;
        if (imageIndex === images.length) {
            imageIndex = 0;
        }
        changeImage();
    });
});