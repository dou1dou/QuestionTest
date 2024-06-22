$(document).ready(function () {
    let currentKnowledgePoint = null;
    let currentDifficulty = 1;


    function updateQuestions() {
        const choices = ['A', 'B', 'C', 'D'];
        $.ajax({
            url: '/questions/api/',
            type: 'GET',
            dataType: 'json',
            data: {
                Knowledge_points: currentKnowledgePoint,
                Difficulty: currentDifficulty
            },
            success: function (data) {
                $('#questions ul').empty();
                $.each(data, function (index, questionData) {
                    const answer = questionData[6];
                    const isMultipleChoice = answer.length > 1;
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

                    const checkButton = $('<button class="check-answer">提交</button>');
                    const answerElement = $('<p class="answer-feedback"></p>');
                    questionElement.append(checkButton);
                    questionElement.append(answerElement);

                    $('#questions ul').append(questionElement);
                    $('#questions ul').append('<hr>');

                    checkButton.click(function () {
                        if (isMultipleChoice) {
                            const selectedOptions = $(`input[name="options-${index}"]:checked`).map(function () {
                                return $(this).val();
                            }).get();

                            // 检查是否选择了答案
                            if (selectedOptions.length === 0) {
                                alert('请选择答案！');
                                return;
                            }

                            // 检查是否所有选项都选对
                            const isAllCorrect = selectedOptions.length === answer.length && selectedOptions.every(option => answer.includes(option));
                            if (isAllCorrect) {
                                answerElement.text('答案正确');
                                let result = "";
                                for(let i = 0; i < selectedOptions.length; i++){
                                    result += selectedOptions[i];
                                }
                                $.ajax({
                                    url: '/questions/store/api/',
                                    type: 'POST',
                                    dataType: 'json',
                                    data: {
                                        question_id: questionData[0],
                                        choices: result, // 发送数组
                                        correct: 0
                                    },
                                    success: function (data) {
                                        console.log('post成功');
                                    },
                                    error: function (error) {
                                        console.error('post失败:', error);
                                    }
                                });
                            } else {
                                answerElement.html(`答案错误，正确答案是：<span class="correct-answer">${answer}</span>`);
                                let result = "";
                                for(let i = 0; i < selectedOptions.length; i++){
                                    result += selectedOptions[i];
                                }
                                $.ajax({
                                    url: '/questions/store/api/',
                                    type: 'POST',
                                    dataType: 'json',
                                    data: {
                                        question_id: questionData[0],
                                        choices: result, // 发送数组
                                        correct: 1
                                    },
                                    success: function (data) {
                                        console.log('post成功');
                                    },
                                    error: function (error) {
                                        console.error('post失败:', error);
                                    }
                                });
                            }
                        } else {
                            const selectedOption = $(`input[name="options-${index}"]:checked`).val();

                            // 检查是否选择了答案
                            if (selectedOption === undefined) {
                                alert('请选择答案！');
                                return;
                            }

                            if (selectedOption === answer) {
                                answerElement.text('答案正确');
                                $.ajax({
                                    url: '/questions/store/api/',
                                    type: 'POST',
                                    dataType: 'json',
                                    data: {
                                        question_id: questionData[0],
                                        choices: selectedOption, // 发送数组
                                        correct: 0
                                    },
                                    success: function (data) {
                                        console.log('post成功');
                                    },
                                    error: function (error) {
                                        console.error('post失败:', error);
                                    }
                                });
                            } else {
                                answerElement.html(`答案错误，正确答案是：<span class="correct-answer">${answer}</span>`);
                                $.ajax({
                                    url: '/questions/store/api/',
                                    type: 'POST',
                                    dataType: 'json',
                                    data: {
                                        question_id: questionData[0],
                                        choices: selectedOption, // 发送数组
                                        correct: 1
                                    },
                                    success: function (data) {
                                        console.log('post成功');
                                    },
                                    error: function (error) {
                                        console.error('post失败:', error);
                                    }
                                });
                            }
                        }
                    });
                });
            },
            error: function (error) {
                alert('获取题目出错:' + error);
            }
        });
    }

    // 假设按钮和下拉菜单的 HTML 结构与之前相同
    $('.button-css button').on('click', function () {
        if ($(this).data('knowledge-point').length !== 0 && $(this).data('knowledge-point') !== null) {
            currentKnowledgePoint = $(this).data('knowledge-point');
        } else {
            currentKnowledgePoint = null;
        }
        updateQuestions();
    });

    $('#difficulty').on('change', function () {
        if ($(this).val().length !== 0) {
            currentDifficulty = $(this).val();
        } else {
            currentDifficulty = 1;
        }
        updateQuestions();
    });

    updateQuestions();

    $(".chart").click(function () {
        window.location.href = "/personal/"
    })


    function updateTests() {
        $.ajax({
            url: '/tests/api/',  // 假定这是获取测试列表的API端点
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                const testsList = $('#tests ul');
                testsList.empty();  // 清空现有的测试列表

                // 遍历返回的测试列表数据
                $.each(data, function (index, testData) {
                    // 假设每个测试数据包含id和title
                    const testId = testData.id;
                    const testTitle = testData.title;

                    // 创建列表项并添加到<ul>中
                    const listItem = $(`<li id="test-${testId}">${testTitle}</li>`);
                    testsList.append(listItem);
                });
            },
            error: function (error) {
                console.error('获取测试列表出错:', error);
                alert('获取测试列表失败，请稍后重试。');
            }
        });
    }

    // 调用updateTests函数来加载并显示测试列表
    updateTests();
});