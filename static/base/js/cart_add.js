$('#cartAdd').click(function(){
    ingre_id = $(this).attr('ingre_id')
    count = $('.num_show').val()
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    params = {'ingre_id': ingre_id, 'count': count, 'csrf': csrf}
    $.post('/cart/add/', params, function(data){
        if (data.res == 5){
            alert("添加成功")
        }
        else{
            alert(data.errmsg)
        }
    })
});