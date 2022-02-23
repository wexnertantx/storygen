
$("button").click(function(){
  $("#form-container").hide(1000);
  $("#suggest").hide(1000);
  $('#loader').show(1000);
});

var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}