window.onload = function() {
    // Show the popup if not previously accepted
    if (!localStorage.getItem("popupShown")) {
        document.getElementById("popupModal").style.display = "flex";
    }

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

const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');
const dots = document.querySelectorAll('.dot');
const sliderContainer = document.querySelector('.slider-container');

let currentIndex = 0; // Tracks the current slide index
let autoSlideInterval; // Will hold the interval ID for auto-sliding

// Function to update the active dot indicator
function updateDots() {
    dots.forEach((dot, index) => {
        if (index === currentIndex) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

// Function to display a specific slide based on the index
function showSlides(index) {
    if (index >= slides.length) {
        currentIndex = 0; // Reset to first slide if at the end
    } else if (index < 0) {
        currentIndex = slides.length - 1; // Go to last slide if at the beginning
    } else {
        currentIndex = index; // Otherwise, set to the provided index
    }
    slider.style.transform = `translateX(-${currentIndex * 100}%)`; // Slide transition
    updateDots(); // Update the dots to reflect the current slide
}

// Function to move to the next slide
function nextSlide() {
    showSlides(currentIndex + 1);
}

// Function to move to the previous slide
function prevSlide() {
    showSlides(currentIndex - 1);
}

// Start the automatic sliding of images
function startAutoSlide() {
    autoSlideInterval = setInterval(nextSlide, 4000); // Slide every 4 seconds
}

// Stop the automatic sliding
function stopAutoSlide() {
    clearInterval(autoSlideInterval); // Clear the interval
}

// Add click event listeners to dots for direct slide navigation
dots.forEach(dot => {
    dot.addEventListener('click', () => {
        stopAutoSlide(); // Stop auto-slide when manually selecting a slide
        showSlides(parseInt(dot.dataset.index)); // Show the selected slide
        startAutoSlide(); // Restart auto-slide
    });
});

// Add event listeners for navigation buttons
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

// Stop auto-slide when the mouse enters the slider container
sliderContainer.addEventListener('mouseover', stopAutoSlide);

// Restart auto-slide when the mouse leaves the slider container
sliderContainer.addEventListener('mouseout', startAutoSlide);

// Start auto-slide when the page loads
startAutoSlide();
updateDots(); // Initialize the dots
}
document.addEventListener("DOMContentLoaded", function() {
    // Load the initial leaderboard data when the page loads
    fetchLeaderboard();

    // Handle form submission for uploading a new entry
    document.getElementById('uploadForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(this); // Capture the form data
        fetch('/upload_photo', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.photo_url) {
                // Add the new entry to the leaderboard without reloading the page
                addEntryToLeaderboard({
                    name: formData.get('name'),
                    length: formData.get('length'),
                    species: formData.get('species'),
                    photo_url: data.photo_url
                });

                // Optional: Clear the form fields after successful upload
                document.getElementById('uploadForm').reset();
            } else {
                alert(data.error || 'Failed to upload photo');
            }
        })
        .catch(error => console.error('Error uploading photo:', error));
    });
});

// Function to fetch and render the leaderboard from the server
function fetchLeaderboard() {
    fetch('/leaderboard')
        .then(response => response.json())
        .then(data => {
            const leaderboardList = document.getElementById('leaderboard-list');
            leaderboardList.innerHTML = ''; // Clear existing items

            data.forEach(entry => {
                addEntryToLeaderboard(entry); // Add each entry to the leaderboard
            });
        })
        .catch(error => console.error('Error fetching leaderboard data:', error));
}

function addEntryToLeaderboard(entry) {
    const leaderboardList = document.getElementById('leaderboard-list');
    
    const listItem = document.createElement('li');
    listItem.classList.add('leaderboard-item');

    const name = document.createElement('p');
    name.textContent = `${entry.name}`;

    const length = document.createElement('p');
    length.textContent = `${entry.length}`;

    const species = document.createElement('p');
    species.textContent = `${entry.species}`;

    const img = document.createElement('img');
    img.src = entry.photo_url;
    img.alt = `${entry.species}`;
    img.classList.add('leaderboard-image');
    img.onclick = function() {
        openModal(entry.photo_url);
    };

    listItem.appendChild(name);
    listItem.appendChild(length);
    listItem.appendChild(species);
    listItem.appendChild(img);

    leaderboardList.appendChild(listItem);
}

// Function to open the modal and display the clicked image
function openModal(imageUrl) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("enlargedImage");
    modal.style.display = "flex"; // Show the modal
    modalImg.src = imageUrl;
}

// Function to close the modal
function closeModal(event) {
    const modal = document.getElementById("imageModal");
    const modalImageContainer = document.querySelector(".modal-image-container");

    // Only close the modal if the click is outside the image container
    if (event.target === modal || event.target === modal.querySelector(".close-button")) {
        modal.style.display = "none";
    }
}
