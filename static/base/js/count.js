$('.add').click(function(){
    count = $('.num_show').val();
    count = parseInt(count)+1;
    $('.num_show').val(count)
});

$('.minus').click(function(){
    count = $('.num_show').val();
    count = parseInt(count)-1;
    if(count <= 1){
        count = 1
    }
    $('.num_show').val(count)
});

$('.num_show').blur(function(){
    count = $(this).val();
    if(isNaN(count)||count.trim().length===0||parseInt(count)<=0){
        count = 1
    }
    $(this).val(count);
});