$(document).ready(function() {
  $('#chat-toggle').on('click', function() {
    $('#chat-container').slideToggle();
  });

  $('#chat-close').on('click', function() {
    $('#chat-container').slideUp();
  });
}); 