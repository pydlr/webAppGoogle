$(function() { 
    $('#btnSignUp').click(function() {
        console.log("This is working so far No 3");
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) 
            {
                var str1 = "/userHome/";
                var str2 = response;
                var str3 = "?fb=0"
                var path = str1.concat(str2);
                var path = path.concat(str3);
                window.location = path;
            },
            error: function(error) {
                console.log(" Debug error in js");
            }
        });
    });
}); 



