;(function(){
var ws;
aw = function(){
};

init = function(wspath) {
ws = new WebSocket(wspath);
};

send = function(value) {
ws.send(value);
};

onupdate = function(callback){
ws.onmessage = callback;
};

onerror = function(callback){
ws.onerror = callback;
}

onclose = function(callback){
ws.onclose = callback;
}

close = function() {
ws.close();
};

aw.init = init;
aw.send = send;
aw.onupdate = onupdate;
aw.onerror = onerror;
aw.onclose = onclose;
aw.close = close;

if(!window.aw) {
window.aw = aw;
} else {
window.anywalker = aw;
};
})();

