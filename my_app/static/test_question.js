const ResultStatus = {
    PASS: "PASS",
    FAILED: "FAILED",
    UNTESTED: "UNTESTED"
};

var list_set_questions = null;

async function GetListSetQuestion() {
    const url = "/question_toeic/get_test_question";
    const data = {
        "user_name": user_name
    };
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            else {
                return response.json();
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

async function LoadPageListQuestion() {
    try {
        let data = await GetListSetQuestion();
        list_set_questions = data["list_set_questions"]
        console.log(list_set_questions);
        LoadUIListQuestion();
    } catch (error) {
        console.error("Error:", error);
    }
}

function LoadUIListQuestion() {
    let test_question_element = document.getElementById("list-test-question");
    let number_question_element = document.getElementById("number_question");
    number_question_element.textContent = list_set_questions.length;
    for (var i = 0; i < list_set_questions.length; i++) {
        var button = document.createElement("button");
        button.innerHTML = "Set " + (i + 1);
        button.id = "set_" + (i + 1);
        button.onclick = (function (set_question) {
            return function () {
                ClickButtonSetQuestion(set_question);
            };
        })(list_set_questions[i]);
        if (list_set_questions[i].result == ResultStatus.UNTESTED) {
            button.style.backgroundColor = "#ffffcc";
        }
        if (list_set_questions[i].result == ResultStatus.FAILED) {
            button.style.backgroundColor = "#ff0000";
        }
        if (list_set_questions[i].result == ResultStatus.PASS) {
            button.style.backgroundColor = "green";
        }
        test_question_element.appendChild(button);
    }
}


function ClickButtonSetQuestion(set_question) {
    const baseUrl = "/question_toeic/test_question_toeic";
    const data = {
        user_name: user_name,
        set_question_id: set_question.id,
        list_question: set_question.list_question
    };

    const url = `${baseUrl}?user_name=${data.user_name}&set_question_id=${data.set_question_id}`;
    window.location.href = url;
}


window.onload = function () {
    LoadPageListQuestion();
};