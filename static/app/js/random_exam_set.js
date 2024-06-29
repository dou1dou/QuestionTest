$(document).ready(function () {
  $("#submitButton").click(function (event) {
    event.preventDefault();

    let formData = $("#examForm").serialize();
    let examId = 0;

    $.ajax({
      type: "POST",
      url: "/teacher/set_exam/api/",
      data: formData,
      dataType: "json",
      success: function (data) {
        alert("Exam Set Successfully");
        examId = parseInt(data['exam-id']);
        // 提示用户输入试题数量、类型和难度
        let questionCount = parseInt(prompt("请输入试题数量："));
        if (isNaN(questionCount) || questionCount <= 0) {
          alert("请输入有效的试题数量！");
          return;
        }

        let questionType = prompt("请输入试题类型：");
        if (questionType === null || questionType.trim() === "") {
          alert("请输入有效的试题类型！");
          return;
        }

        let questionDifficulty = parseInt(prompt("请输入试题难度："));
        if (isNaN(questionDifficulty)) {
          alert("请输入有效的试题难度！");
          return;
        }

        // 从服务器获取试题
        const choices = ['A', 'B', 'C', 'D'];
        $.ajax({
          url: '/questions/api/',
          type: 'GET',
          dataType: 'json',
          data: {
            limit: questionCount,
            Knowledge_points: questionType,
            Difficulty: questionDifficulty // 假设服务器API接受这些参数
          },
          success: function (data) {
            // 假设data是一个包含试题的数组，每个试题是一个对象
            $('#questions ul').empty(); // 清空现有的试题列表
            $.each(data, function (index, questionData) {
              const questionElement = $('<li></li>'); // 创建一个新的列表项

              // 添加问题描述（这里假设questionData[0]是问题描述）
              // questionElement.append(`<p class="questions-desc-css">${parseInt(index) + 1}、${questionData[0]}</p>`);

              // 假设questionData[1]到questionData[4]是选项，questionData[5]是答案
              for (let i = 0; i < 5; ++i) {
                if (i === 0) {
                  questionElement.append(`<p class="questions-desc-css">${parseInt(index) + 1}、${questionData[i + 1]}</p>`);
                } else if (questionData[i + 1] !== null) {
                  const isMultipleChoice = questionData[6].length > 1;
                  const choiceElement = $(`
                  <div class="questions-choice-css" style="display: flex">
                    <div class="choice-btn">
                      <input type="${isMultipleChoice ? 'checkbox' : 'radio'}" id="option${i + 1}" name="options-${index}" value="${choices[i - 1]}">
                    </div>
                    <div class="choice-content">${questionData[i + 1]}</div>
                  </div>
                `);
                  questionElement.append(choiceElement);
                }
              }

              // 将问题添加到列表中
              $('#questions ul').append(questionElement);
                $("#que").click(function (event){
                  event.preventDefault()
                  $.ajax({
                    type: "POST",
                    url:"/commit_questions/api/",
                    dataType:"json",
                    data:{
                    question_id: parseInt(questionData[0]),
                      exam_id: examId,
                    },
                    success: function(response){
                      console.log("Questions committed successfully:", response);
                    },
                    error: function(error){
                      console.error("Error committing questions:", error);
                      alert("提交试题时出错，请稍后再试。");
                    }
                  });
              })
            });
          },
          error: function (error) {
            // 处理请求失败的情况
            console.error("Error fetching questions:", error);
            alert("获取试题时出错，请稍后再试。");
          }
        });
      },
      error: function (error) {
        // 处理POST请求失败的情况
        // console.error("Error setting exam:", error);
        alert("设置考试时出错，请稍后再试。");
      }
    });
  });
});
