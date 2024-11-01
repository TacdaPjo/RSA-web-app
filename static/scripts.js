// Wait until DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded.");

    // Popup functions
    function closePopup() {
        document.getElementById("popupModal").style.display = "none";
        localStorage.setItem("popupShown", "true");
    }

    // Slider elements
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    const dots = document.querySelectorAll('.dot');
    const sliderContainer = document.querySelector('.slider-container');

    let currentIndex = 0; 
    let autoSlideInterval;

    function updateDots() {
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }

    function showSlides(index) {
        currentIndex = (index + slides.length) % slides.length;
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;
        updateDots();
    }

    function nextSlide() {
        showSlides(currentIndex + 1);
    }

    function prevSlide() {
        showSlides(currentIndex - 1);
    }

    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 4000);
    }

    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    // Event listeners for slider
    dots.forEach(dot => dot.addEventListener('click', (e) => {
        stopAutoSlide();
        showSlides(parseInt(e.target.dataset.index));
        startAutoSlide();
    }));

    nextBtn?.addEventListener('click', nextSlide);
    prevBtn?.addEventListener('click', prevSlide);

    sliderContainer?.addEventListener('mouseover', stopAutoSlide);
    sliderContainer?.addEventListener('mouseout', startAutoSlide);

    startAutoSlide();
    updateDots();

    // Modal functions
    window.openModal = function (imageUrl) {
        const modal = document.getElementById("imageModal");
        const modalImg = document.getElementById("enlargedImage");

        if (modal && modalImg) {
            modal.style.display = "flex";
            modalImg.src = imageUrl;
        } else {
            console.error("Modal or image element not found in the DOM.");
        }
    };

    window.closeModal = function (event) {
        const modal = document.getElementById("imageModal");
        if (event.target === modal || event.target.classList.contains("close-button")) {
            modal.style.display = "none";
        }
    };

    
    // Upload form submission
    document.getElementById('uploadForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch('/upload_photo', { method: 'POST', body: formData })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
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
                    document.getElementById('uploadForm').reset();
                } else {
                    alert(data.error || 'Failed to upload photo');
                }
            })
            .catch(error => console.error('Error uploading photo:', error));
    });

    function fetchLeaderboard() {
        fetch('/leaderboard')
            .then(response => response.json())
            .then(data => {
                const leaderboardList = document.getElementById('leaderboard-list');
                leaderboardList.innerHTML = '';
                data.forEach(entry => addEntryToLeaderboard(entry));
            })
            .catch(error => console.error('Error fetching leaderboard data:', error));
    }

    function addEntryToLeaderboard(entry) {
        const leaderboardList = document.getElementById('leaderboard-list');
        const listItem = document.createElement('li');
        listItem.classList.add('leaderboard-item');

        const name = document.createElement('p');
        name.textContent = entry.name;

        const length = document.createElement('p');
        length.textContent = entry.length;

        const species = document.createElement('p');
        species.textContent = entry.species;

        const location = document.createElement('p');
        location.textContent = entry.location;

        const img = document.createElement('img');
        img.src = entry.photo_url;
        img.alt = entry.species;
        img.classList.add('leaderboard-image');
        img.onclick = () => openModal(entry.photo_url);

        listItem.append(name, length, species, location, img);
        leaderboardList.appendChild(listItem);
    }

    fetchLeaderboard();
});

