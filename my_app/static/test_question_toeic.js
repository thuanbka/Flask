const ResultStatus = {
    PASS: "PASS",
    FAILED: "FAILED",
    UNTESTED: "UNTESTED"
};

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
            .then(data => {
                console.log("Response from server:", data);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }
    else {
        alert("Can not update result");
    }
}