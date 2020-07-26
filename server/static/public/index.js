$(function(){
    var frmLogin = document.getElementById("frmLogin");
    function SubmitForm(){
        $.post("/login", $('#frmLogin').serialize(), function(data, status){
            alert(status);
            if(status == "success"){
                window.location = "/dashboard";
            }
        }).fail(function(fData, status){
            var errMessage = fData.responseText;
            $("#txtErr").text(errMessage);
        })
    }
    
    frmLogin.addEventListener("submit", SubmitForm);

    var funcClearErrText = function(){
        $("#txtErr").text("");
    }

    $("#txtUsername").on("input", funcClearErrText);
    $("#txtPassword").on("input", funcClearErrText);
});

