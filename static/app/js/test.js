// 使用 jQuery 发送 AJAX 请求
$(document).ready(function(){
    $('form').submit(function(e){
        e.preventDefault(); // 防止表单默认提交

        $.ajax({
            type: 'POST',
            url: '/api/test/', // 提交表单的后端处理接口
            data: $('form').serialize(), // 序列化表单数据
            success: function(response){
                // 在页面上显示提交结果
                alert(JSON.stringify(response));
            },
            error: function(){
                // 处理错误情况
                alert('表单提交失败');
            }
        });
    });
});
