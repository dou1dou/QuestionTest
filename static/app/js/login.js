$(document).ready(function() {
    $("form").submit(function(event) {
        event.preventDefault();

        $.ajax({
            method: "POST",
            url: "api/",
            data: $("form").serialize(),
            success: function(response) {
                if(JSON.parse(JSON.stringify(response)).login) {
                    alert("登陆成功")
                } else {
                    alert("用户名或密码错误")
                }
            },
            error: function() {
                alert("发生错误，请重试")
            }
        })
    });

    $("#goto-register").click(function() {
        window.location.href = "/register";
    })
})
