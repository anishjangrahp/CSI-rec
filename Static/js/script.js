$(document).ready(function () {
    console.log("loaded");
    $(document).on('submit', '#Register', function (e) {
        e.preventDefault();
        var form = $(this).serialize();
        $.ajax({
            url: '/post-registration',
            type: 'POST',
            data: form,
            success: function (response) {
                if (response === "error") {
                    alert("username already exists");
                }
                else {
                    console.log(response);
                    window.location.href = '/login';
                }
            }
        });
    });

    $(document).on('submit','#event',function (e) {
        e.preventDefault();
        var form = $(this).serialize();
        $.ajax({
            url: '/post-event',
            type: 'POST',
            data: form,
            success:function (response) {
                if(response === "error"){
                    alert("Something went wrong!");
                }
                else{
                    console.log(response);
                    window.location.href = '/my-events';
                }
            }
        });
    });


    $(document).on('submit', '#login', function (e) {
        e.preventDefault();
        var form = $(this).serialize();
        $.ajax({
            url: '/check-login',
            type: 'POST',
            data: form,
            success: function (response) {
                if (response === "Incorrect Password" || response === "User not registered") {
                    alert(response);
                } else {
                    console.log("Logged in as", response);
                    window.location.href = '/my-events';
                }
            }
        });
    });

    $(document).on('click', '#logout', function (e) {
        e.preventDefault();
        $.ajax({
            url: '/logout',
            type: 'GET',
            success: function (response) {
                if (response == "success") {
                    window.location.href = '/login';
                }
                else {
                    alert("Something went wrong");
                }
            }
        });
    });



});