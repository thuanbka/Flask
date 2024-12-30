const ResultStatus = {
    PASS: "PASS",
    FAILED: "FAILED",
    UNTESTED: "UNTESTED"
};

const MAX_ERROR = 3;
const MAX_LEVEL = 3;
const MAX_TOTAL_ERROR = 5;
var list_question_in_set = null;
var number_screen = 0;
var list_vocabulary = null;
var length_list_vocabulary = 0;
var number_question = 0;
var length_question = 0;
var answer_correct = 0;
var has_answer = false;
var level_test = 1;
var question_test = 0;
var list_count_error = [0, 0, 0, 0];
const element_question = document.getElementById("question_toeic");
const element_answerA = document.getElementById("answer_a");
const element_answerB = document.getElementById("answer_b");
const element_answerC = document.getElementById("answer_c");
const element_answerD = document.getElementById("answer_d");
const list_element =[element_answerA, element_answerB, element_answerC, element_answerD];
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

function SetAnswerUI(answer_number, data){
    switch(answer_number){
        case 0:
            element_answerA.textContent = data;
            break;
        case 1:
            element_answerB.textContent = data;
            break;
        case 2:
            element_answerC.textContent = data;
            break;
        case 3:
            element_answerD.textContent = data;
            break;
    }
}

function GetRandomAnswer(answer){
    let x = Math.floor(Math.random()*4);
    for(let i =0;i<4;i++)
    {
        if(i!=x)
        {
            let random = answer;
            while(random == answer){
                random =  Math.floor(Math.random()*length_list_vocabulary);
            }
            switch(level_test){
                case 1: 
                    SetAnswerUI(i, list_vocabulary[random]["mean1"]);
                    break;
                case 2:
                    SetAnswerUI(i, list_vocabulary[random]["word"]);
                    break;
                case 3:
                    SetAnswerUI(i, list_vocabulary[random]["transliteration"]);
                    break;
            }
        }
    }
    switch(level_test){
        case 1: 
            SetAnswerUI(x, list_vocabulary[answer]["mean1"]);
            break;
        case 2:
            SetAnswerUI(x, list_vocabulary[answer]["word"]);
            break;
        case 3:
            SetAnswerUI(x, list_vocabulary[answer]["transliteration"]);
            break;
    }
    answer_correct = x;
}

async function ClearUIButton(){
    for(let i =0;i<list_element.length;i++)
    {
        list_element[i].classList.remove("answer_correct");
        list_element[i].classList.remove("answer_fail");
    }
}


async function UpdateUIQuestion(level, answer){
    level_test = level;
    await ClearUIButton();
    has_answer = false;
    switch(level){
        case 1: 
            element_question.innerText = list_vocabulary[list_question_in_set[answer]]["word"] + "\n-----------\n" + list_vocabulary[list_question_in_set[answer]]["transliteration"];
            GetRandomAnswer(list_question_in_set[answer]);
            break;
        case 2:
            element_question.innerText = list_vocabulary[list_question_in_set[answer]]["mean1"];
            GetRandomAnswer(list_question_in_set[answer]);
            break;
        case 3:
            element_question.innerText = list_vocabulary[list_question_in_set[answer]]["mean1"];
            GetRandomAnswer(list_question_in_set[answer]);
            break;
    }
}

async function LoadPageQuestion() {
    try {
        let data = await GetListQuestionInSet();
        list_question_in_set = data["set_question"]["list_question"].split("_");
        length_question = list_question_in_set.length;
        data = await GetListVocabulary();
        list_vocabulary = data["list_vocabulary"];
        length_list_vocabulary = list_vocabulary.length;
        level_test = 1;
        question_test = 0;
        UpdateUIQuestion(level_test, question_test);
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

async function Check_Answer(id ,answer){

    let button_element = document.getElementById(id);
    let time_out = 1000;
    if(has_answer == false){
        has_answer = true;
        if(answer == answer_correct)
        {
            button_element.classList.add("answer_correct");
        }
        else{
            list_count_error[level_test]++;
            button_element.classList.add("answer_fail");
            list_element[answer_correct].classList.add("answer_correct");
        }
        question_test++;
        if(question_test>=length_question){
            if(list_count_error[level_test] < MAX_ERROR){
                let text = "Happy pass level " + level_test  + "!";
                text += "\n";
                text += "Result: " + (length_question - list_count_error[level_test]) + "/" + length_question
                alert(text);
                level_test += 1;
                if(level_test > MAX_LEVEL){
                    await HandleEndTest();
                    return;
                }
            }
            else{
                let text = "Test again!";
                text += "\n";
                text += "Failed: " + list_count_error[level_test] + "/" + length_question
                alert(text);
                list_count_error[level_test] = 0;
            }
            question_test = 0;
        }
        setTimeout(UpdateUIQuestion, time_out, level_test, question_test);
    }
}

async function HandleEndTest(){

    let total_count_error = 0;
    let status = UpdateResult(ResultStatus.UNTESTED);
    for(let i =0; i<MAX_LEVEL;i++)
    {
        total_count_error += list_count_error[i];
    }
    
    if(total_count_error > MAX_TOTAL_ERROR){
        let text = "Test Failed!";
        text += "\n";
        text += "Failed: " + total_count_error;
        alert(text);
        status = ResultStatus.FAILED;
    }
    else{
        let text = "Test Passed!";
        text += "\n";
        text += "Happy you!";
        status = ResultStatus.PASS;
    }
    await UpdateResult(status);
    return;
}


window.onload = function () {
    LoadPageQuestion();
};