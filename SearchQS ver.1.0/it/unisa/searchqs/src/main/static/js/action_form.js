function displayUndisplayPassword(passwordId, buttonId) {
    const passwordField = document.getElementById(passwordId);
    const displayPasswordButton = document.getElementById(buttonId);
    if (passwordField.type === "password") {
        passwordField.type = "text";
        displayPasswordButton.innerHTML = '<i class="fa fa-eye-slash fa-2x" aria-hidden="true"></i>';
    } else {
        passwordField.type = "password";
        displayPasswordButton.innerHTML = '<i class="fa fa-eye fa-2x" aria-hidden="true"></i>';
    }
}

function enableDisableElements(arrayId) {
    arrayId.forEach(function(idElement) {
        var element = document.getElementById(idElement);
        element.disabled = !element.disabled;
    })
}

function enableDisableReadonlyElements(arrayId) {
    arrayId.forEach(function(idElement) {
        var element = document.getElementById(idElement);
        if (element.hasAttribute('readonly')) {
            element.removeAttribute('readonly');
        } else {
            element.setAttribute('readonly', true);
        }
    })
}

module.exports = { displayUndisplayPassword, enableDisableElements };







