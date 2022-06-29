window.onload = function(){
    $('.likes').on('click', 'button[type=like]', function(){
        var t_href = event.target;
        if (t_href.tagName != 'BUTTON'){
            t_href= t_href.parentElement;
            }

            console.log()
            if (t_href.parentElement.className.split(' ').indexOf('likes_comment') != -1){
                $.ajax({
                url:'/like/comment/' + t_href.value + '/',

                success: function(data){
                $('.likes').find('[value='+t_href.value+']').parent().html(data.result)
                }
            });
            } else {
            $.ajax({
                url:'/like/' + t_href.value + '/',

                success: function(data){
                $('.likes').find('[value='+t_href.value+']').parent().html(data.result)
                }
            });

            }


        return false;
    });
};