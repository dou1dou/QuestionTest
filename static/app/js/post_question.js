$(document).ready(function() {
    $("form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            url: "/postquestion/api/",
            method: "POST",
            data: $(this).serialize(),
            success: function(response) {
                alert(JSON.stringify(response));
            },
            error: function(){
                alert("发送失败")
            }
        })
    })
})
