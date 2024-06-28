$(document).ready(function() {
    function fetchExamList() {
        $.ajax({
            url: "/exam/list/api/",
            type: "GET",
            dataType: "json",
            success: function(response) {
                const exams = response.data;
                const examList = $("#tests ul");
                examList.empty();

                $.each(exams, function(index, exam) {
                    const examItem = $(`
                        <li class="exam-item" data-exam-id="${exam['exam-id']}">
                            <p class="exam-id">考试编号：${exam['exam-id']}</p>
                            <p class="exam-title">考试标题：${exam['exam-name']}</p>
                            <p class="exam-time">考试时间：${exam['exam-time']}分钟</p>
                        </li>
                    `);
                    examItem.on('click', function() {
                        fetchExamQuestions($(this).data('exam-id'));
                    });
                    examList.append(examItem);
                });
            },
            error: function(xhr, status, error) {
                console.error("获取考试信息失败：", error);
            }
        });
    }

    function fetchExamQuestions(examId) {
        $.ajax({
            url: '/exam/question/api/',
            type: 'GET',
            dataType: 'json',
            data: { 'exam-id': examId },
            success: function(response) {
                const questions = response.data;
                const questionList = $('#questions ul');
                questionList.empty();

                $.each(questions, function(index, questionData) {
                    const questionElement = $(`
                        <li>
                            <p class="questions-desc-css">${index + 1}、${questionData[1]}</p>
                            ${generateChoiceElements(questionData).join('')}
                            <button class="check-answer">提交</button>
                            <p class="answer-feedback"></p>
                        </li>
                    `);

                    questionElement.find('.check-answer').on('click', function() {
                        checkAnswer(questionElement, questionData);
                    });

                    questionList.append(questionElement);
                    questionList.append('<hr>');
                });

                questionList.append('<button id="submit-all" class="submit-all-css">提交全部答案</button>');
                $('#submit-all').on('click', submitAllAnswers);
            },
            error: function(error) {
                alert('获取题目出错: ' + error);
            }
        });
    }

    function generateChoiceElements(questionData) {
        const choices = ['A', 'B', 'C', 'D'];
        const isMultipleChoice = questionData[6].length > 1; // Assuming the correct answers are in questionData[6]
        return choices.map((choice, i) => {
            return questionData[i + 2] ? `
                <div class="questions-choice-css" style="display: flex">
                    <div class="choice-btn">
                        <input type="${isMultipleChoice ? 'checkbox' : 'radio'}" id="option${i + 1}" name="options-${questionData[0]}" value="${choice}">
                    </div>
                    <div class="choice-content">${questionData[i + 2]}</div>
                </div>
            ` : '';
        });
    }

    function checkAnswer(questionElement, questionData) {
        const selectedOptions = questionElement.find(`input[name="options-${questionData[0]}"]:checked`).map(function() {
            return $(this).val();
        }).get();
        const answerFeedback = questionElement.find('.answer-feedback');
        const correctAnswer = questionData[6]; // Assuming the correct answers are in questionData[6]

        if (selectedOptions.length === 0) {
            alert('请选择答案！');
            return;
        }

        const isAllCorrect = selectedOptions.length === correctAnswer.length && selectedOptions.every(option => correctAnswer.includes(option));

        if (isAllCorrect) {
            answerFeedback.text('答案正确');
        } else {
            answerFeedback.html(`答案错误，正确答案是：<span class="correct-answer">${correctAnswer}</span>`);
        }

        $.ajax({
            url: '/questions/store/api/',
            type: 'POST',
            dataType: 'json',
            data: {
                question_id: questionData[0],
                choices: selectedOptions.join(''), // Sending as a concatenated string for multiple-choice
                correct: isAllCorrect ? 1 : 0 // 1 means correct, 0 means incorrect
            },
            success: function(data) {
                console.log('答案提交成功');
            },
            error: function(error) {
                console.error('答案提交失败:', error);
            }
        });
    }

    function submitAllAnswers() {
        let allAnswered = true;

        $('#questions ul li').each(function() {
            const inputs = $(this).find('input');
            if (inputs.length > 0 && !inputs.is(':checked')) {
                allAnswered = false;
                return false;
            }
        });

        if (!allAnswered) {
            alert('请回答所有问题后再提交！');
            return;
        }

        let score = 0;
        $('.check-answer').each(function() {
            $(this).click();
            if ($(this).next('.answer-feedback').text().includes('答案正确')) {
                score += 5;
            }
        });

        const resultMessage = `你的总分是：${score} 分，满分为 100 分。${score === 100 ? ' 恭喜你，满分！' : ''}`;
        $('#questions ul').append(`<p class="total-score">${resultMessage}</p>`);
    }

    fetchExamList();

    $(".chart").click(function() {
        window.location.href = "/personal/";
    });

});
