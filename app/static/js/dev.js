function objectifyForm(form) {//serialize data function
    var formArray = form.serializeArray()
    var returnArray = {};
    for (var i = 0; i < formArray.length; i++){
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}

var post_obj = {
    type: "POST",
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    success: function(data){
        $("#message").html(JSON.stringify(data.message));
    },
    add_data: function(data_obj){
        this["data"] = JSON.stringify(data_obj);
    },
    add_url: function(url){
        this["url"] = dev_mode + "/" + url;
    }
}

$('#create_tables').click(function(){
    post_obj.add_url("create_tables");
    $.ajax(post_tables);
});

$('#list_tables').click(function(){
    post_obj.add_url("list_tables");
    $.ajax(post_obj);
});

$('#delete_tables').click(function(){
    post_obj.add_url("delete_tables");
    $.ajax(post_obj);
});

$('#import_provisional_leaders').click(function(e){
    post_obj.add_data(objectifyForm($("#ipl_form")));
    post_obj.add_url("import_provisional_leaders");
    $.ajax(post_obj);
});

$('#import_smashgg_tournament').click(function(e){
    post_obj.add_data(objectifyForm($("#ist_form")));
    post_obj.add_url("import_smashgg_tournament");
    $.ajax(post_obj);
});