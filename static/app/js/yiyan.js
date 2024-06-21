$(document).ready(function() {
    $.ajax({
        url: "/homepage/api/",
        method: "GET",
        dataType: "json",
        success: function(data) {
            if(!data['hasLogin']) {
                window.location.href = "/login/";
                return;
            }

            alert(data['user_name'])
        }
    })


    const yiyan = $("#yiyan");
    let author, content, date, from, pic_url;
    $.ajax({
        url: "https://api.oioweb.cn/api/common/yiyan",
        method: "GET",
        success: function(res) {
            // const json = JSON.parse(JSON.stringify(res));
            const json = res.result;
            author = json.author;
            content = json.content;
            date = json.date;
            from = json.from;
            pic_url = json.pic_url;

            // 将数据插入到页面
            yiyan.html(`
                    <div>
                        <p class="center_content">${content}</p>
                        <p class="content_author">———${author}</p>
                        <img class="content_image" src="${pic_url}" alt="Image"/>
                    </div>
                `);
        },
        error: function() {
            alert("Internet Err! ")
        }
    });

    $(".chart").click(function() {
        window.location.href = "/personal/"
    })

    $(".Review").click(function() {
        window.location.href = "/recommend/";
    })
})



