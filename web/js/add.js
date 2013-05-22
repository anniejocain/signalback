$(document).ready(function() {
  $('#share-form').submit(function() {
    var post_url = web_base + "api/item";
    var title = $('#title').val();
    var url = $('#url').val();
    var creator = $('#creator').val();
    var description = $('#description').val();
    $.post(post_url, {title: title, creator: creator, link: url, description: description}, function(data) {
      $('#share-form input, #share-form textarea').each(function() {
            $(this).val('');
      });
      $('#result').html('<h4>' + data.response + '</h4>');
    });
  return false;	
	});
	
	$('#bookmarklet-name').keyup(function() {
	  var name = $(this).val();
	  var bookmarklet = "javascript:(function(){%20window.open(%22" + web_base + "add?link=%22+encodeURIComponent(%20location.href)+%22&title=%22+encodeURIComponent(document.title)+%22&name=" + name + "%22);%20})();"
	  $("#bookmarklet").attr('href', bookmarklet);
	});
	
	$('#get').collapse("hide");
});
