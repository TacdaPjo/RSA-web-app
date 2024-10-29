window.onload = function() {
    if (!localStorage.getItem("popupShown")) {
        document.getElementById("declinePopup").style.display = "flex";
    }
};

function closePopup() {
    document.getElementById("declinePopup").style.display = "none";
    localStorage.setItem("popupShown", "true");
}

function acceptAll() {
    closePopup();
}

function declineAll() {
    closePopup();
}