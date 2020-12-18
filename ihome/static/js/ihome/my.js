// js读取cookie的方法
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function logout() {
    $.ajax({
        url: "/api/v1.0/sessions",
        type: "delete",
        headers: {
            "X_CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if ("0" == resp.errno) {
                location.href = "/index.html"
            }
        }
    })
}

$(document).ready(function () {
})