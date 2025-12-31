// Search and Filter Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const cityFilter = document.getElementById('cityFilter');
    const restaurantsGrid = document.getElementById('restaurantsGrid');
    const noResults = document.getElementById('noResults');
    const totalCount = document.getElementById('totalCount');

    // Get all restaurant cards
    const restaurantCards = Array.from(document.querySelectorAll('.restaurant-card'));

    // Filter function
    function filterRestaurants() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCity = cityFilter.value;

        let visibleCount = 0;

        restaurantCards.forEach(card => {
            const restaurantName = card.getAttribute('data-name');
            const restaurantCity = card.getAttribute('data-city');
            const restaurantLocation = card.getAttribute('data-location') || '';
            const restaurantCuisine = card.getAttribute('data-cuisine') || '';
            const restaurantSpecialties = card.getAttribute('data-specialties') || '';

            // Search across all fields
            const searchableText = `${restaurantName} ${restaurantLocation} ${restaurantCuisine} ${restaurantSpecialties}`.toLowerCase();

            // Check search term - matches if found in any field
            const matchesSearch = !searchTerm || searchableText.includes(searchTerm);

            // Check city filter
            const matchesCity = !selectedCity || restaurantCity === selectedCity;

            // Show/hide card
            if (matchesSearch && matchesCity) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Update count
        if (totalCount) {
            totalCount.textContent = visibleCount;
        }

        // Show/hide no results message
        if (visibleCount === 0) {
            restaurantsGrid.style.display = 'none';
            noResults.style.display = 'block';
        } else {
            restaurantsGrid.style.display = 'grid';
            noResults.style.display = 'none';
        }
    }

    // Add event listeners
    if (searchInput) {
        searchInput.addEventListener('input', filterRestaurants);
    }

    if (cityFilter) {
        cityFilter.addEventListener('change', filterRestaurants);
    }

    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';

                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all restaurant cards
    restaurantCards.forEach(card => {
        observer.observe(card);
    });
});

// Download Excel functionality
document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('downloadExcelBtn');
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            // Get current filter state
            const stateFilter = document.getElementById('stateFilter');
            const lgaFilter = document.getElementById('lgaFilter');
            
            const state = stateFilter ? stateFilter.value : 'Lagos';
            const lga = lgaFilter ? lgaFilter.value : '';
            
            // Build download URL
            let downloadUrl = '/api/restaurants/download/excel';
            const params = new URLSearchParams();
            
            if (state) {
                params.append('state', state);
            }
            
            if (lga) {
                params.append('lga', lga);
            }
            
            if (params.toString()) {
                downloadUrl += '?' + params.toString();
            }
            
            // Show downloading feedback
            const originalText = downloadBtn.innerHTML;
            downloadBtn.innerHTML = '⏳ Preparing...';
            downloadBtn.disabled = true;
            
            // Trigger download
            window.location.href = downloadUrl;
            
            // Reset button after a delay
            setTimeout(() => {
                downloadBtn.innerHTML = originalText;
                downloadBtn.disabled = false;
            }, 2000);
        });
    }
});
