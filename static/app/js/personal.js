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
    });

    $(".questions").click(function (){
        window.location.href = "/questions/"
    });
})


$(document).ready(function (){
    let all, solved;
    $.ajax({
        url: "/info/personal/get_solved_question_number/api/",
        method: "GET",
        success: function(response){
            const sum_solved = $(".circle-content1-sum");
            sum_solved.text(response['solved'] + "/" + response['all'])
            all = response['all'];
            solved = response['solved'];
        },
        error: function (){
            alert("请求失败！")
        }
    });

    $.ajax({
        url: "/exam/list/api/",
        method: "GET",
        success: function(response) {
            for(let i = 0; i < response['data'].length && i < 6; ++i) {
                const info_div = document.createElement("div");
                info_div.className = "exam-info-items";
                info_div.innerHTML = `
                    <div style="display: flex; font-size: 1.5vw; align-items: center; margin-top: 1vw">    
                        <div style="flex: 1; display: flex; justify-content: center;">${response['data'][i]['exam-id']}</div>
                        <div style="flex: 1; display: flex; justify-content: center;">${response['data'][i]['exam-name']}</div>
                        <div style="flex: 1; display: flex; justify-content: center;">${response['data'][i]['exam-time']}分钟</div>
                    </div>
                    <hr style="margin-top: 1vw; margin-bottom: 1vw">
                `;
                $("#content2").append(info_div);
            }
        },
        error: function() {

        }
    })
})

function confirmLogout() {
    $.ajax({
        url: "/logout/api/",
        method: "POST",
        success: function(response) {
            if(response['logout']) {
                alert("注销成功！");
                window.location.href = "/";
            } else {
                alert("数据库繁忙，请稍后再试！");
            }
        },
        error: function() {
            alert("网络异常，请重试！");
        }
    })
}
