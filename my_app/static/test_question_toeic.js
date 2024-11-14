const ResultStatus = {
    PASS: "PASS",
    FAILED: "FAILED",
    UNTESTED: "UNTESTED"
};

var list_question_in_set = null;
var number_screen = 0;
var list_vocabulary = null;
var number_question = 0;
const element_question = document.getElementById("question_toeic");
const element_answerA = document.getElementById("answer_a");
const element_answerB = document.getElementById("answer_b");
const element_answerC = document.getElementById("answer_c");
const element_answerD = document.getElementById("answer_d");

async function GetListQuestionInSet() {
    const url = "/question_toeic/test_question_toeic";
    const data = {
        "set_question_id": set_question_id
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

async function GetListVocabulary() {
    const url = "/question_toeic/list_vocabulary";
    const data = {
        "token": "this is token"
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

async function LoadPageQuestion() {
    try {
        let data = await GetListQuestionInSet();
        list_question_in_set = data["set_question"]["list_question"].split("_");
        data = await GetListVocabulary();
        list_vocabulary = data["list_vocabulary"];
        element_question.innerText = list_vocabulary[list_question_in_set[10]]["word"] + "            " + list_vocabulary[list_question_in_set[10]]["transliteration"];
        element_answerA.textContent = list_vocabulary[list_question_in_set[10]]["mean1"];
        element_answerB.textContent = list_vocabulary[599]["mean1"];
        element_answerC.textContent = list_vocabulary[400]["mean1"];
        element_answerD.textContent = list_vocabulary[300]["mean1"];
    } catch (error) {
        console.error("Error:", error);
    }
}

function UpdateResult(result) {
    if (Object.values(ResultStatus).includes(result)) {
        const data = {
            username: user_name,
            set_question_id: set_question_id,
            result: result
        };

        const url = "/question_toeic/update_result";
        fetch(url, {
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
                    const url_direct = `/question_toeic/get_test_question?user_name=${data.username}`;
                    window.location.href = url_direct;
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
    else {
        alert("Can not update result");
    }
}


window.onload = function () {
    LoadPageQuestion();
};