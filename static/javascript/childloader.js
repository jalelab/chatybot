window.onload = function() {
    document.getElementById("jsoneditor").onclick = function() {
        doWork()
    };
}

function childloader(){
  $.get("http://127.0.0.1:5000/jsoneditor")


}





$(function () {
   $('editor').click(function(){
    $.get("/jsoneditor",
    function(data) {
       console.log("data");
       console.log(data);
       $("#container").html(data);
    });
    console.log("error");;
  });
});

onclick="loadchild('editor')"

$("#jsoneditor").click(function() {
  $.get("/jsoneditor", function(data) {
      document.open('text/html');
      document.write(data);
      document.close();
    }
}


addfiles('script'){
  $.get(script).done(function (data) {
    $("#jsoneditor").html(data);
  })
}



const blob = new Blob([editor.getText()], {type: 'application/json;charset=utf-8'})
