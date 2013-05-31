var item_url = web_base + "api/item";
$(document).ready(function() {
  showHopper();
  $('#share-form').submit(function() {
    var title = $('#title').val();
    var url = $('#url').val();
    var creator = $('#creator').val();
    var description = $('#description').val();
    $.post(item_url, {title: title, creator: creator, link: url, description: description}, function(data) {
      $('#share-form input, #share-form textarea').each(function() {
            $(this).val('');
      });
      $('#result').html('<h4>' + data.response + '</h4>');
      showHopper();
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

function showHopper() {
  $.getJSON(item_url + '/recent?callback=?', function(data) {
    var items = [];
    $.each(data, function(key, val) {
      items.push('<p><a href="' + val.link + '">' + val.title + '</a><br>' + val.description + '<br><small>- ' + val.creator + '</small>');
    });
    var ul = items.join('');
    
    $('#hopper').html(ul);
});
}
