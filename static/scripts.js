document.addEventListener("DOMContentLoaded", function() {
    // Show the popup if not previously accepted
    if (!localStorage.getItem("popupShown")) {
        const popupModal = document.getElementById("popupModal");
        if (popupModal) {
            popupModal.style.display = "flex";
        }
    }

    // Popup close functions
    function closePopup() {
        const popupModal = document.getElementById("popupModal");
        if (popupModal) popupModal.style.display = "none";
        localStorage.setItem("popupShown", "true");
    }

    function acceptAll() {
        closePopup();
    }

    function declineAll() {
        closePopup();
    }

    // Slider functionality
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
            dot.classList.toggle('active', index === currentIndex);
        });
    }

    // Function to display a specific slide based on the index
    function showSlides(index) {
        if (slider) {
            currentIndex = (index + slides.length) % slides.length;
            slider.style.transform = `translateX(-${currentIndex * 100}%)`; // Slide transition
            updateDots(); // Update the dots to reflect the current slide
        }
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

    // Add event listeners to navigation buttons if they exist
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);

    // Stop auto-slide on hover and resume on mouseout
    if (sliderContainer) {
        sliderContainer.addEventListener('mouseover', stopAutoSlide);
        sliderContainer.addEventListener('mouseout', startAutoSlide);
    }

    // Start the auto slide initially
    startAutoSlide();
    updateDots();

    // Leaderboard data fetch and display
    fetchLeaderboard();

    // Fetch leaderboard data
    function fetchLeaderboard() {
        fetch('/leaderboard')
            .then(response => response.json())
            .then(data => {
                const leaderboardList = document.getElementById('leaderboard-list');
                if (!leaderboardList) {
                    console.error("Leaderboard list element not found.");
                    return;
                }
                leaderboardList.innerHTML = ''; // Clear existing items

                data.forEach(entry => {
                    addEntryToLeaderboard(entry); // Add each entry to the leaderboard
                });
            })
            .catch(error => console.error('Error fetching leaderboard data:', error));
    }

    // Form submission for uploading a photo
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', event => {
            event.preventDefault();
            const formData = new FormData(uploadForm);

            fetch('/upload_photo', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    console.log('Response status: ', response.status);
                    response.text().then(text => console.error('Response body:', text));
                    throw new Error(`Network response was not ok. Status: ${response.status}`);
                }
                return response.json(); // Expect JSON response
            })
            .then(data => {
                if (data.photo_url) {
                    addEntryToLeaderboard({
                        name: formData.get('name'),
                        length: formData.get('length'),
                        species: formData.get('species'),
                        location: formData.get('location'),
                        photo_url: data.photo_url
                    });
                    uploadForm.reset();
                } else {
                    alert(data.error || 'Failed to upload photo');
                }
            })
            .catch(error => console.error('Error uploading photo:', error));
        });
    }

    // Function to add an entry to the leaderboard
    function addEntryToLeaderboard(entry) {
        const leaderboardList = document.getElementById('leaderboard-list');
        if (!leaderboardList) return;

        const listItem = document.createElement('li');
        listItem.classList.add('leaderboard-item');

        const name = document.createElement('p');
        name.textContent = `${entry.name}`;

        const length = document.createElement('p');
        length.textContent = `${entry.length}`;

        const species = document.createElement('p');
        species.textContent = `${entry.species}`;

        const location = document.createElement('p');
        location.textContent = `${entry.location}`;

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
        listItem.appendChild(location);
        listItem.appendChild(img);

        leaderboardList.appendChild(listItem);
    }

    // Modal functionality for viewing images
    function openModal(imageUrl) {
        const modal = document.getElementById("imageModal");
        const modalImg = document.getElementById("enlargedImage");
        if (modal && modalImg) {
            modal.style.display = "flex"; 
            modalImg.src = imageUrl;
        }
    }

    function closeModal(event) {
        const modal = document.getElementById("imageModal");
        if (modal && (event.target === modal || event.target.classList.contains("close-button"))) {
            modal.style.display = "none";
        }
    }
});
