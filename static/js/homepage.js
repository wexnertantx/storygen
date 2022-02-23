
$(function(){
  $('.homepage').hide();
  $('.box').delay(500).effect("bounce", { times: 8 }, 800);
  $('.box').hide().slideDown(500);
  
  
  $('button').click(function(){
    $('.intro').slideUp(400);
     $('.box').slideUp(200);
    $('.homepage').delay(500).slideDown(300);
  });
  
});