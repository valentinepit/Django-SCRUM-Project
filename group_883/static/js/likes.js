window.onload = function(){
    $('.likes').on('click', 'button[type=like]', function(){
        var t_href = event.target;
        if (t_href.tagName != 'BUTTON'){
            t_href= t_href.parentElement;
            }

        $.ajax({
            url:'/like/' + t_href.value + '/',

            success: function(data){
            $('.likes').html(data.result)
            }
        });
        return false;
    });
};