$('#imageModal').on('show.bs.modal', function (event) {
  var image_src = $(event.relatedTarget) // Button that triggered the modal
  var parent = image_src.parent().parent()
  var source = image_src.attr('original-image')
  var modal = $(this)
  var name = parent.find('h3').text()
  var description = parent.find('p').text()
  var image = modal.find('img')
  var modal_name = modal.find('#name')
  var modal_description = modal.find('#description')
  image.attr('src', source)
  modal_name.html(name)
  modal_description.html(description)
  var thumbnail = $('.thumbnail')
  $('.thumbnail').each(function(i, v) {
    var self = $(this)
    var modal_image = $('#modal-image')
    if (self.find('#gallery-image').attr('original-image') == modal_image.attr('src')) {
      if (i == 0 ) {
        $('.previous').css('display', 'none');
      } else if ((i+1) == thumbnail.length) {
        $('.next').css('display', 'none'); 
      }
    }
  });
});

$('#imageModal').on('hidden.bs.modal', function (event) {
  if ($('.previous').css('display') == 'none' ){
    $('.previous').css('display', 'inline-block');
  } else if ( $('.next').css('display') == 'none' ) {
    $('.next').css('display', 'inline-block');
  }
});

function next_img() {
  var thumbnail = $('.thumbnail');
  if ($('.previous').css('display') == 'none' ){
    $('.previous').css('display', 'inline-block');
  }
  $('.thumbnail').each(function(i, v){
    var self = $(this)
    var modal_image = $('#modal-image')
    if (self.find('#gallery-image').attr('original-image') == modal_image.attr('src')) {
        if ((i+1) == thumbnail.length) {
          // alert("No more image");
          return false;
        }
        next_image = $(thumbnail[i+1]).find('#gallery-image').attr('original-image')
        next_name = $(thumbnail[i+1]).find('#gallery-name').text()
        next_description = $(thumbnail[i+1]).find('#gallery-name').text()
        $('#modal-image').attr('src', next_image)
        $('#name').html(next_name)
        $('#description').html(next_description)
        if ((i+2) == thumbnail.length) {
          $('.next').css('display', 'none');
          return false;
        } else if ($('.previous').css('display') == 'none' ){
          $('.previous').css('display', 'inline-block');
        }        
        return false;
      } 
    });
};

function previous_image() {
  var thumbnail = $('.thumbnail');
  if ($('.next').css('display') == 'none' ){
    $('.next').css('display', 'inline-block');
  }
  $('.thumbnail').each(function(i, v){
    var self = $(this)
    var modal_image = $('#modal-image')
    if (self.find('#gallery-image').attr('original-image') == modal_image.attr('src')) {
      if (i == 0) {
        // alert("No more image");
        return false;
      }
      prev_image = $(thumbnail[i-1]).find('#gallery-image').attr('original-image')
      prev_name = $(thumbnail[i-1]).find('#gallery-name').text()
      prev_description = $(thumbnail[i-1]).find('#gallery-name').text()
      $('#modal-image').attr('src', prev_image)
      $('#name').html(prev_name)
      $('#description').html(prev_description)
      if (i == 1) {
        $('.previous').css('display', 'none');
          return false;
      }      
      return false;
    } 
  });
};

$(document).ready(function() {  
  $("body").on('keydown',function(e) {
  if(e.keyCode == 37) {
    previous_image();
  } // left
  });
});

$(document).ready(function() {
  $("body").keydown(function(e) {
  if(e.keyCode == 39) {
    next_img();
    } // right
  });
});

$(document).ready(function() {
  $(".next").on("click", next_img);
});

$(document).ready(function() {
  $(".previous").on("click", previous_image);
});
