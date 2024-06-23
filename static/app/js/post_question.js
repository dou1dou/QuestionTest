$(document).ready(function() {
    $("form").submit(function(e) {
        e.preventDefault();

        let answer = "";
        const selected = document.querySelectorAll("input[name='answer']:checked");
        for(let i = 0; i < selected.length; i++) {
            answer = answer + selected[i].value;
        }

        $.ajax({
            url: "/postquestion/api/",
            method: "POST",
            data: {
                "csrfmiddlewaretoken": $("input[name='csrfmiddlewaretoken']").val(),
                "description": $("input[name='description']").val(),
                "choice_a": $("input[name='choice_a']").val(),
                "choice_b": $("input[name='choice_b']").val(),
                "choice_c": $("input[name='choice_c']").val(),
                "choice_d": $("input[name='choice_d']").val(),
                "answer": answer,
                "knowledge_point": $("input[name='knowledge_point']").val(),
                "parse": $("input[name='parse']").val(),
                "difficulty": $("input[name='difficulty']").val(),
            },
            success: function(response) {
                alert(JSON.stringify(response));
            },
            error: function(){
                alert("发送失败")
            }
        })
    })
})
