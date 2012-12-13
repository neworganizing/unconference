/*
By Nick Catalano (@nickcatal)

Copyright 2012 New Organizing Institute
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0

*/

$('.sessionlink').click(function () {
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
});