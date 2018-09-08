window.onload = (function(){
    get_questions();
      
}());

function get_questions(){
    

    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/questions';
    let question_list = "";
    fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        //mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json;"
            // "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then((resp) => resp.json())
    .then(function(data) {
        data.Questions.forEach(element => {
            question_list += '<table class="table"><tr class="warning borderless"><td><div class = "question"><a href="#" onclick = "view_question_and_answers('+element.questionId+')"><h4>'+ element.question +'</h4></a></div><div class = "answer"><a href="#"class = "btn btn-primary" onclick ="get_question('+element.questionId+');">answer</a><p class = "asked">modified '+element.createdOn+' posted by '+element.username+'</p></div></td></tr></table>'
        });
        document.getElementById('ask-question').style.display = "none";
        document.getElementById('answer-question-box-1').style.display = "none";
        document.getElementById('question-and-answers').style.display = "none";
        document.getElementById('question-and-answers').style.display = "none";
        var div = document.getElementById('questions-table-box');
        document.getElementById('answer-question-box').style.display = "none";
        document.getElementById('question-box').style.display = "block";
        div.innerHTML = question_list;
    })
    .catch(function(error) {
    console.log(error);
    }); 
}
function get_answer(answerId){
    document.getElementById('question-and-answers').style.display = "none";
    document.getElementById('ask-question').style.display = "none";
    if(!answerId){
        return null;
    }

    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/questions';
    // The parameters we are gonna pass to the fetch function

    let question_list = "";
    fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        //mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json;"
            // "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then((resp) => resp.json())
    .then(function(data) {
        data.Questions.forEach(element => {
            question_list += '<tr class="warning borderless"><td><div class = "question"><a href = "question.html"><h4>'+ element.question +'</h4></a></div><div class = "answer"><a class = "btn btn-primary">answer</a><p class = "asked">modified '+element.createdOn+' Nevi</p></div></td></tr>'
        });
        var div = document.getElementById('question-table');
        div.innerHTML = question_list;
    })
    .catch(function(error) {
    console.log(error);
    }); 

}

function get_question(questionId){
    document.getElementById('answer-question-box-1').style.display = "block";
    document.getElementById('question-and-answers').style.display = "none";
    document.getElementById('ask-question').style.display = "none";
    
    document.getElementById('answer-res').style.display = "none";
    document.getElementById('add-answer-response').style.display = "none";
    document.getElementById('page-title').innerHTML = 'Add answer to question';
    document.getElementById('question-box').style.display = "none";
    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/questions/'+questionId;
    let question = "";
    fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        //mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json;"
            // "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then((resp) => resp.json())
    .then(function(data) {
        question = data.Question.question;
        document.getElementById('answer-question-box').style.display = "block";
        document.getElementById('userId').innerHTML = '<input type="hidden" name="userId" value="'+ data.Question.userId +'"/>';
        document.getElementById('questionId').innerHTML = '<input type="hidden" name="questionId" value="'+ data.Question.questionId +'"/>'
        document.getElementById('answer_submit').innerHTML = '<a class="btn btn-primary float-right" onclick="answer_question('+data.Question.questionId+');">post answer</a>';
        var div = document.getElementById('question-to-answer');
        div.innerHTML = '<p>'+ question +'</p>';
    })
    .catch(function(error) {
    console.log(error);
    }); 
}

function answer_question(questionId){
    document.getElementById('answer-question-box-1').style.display = "block";
    document.getElementById('question-and-answers').style.display = "none";
    document.getElementById('add-answer-response').style.display = "none";
    document.getElementById('ask-question').style.display = "none";
    document.getElementById('page-title').innerHTML = 'Add answer to question'
    document.getElementById('question-box').style.display = "none";
    document.getElementById('answer-res').style.display = "none";
    let object = {};
    let form = document.getElementById('answer-form');
    let formData = new FormData(form);
    formData.forEach(function(value, key){
        object[key] = value;
    });
    let jsonData = JSON.stringify(object);
    console.log(object);
    console.log(jsonData);
    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/'+questionId+'/answers';
    let question = "";
    fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        //mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json;"
            //"Content-Type": "application/x-www-form-urlencoded",
        },
        body: jsonData
    })
    .then((resp) => resp.json())
    .then(function(data) {
        console.log(data.Message);
        question = data.Question.question;
        document.getElementById('answer-question-box').style.display = "block";
        document.getElementById('add-answer-response').style.display = "block";
        document.getElementById('answer-res').style.display = "block";
        var div = document.getElementById('question-to-answer');
        div.innerHTML = '<p>'+ question +'</p>';

        let header = document.createElement("h2"); 
        let paragraph = document.createElement("p"); 
        let paragraph_node = document.createTextNode(data.Answer.answer);               // Create a <li> node
        let header_node = document.createTextNode(data.Message);         // Create a text node
        paragraph.appendChild(paragraph_node); 
        header.appendChild(header_node);    
        console.log(header)                         // Append the text to <li>
        document.getElementById('add-answer-response').appendChild(header); 
        document.getElementById('add-answer-response').appendChild(paragraph);  
        node.appendChild()
        document.getElementById('answer-res').style.display = "block";
    })
    .catch(function(error) {
    console.log(error);
    }); 
}
function ask_question(){
    
    document.getElementById('question-and-answers').style.display = "none";
    document.getElementById('add-answer-response').style.display = "none";
    document.getElementById('question-box').style.display = "none";
    document.getElementById('ask-question').style.display = "block";
    document.getElementById('answer-question-box-1').style.display = "none";
    document.getElementById('question-and-answers').style.display = "none";
    document.getElementById('add-answer-response').style.display = "none";
    document.getElementById('page-title').innerHTML = 'Ask answer question'
}
function post_question(){
    let object = {};
    let form = document.getElementById('ask_question_form');
    let formData = new FormData(form);
    formData.forEach(function(value, key){
        object[key] = value;
    });
    let jsonData = JSON.stringify(object);
    console.log(object);
    console.log(jsonData);
    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/questions';
    fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        //mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json;"
            //"Content-Type": "application/x-www-form-urlencoded",
        },
        body: jsonData
    })
    .then((resp) => resp.json())
    .then(function(data) {
        console.log(data);
        var div = document.getElementById('ask_question_form_panel');
        div.innerHTML = '<h4>'+ data.Message +'</h4>';
    })
    .catch(function(error) {
    console.log(error);
    }); 
}

function view_question_and_answers(questionId){
    document.getElementById('question-and-answers').style.display = "none";
    document.getElementById('add-answer-response').style.display = "block";
    document.getElementById('page-title').innerHTML = 'Answers to question';
    document.getElementById('question-box').style.display = "none";
    const url = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1/questions/questions/'+questionId;
    let question = "";
    let answer_list = "";
    fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        //mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        headers: {
            "Content-Type": "application/json;"
            // "Content-Type": "application/x-www-form-urlencoded",
        }
    })
    .then((resp) => resp.json())
    .then(function(data) {
        question = data.Question.question;
        console.log(data);
        document.getElementById('question-and-answers').style.display = "block";
        var div = document.getElementById('question-answer-2');
        document.getElementById('ans_message_ff').innerHTML = '<spa>'+ data.Message +'</spa>';
        let ansList = document.getElementById('answer_lists');
        div.innerHTML = '<span>'+ question +'</span>';
        data.Answers.forEach(element => {
            answer_list += '<li><p>'+element.answer+'</p><div class="answer-action"><a class="prefer">prefer</a><a class="upvote">up vote</a><a class="downvote">down vote</a></div></li>'
        });
        
        ansList.innerHTML = answer_list;
        console.log(answer_list);
        console.log(data.Message);
    })
    .catch(function(error) {
    console.log(error);
    }); 
}