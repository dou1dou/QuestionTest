$(document).ready(function () {
  function updateQuestions() {
    const choices = ['A', 'B', 'C', 'D'];
    $.ajax({
      url: '/get_mistakes/api/',
      type: 'GET',
      dataType: 'json',
      success: function (data) {
        if (data.error || data.noquestions) {
          $('#questions ul').html('<li>没有错题数据</li>');
          return;
        }
        $('#questions ul').empty();
        $.each(data.questions, function (index, questionData) {
          const answer = questionData[6];

          const isMultipleChoice = answer.length > 1;
          const questionElement = $('<li></li>');
          questionElement.attr('data-question-id', questionData[0]);

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

              const buttonContainer = $('<div class="button-container"></div>');

              const checkButton = $('<button class="check-answer">提交</button>');
              const hasLearned = $('<button class="hasLearnt">已会</button>');
              const answerElement = $('<p class="answer-feedback"></p>');

              // 将按钮添加到容器中
              buttonContainer.append(checkButton);
              buttonContainer.append(hasLearned);

              // 将容器和答案元素添加到问题元素中
              questionElement.append(buttonContainer);
              questionElement.append(answerElement);

              $('#questions ul').append(questionElement);
              $('#questions ul').append('<hr>');

          checkButton.click(function () {
            if (isMultipleChoice) {
              const selectedOptions = $(`input[name="options-${index}"]:checked`).map(function () {
                return $(this).val();
              }).get();

              if (selectedOptions.length === 0) {
                alert('请选择答案！');
                return;
              }

              const isAllCorrect = selectedOptions.length === answer.length && selectedOptions.every(option => answer.includes(option));
              if (isAllCorrect) {
                answerElement.text('答案正确');
                let result = selectedOptions;
              } else {
                answerElement.html(`答案错误，正确答案是：<span class="correct-answer">${answer}</span>`);
                let result = selectedOptions;
              }
            } else {
              const selectedOption = $(`input[name="options-${index}"]:checked`).val();

              if (selectedOption === undefined) {
                alert('请选择答案！');
                return;
              }

              if (selectedOption === answer) {
                answerElement.text('答案正确');
              } else {
                answerElement.html(`答案错误，正确答案是：<span class="correct-answer">${answer}</span>`);
              }
            }
          });
        });
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error("AJAX error: " + textStatus + ' : ' + errorThrown);
        $('#questions ul').html('<li>加载错题时出错</li>');
      }
    });
  }

  $('#questions ul').on('click', '.hasLearnt', function () {
    const questionElement = $(this).closest('li');

    // 从 data-question-id 属性中获取题目 ID
    const questionId = questionElement.attr('data-question-id');

    if (confirm('确定要将此题标记为已会并从错题本中移除吗？')) {
      $.ajax({
        url: '/delete_mistakes/api/',  // 替换为你的删除 API 地址
        type: 'POST',
        data: { question_id: questionId },
        dataType: 'json',
        success: function (response) {
          if (response.success) {
            questionElement.remove(); // 从页面上移除题目
          } else {
            alert('删除题目失败：' + response.error);
          }
        },
        error: function (jqXHR, textStatus, errorThrown) {
          console.error("AJAX error: " + textStatus + ' : ' + errorThrown);
          alert('删除题目时发生错误');
        }
      });
    }
  });


  updateQuestions();
});