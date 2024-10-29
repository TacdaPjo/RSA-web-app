window.onload = function() {
    if (!localStorage.getItem("popupShown")) {
        document.getElementById("popupModal").style.display = "flex";
    }
};

function closePopup() {
    document.getElementById("popupModal").style.display = "none";
    localStorage.setItem("popupShown", "true");
}

function acceptAll() {
    closePopup();
}

function declineAll() {
    closePopup();
}

let currentIndex = 0;
const images = document.querySelectorAll(".image");

function showSlide(index) {
    images.forEach((img, i) => {
        img.classList.remove("show"); 
        if (i === index) {
            img.classList.add("show"); 
        }
    });
}

function changeSlide(direction) {
    currentIndex += direction;
    if (currentIndex < 0) {
        currentIndex = images.length - 1;
    } else if (currentIndex >= images.length) {
        currentIndex = 0;
    }
    showSlide(currentIndex);
}

showSlide(currentIndex);
