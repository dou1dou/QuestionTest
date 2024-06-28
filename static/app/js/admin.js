$(document).ready(function (){
    $.ajax({
        url: "/deleted_user/api/",
        method: "GET",
        success: function(response) {
            for(let i = 0; i < response['user'].length; ++i) {
                const info_div = document.createElement("div");
                info_div.className = "users";
                info_div.innerHTML = `
                    <div style="display: flex; justify-content: center;align-items: center; flex: 1">    
                        <div>${response['user'][i]}</div>
                    </div>
                `;
                $("#deleted_user").append(info_div);
            }
        },
        error: function() {
            alert("error!");
        }
    })
})


$(document).ready(function () {
    $("#Button").click(function (event) {
        $.ajax({
        type: "POST",
        url: "/delete_user/api/",
        success: function (response) {
            alert("delete successfully");
        },
        error: function() {
            alert("error!");
        }
        })
    })
})
