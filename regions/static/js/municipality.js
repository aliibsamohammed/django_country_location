var response_cache = {};

function fill_municipalities(county_id) {
    if (response_cache[county_id]) {
        $("#id_municipality").html(response_cache[county_id]);
    } else {
        $.getJSON("/municipalities_for_county/", { county_id: county_id },
            function(ret, textStatus) {
                var options = '<option value="" selected="selected">---------</option>';
                for (var i in ret) {
                    options += '<option value="' + ret[i].id + '">' +
                        ret[i].name + '</option>';
                }
                response_cache[county_id] = options;
                $("#id_municipality").html(options);
            });
    }
}
$(document).ready(function() {
    $("#id_county").change(function() { fill_municipalities($(this).val()); });
});