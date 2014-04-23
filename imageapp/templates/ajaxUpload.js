file_input = $('#file');
form = $('#form');

$(document).ready(function(e) {
  form.on('submit', (function(e) {
    e.preventDefault();
    var formData = new FormData(this);

    $.ajax({
      type:'POST',
      url:$(this).attr('action'),
      data:formData,
      cache:false,
      contentType:false,
      processData:false,
      success:function(data) {
        console.log('success!');
        $('#success').fadeIn()
        $('#image').attr('src', '/image_raw?special=latest')
        $('#image').attr('style', 'max-height:400px')

      },
      error:function(data) {
        console.log('error!');

      }

    });
  }));

  file_input.on('change', function() {
    form.submit();
  });
});
