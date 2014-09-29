$(function() {
    $("input[id*=organization]").autocomplete({
        minLength: 2,
        source: "/organizations"
    });
});