$(document).ready(function () {
    $("#login-form").submit(function (event) {
        event.preventDefault();

        $.ajax({
            type: "POST",
            url: "login/",
            data: $("#login-form").serialize(),
            success: function(response){
                let json = JSON.parse(JSON.stringify(response));
                if(json.login) {
                    $("#wrong-notice").hide()
                    alert("登陆成功");
                } else {
                    $("#wrong-notice").show()
                }
            },
            error: function(){
                alert("请重试！")
            }
        });
    });

    $("#register").click(function() {
        window.location.href = "http://localhost:8000/register";
    })
})
