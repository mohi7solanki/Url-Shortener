function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    var $myForm = $('.my-ajax-form')
    $myForm.submit(function(event){
        event.preventDefault()
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr('data-url')
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError,
        })
    })

    function handleFormSuccess(data, textStatus, jqXHR){
        var url = data.message
        $("#foo").attr('value',url);
        $("#copy-button").attr('data-clipboard-text',url);
        $(".form").remove();
        $(".shorten_url").fadeIn("slow");
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
    	var urlError = jqXHR.responseJSON.url
    	if (urlError) {
    		urlError = urlError[0]
    		$("#id_url").addClass("is-invalid");
    		$(".invalid_url").html(urlError);
    	}
    	else{
    		$("#id_url").removeClass("is-invalid");
    		$(".invalid_url").empty();
    		$("#id_url").addClass("is-valid");
    	}
    	var shortUrlError = jqXHR.responseJSON.short_url
    	if (shortUrlError) {
    		shortUrlError = shortUrlError[0]
    		$("#id_short_url").addClass("is-invalid");
    		$(".invalid_short_url").html(shortUrlError);
    	}
    	else{
    		$("#id_short_url").removeClass("is-invalid");
    		$(".invalid_short_url").empty();
    		$("#id_short_url").addClass("is-valid");
    	}
    }
})