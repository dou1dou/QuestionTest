$(document).ready(function() {
  let currentKnowledgePoint = null;
  let currentDifficulty = 1;
function updateQuestions() {
  const choices = ['A', 'B', 'C', 'D'];
  $.ajax({
    url: '/questions/api/',
    type: 'GET',
    dataType: 'json',
    data: {
      Knowledge_points: currentKnowledgePoint, // 传递知识点参数
      Difficulty: currentDifficulty          // 传递难度参数
    },
    success: function(data) {
      $('#questions ul').empty();
      $.each(data, function(index, questionData) {
        const answer = questionData[6];
        const isMultipleChoice = answer.length>1; // 检查答案是否为数组(多选题)
        // 假设 API 返回的数据结构是 ["题目内容", "选项A", "选项B", "选项C", "选项D"]
        const questionElement = $('<li></li>');
        for (let i = 0; i < 5; ++i) {
          if (i === 0) {
            questionElement.append(`<p class="questions-desc-css">${parseInt(index) + 1}、${questionData[i + 1]}</p>`);
          } else if (questionData[i + 1] !== null) {
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
        $('#questions ul').append(questionElement);
        $('#questions ul').append('<hr>');
        let answerShown = false; // 标记是否已显示正确答案
        const answerElement = $(`<p class="answer-feedback"></p>`);
        $(questionElement).append(answerElement);

          if (isMultipleChoice) {
            $(`input[name="options-${index}"]`).change(function () {
              const selectedOptions = $(`input[name="options-${index}"]:checked`).map(function () {
                return $(this).val();
              }).get();
              const isAllCorrect = selectedOptions.length === answer.length && selectedOptions.every(option => answer.includes(option));
              const hasWrongOption = selectedOptions.some(option => !answer.includes(option));

              if (hasWrongOption) { // 只要有选错的选项就显示错误
                answerElement.html(`答案错误，正确答案是：<span class="correct-answer">${answer}</span>`);
              } else if (isAllCorrect) { // 所有选项都选对才显示正确
                answerElement.text('答案正确');
              } else {
                answerElement.empty(); // 其他情况（例如只选择了部分正确选项）清空提示
              }
            });
          }
         else {
          $(`input[name="options-${index}"]`).change(function() {
            const selectedOption = $(this).val();
            if (selectedOption === answer) {
              answerElement.text('答案正确');
            } else {
              answerElement.html(`答案错误，正确答案是：<span class="correct-answer">${answer}</span>`);
              answerShown = true;
            }
          });
        }
      });
    },
    error: function(error) {
      console.error('获取题目出错:', error);
    }
  });
}

  // 假设按钮和下拉菜单的 HTML 结构与之前相同
  $('.button-css button').on('click', function() {
    if($(this).data('knowledge-point').length !== 0 && $(this).data('knowledge-point') !== null) {
      currentKnowledgePoint = $(this).data('knowledge-point');
    } else {
      currentKnowledgePoint = null;
    }
    updateQuestions();
  });

  $('#difficulty').on('change', function() {
    if($(this).val().length !== 0) {
      currentDifficulty = $(this).val();
    } else {
      currentDifficulty = 1;
    }
    updateQuestions();
  });

  updateQuestions();
});