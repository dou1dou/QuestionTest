document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.sidebar li');
    const contents = document.querySelectorAll('.content-item');

    items.forEach(item => {
        item.addEventListener('click', function() {
            const contentId = this.getAttribute('data-content');

            contents.forEach(content_right => {
                if (content_right.id === contentId) {
                    content_right.classList.add('active');
                } else {
                    content_right.classList.remove('active');
                }
            });
        });
    });
});

$(document).ready(function () {
    $.ajax({
        url: "/info/personal/api/",
        method: "GET",
        // type: "application/json",
        success: function(response) {
            const username = $(".first-content-item-2");
            const password = $(".first-content-item-3");
            const role = $(".first-content-item-4");
            username.text("账户：" + response['user_name']);
            password.text("密码：" + response['user_password']);
            role.text("角色：" + response['user_role_id']);
        },
        error: function() {
            alert("请求失败！")
        }
    });

    $(".my_homepage").click(function (){
        window.location.href = "/homepage/"
    })
})