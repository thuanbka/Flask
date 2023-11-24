var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat/simple');
    socket.on('chat', function(msg){
        var ul = document.getElementById('messages');
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(msg));
        ul.appendChild(li);
    });
});

document.getElementById('send').onclick = function(){
    var message = document.getElementById('message_input').value;
    socket.emit('chat_simple', message);
    document.getElementById('message_input').value = '';
    return false;
};