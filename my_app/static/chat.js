var url_home = 'https://' + document.domain;
// var url_home = 'https://' + document.domain + ':' + location.port
var socket = io.connect(url_home + "/chat/simple");

socket.on('connect', function() {
    socket.emit('joined', {});
});

socket.on('chat', function(msg){
    var ul = document.getElementById('messages');
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(msg));
    ul.appendChild(li);
});

document.getElementById('send').onclick = function(){
    var message = document.getElementById('message_input').value;
    socket.emit('chat_simple', message);
    document.getElementById('message_input').value = '';
    return false;
};

document.getElementById('leave_room').onclick = function(){
    console.log("leave_room")
    socket.emit('left', {}, function() {
        socket.disconnect();
        window.location.href = url_home;
    });
};