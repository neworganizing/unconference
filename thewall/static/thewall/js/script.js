/*
By Nick Catalano (@nickcatal), Tim Anderegg (@tanderegg)

Copyright 2012 New Organizing Institute
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0

*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function($) {
    /*$('.session-link').click(function () {
        var session_id = $(this).attr("data-session_id");

        $.ajax({
            url: '/api/' + session_id + '/',
            data: {
                'format': 'json'
            }
        }).done(function(result) { 

            // Handle presenters
            var presenter_list = "";
            $.each(result[0]['presenters'], function() {
                var name = $(this)[0]['name'];
                var org = $(this)[0]['organization'];
                presenter_list += '<li class="presenters">' + name + ' (' + org + ')</li>';
            });
            $('.session' + session_id + '-presenterlist').html(presenter_list);

            // Handle Tags
            var tag_list = "";
            $.each(result[0]['tags'], function() {
                console.log($(this));
                var tag = $(this)[0]['tag'];
                tag_list += '<li class="tags">' + tag + '</li>'
            });
            $('.session' + session_id + '-taglist').html(tag_list);

            // Put it all together
            $('.session' + session_id + '-details').show('linear');
            $('.session' + session_id + '-detailslink').hide();
        });

        return false;
    });*/

    $('.session-link').click(function() {
        var session_id = $(this).attr("data-session_id");
        $('.session-'+session_id+'-details').slideToggle();
    });

    $('a.vote-link').click(function() {
        var vote_value = $(this).attr('data-value');
        url = $(this).attr('href');

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'value': vote_value,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            }
        }).done(function(result) {
            if(vote_value > 0) {
                $('#vote-up-'+result.session_id).addClass('inactive');
                $('#vote-down-'+result.session_id).removeClass('inactive');
            }
            else {
                $('#vote-down-'+result.session_id).addClass('inactive');
                $('#vote-up-'+result.session_id).removeClass('inactive');   
            }

            $('#vote-total-'+result.session_id).css('width', result.vote_width);
        });
        return false;
    });
});