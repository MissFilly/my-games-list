$(function(){      
   $("#allcat").click(function(){
       $(".discounted-item").slideDown();
       $("#catpicker a").removeClass("current");
       $(this).addClass("current");
       return false;
   });
   
   $(".filter").click(function(){
        var thisFilter = $(this).attr("id");
        $(".discounted-item").slideUp();
        $("."+ thisFilter).slideDown();
        $("#catpicker a").removeClass("current");
        $(this).addClass("current");
        return false;
   });
});