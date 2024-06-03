$(document).ready(function() {
    $("#registerForm").submit(function(e) {
        e.preventDefault();

        const notice = $("#wrong-notice");
        if($("#password").val() !== $("#password_two").val()) {
            notice.show();
            return;
        }
        notice.hide();

        $.ajax({
            method: "POST",
            url: "register/api/user/",
            data: $("#registerForm").serialize(),
            success: function(response) {
                alert("注册成功");
                window.location.href="/login";
            },
            error: function() {
                alert("发送失败")
            }
        })
    })
})
