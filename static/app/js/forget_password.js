$(document).ready(function() {
    $("form").submit(function(e) {
        e.preventDefault();

        const notice = $("#wrong-notice");
        const password = $("#password").val();
        if(password !== $("#password_two").val()) {
            notice.show();
            return;
        }
        notice.hide();

        const weak_notice = $("#password-weak-notice");
        if(password.length < 8) {
            weak_notice.show();
            return;
        }
        weak_notice.hide();

        $.ajax({
            method: "POST",
            url: "/forgetpassword/api/",
            data: $("form").serialize(),
            success: function(response) {
                alert("修改密码成功，返回登录");
                window.location.href="/login";
            },
            error: function() {
                alert("发送失败")
            }
        })
    })
})
