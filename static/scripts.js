window.onload = function() {
    // Show the popup if not previously accepted
    if (!localStorage.getItem("popupShown")) {
        document.getElementById("popupModal").style.display = "flex";
    }

    // Get references to buttons and images only after the DOM loads
    const prevButton = document.querySelector(".prev");
    const nextButton = document.querySelector(".next");
    const images = document.querySelectorAll(".image");
    let currentIndex = 0;

    function showSlide(index) {
        images.forEach((img, i) => {
            img.classList.remove("show"); // Hide all images
            if (i === index) {
                img.classList.add("show"); // Show only the current image
            }
        });
        console.log(`Displaying slide ${index + 1}`);
    }

    function changeSlide(direction) {
        currentIndex += direction;
        if (currentIndex < 0) {
            currentIndex = images.length - 1; // Wrap to the last image
        } else if (currentIndex >= images.length) {
            currentIndex = 0; // Wrap to the first image
        }
        showSlide(currentIndex);
        console.log(`Changed to slide ${currentIndex + 1}`);
    }

    // Show the initial slide
    showSlide(currentIndex);

    // Attach event listeners to the buttons
    prevButton.addEventListener("click", () => changeSlide(-1));
    nextButton.addEventListener("click", () => changeSlide(1));
};

// Popup close functions
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
