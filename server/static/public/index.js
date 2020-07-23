const frmLogin = document.getElementById("frmLogin");

function SubmitForm(){
    alert("SENDING!");
    $.post("/login", $('#frmLogin').serialize(), function(data, status){
        alert(status);
        if(status == "success"){
            window.location = "/dashboard";
        }
        else{
            alert(data);
            alert("Error");
        }
    });
}

frmLogin.addEventListener("submit", SubmitForm);