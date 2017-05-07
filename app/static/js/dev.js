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
    // post_obj.add_data($("#ipl_form").serialize());
    post_obj.add_url("import_provisional_leaders");
    $.ajax(post_obj);
});