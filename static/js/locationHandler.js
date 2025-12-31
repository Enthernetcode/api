// Location-based dynamic restaurant loading
document.addEventListener('DOMContentLoaded', function() {
    const stateFilter = document.getElementById('stateFilter');
    const lgaFilter = document.getElementById('lgaFilter');
    const fetchBtn = document.getElementById('fetchBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const restaurantsGrid = document.getElementById('restaurantsGrid');
    const noResults = document.getElementById('noResults');
    const paginationControls = document.getElementById('paginationControls');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');
    const totalCount = document.getElementById('totalCount');
    const currentPageSpan = document.getElementById('currentPage');
    const avgRatingSpan = document.getElementById('avgRating');

    let currentState = '';
    let currentLGA = '';
    let currentPage = 1;
    let totalPages = 1;

    // Load states on page load
    loadStates();

    // Event Listeners
    stateFilter.addEventListener('change', function() {
        currentState = this.value;
        if (currentState) {
            loadLGAs(currentState);
            lgaFilter.disabled = false;
        } else {
            lgaFilter.innerHTML = '<option value="">Select LGA...</option>';
            lgaFilter.disabled = true;
        }
    });

    fetchBtn.addEventListener('click', fetchRestaurants);

    prevBtn.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            fetchRestaurants();
        }
    });

    nextBtn.addEventListener('click', function() {
        if (currentPage < totalPages) {
            currentPage++;
            fetchRestaurants();
        }
    });

    // Load all available states
    async function loadStates() {
        try {
            const response = await fetch('/api/locations/states');
            const data = await response.json();

            if (data.success) {
                stateFilter.innerHTML = '<option value="">Select State...</option>';
                data.data.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state;
                    option.textContent = state;
                    stateFilter.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading states:', error);
        }
    }

    // Load LGAs for selected state
    async function loadLGAs(state) {
        try {
            const response = await fetch(`/api/locations/lgas/${encodeURIComponent(state)}`);
            const data = await response.json();

            if (data.success) {
                lgaFilter.innerHTML = '<option value="">All LGAs</option>';
                data.data.forEach(lga => {
                    const option = document.createElement('option');
                    option.value = lga;
                    option.textContent = lga;
                    lgaFilter.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading LGAs:', error);
        }
    }

    // Fetch restaurants for selected location
    async function fetchRestaurants() {
        const state = stateFilter.value;

        if (!state) {
            alert('Please select a state');
            return;
        }

        const lga = lgaFilter.value;

        // Show loading
        loadingIndicator.style.display = 'block';
        restaurantsGrid.style.display = 'none';
        noResults.style.display = 'none';
        paginationControls.style.display = 'none';

        try {
            let url = `/api/restaurants/location?state=${encodeURIComponent(state)}&page=${currentPage}&per_page=15`;

            if (lga) {
                url += `&lga=${encodeURIComponent(lga)}`;
            }

            const response = await fetch(url);
            const data = await response.json();

            // Hide loading
            loadingIndicator.style.display = 'none';

            if (data.success && data.data.length > 0) {
                displayRestaurants(data.data);
                updatePagination(data);
                updateStats(data);
            } else {
                noResults.style.display = 'block';
            }
        } catch (error) {
            console.error('Error fetching restaurants:', error);
            loadingIndicator.style.display = 'none';
            noResults.style.display = 'block';
        }
    }

    // Display restaurants in grid
    function displayRestaurants(restaurants) {
        restaurantsGrid.innerHTML = '';

        restaurants.forEach(restaurant => {
            const card = createRestaurantCard(restaurant);
            restaurantsGrid.appendChild(card);
        });

        restaurantsGrid.style.display = 'grid';
    }

    // Create restaurant card HTML
    function createRestaurantCard(restaurant) {
        const card = document.createElement('div');
        card.className = 'restaurant-card';
        card.setAttribute('data-city', restaurant.city || 'Unknown');
        card.setAttribute('data-name', restaurant.name.toLowerCase());

        card.innerHTML = `
            <div class="card-header">
                <div class="restaurant-icon">🍛</div>
                ${restaurant.rating ? `
                <div class="rating-badge">
                    <span class="star">⭐</span>
                    <span class="rating-value">${restaurant.rating}</span>
                </div>
                ` : ''}
            </div>

            <div class="card-body">
                <h3 class="restaurant-name">${restaurant.name}</h3>

                <div class="restaurant-info">
                    ${restaurant.city ? `
                    <div class="info-item">
                        <span class="info-icon">📍</span>
                        <span class="info-text">${restaurant.city}${restaurant.state ? ', ' + restaurant.state : ''}</span>
                    </div>
                    ` : ''}

                    ${restaurant.lga ? `
                    <div class="info-item">
                        <span class="info-icon">🏛️</span>
                        <span class="info-text">${restaurant.lga} LGA</span>
                    </div>
                    ` : ''}

                    ${restaurant.location ? `
                    <div class="info-item">
                        <span class="info-icon">🏠</span>
                        <span class="info-text">${restaurant.location.substring(0, 50)}${restaurant.location.length > 50 ? '...' : ''}</span>
                    </div>
                    ` : ''}

                    ${restaurant.opening_hours ? `
                    <div class="info-item">
                        <span class="info-icon">🕒</span>
                        <span class="info-text">${restaurant.opening_hours.substring(0, 40)}${restaurant.opening_hours.length > 40 ? '...' : ''}</span>
                    </div>
                    ` : ''}
                </div>

                <div class="specialties">
                    ${restaurant.specialties && restaurant.specialties.length > 0 ?
                        restaurant.specialties.map(s => `<span class="specialty-tag">${s}</span>`).join('') :
                        '<span class="specialty-tag">Nigerian Cuisine</span>'
                    }
                </div>
            </div>

            <div class="card-footer">
                <a href="/restaurant/${restaurant.id}" class="btn-view">View Details</a>
                ${restaurant.url ? `<a href="${restaurant.url}" target="_blank" class="btn-order">Order Now</a>` : ''}
            </div>
        `;

        return card;
    }

    // Update pagination controls
    function updatePagination(data) {
        totalPages = data.pages;
        currentPage = data.page;

        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

        prevBtn.disabled = currentPage <= 1;
        nextBtn.disabled = currentPage >= totalPages;

        paginationControls.style.display = totalPages > 1 ? 'flex' : 'none';
    }

    // Update statistics
    function updateStats(data) {
        totalCount.textContent = data.total;
        currentPageSpan.textContent = data.page;

        // Calculate average rating
        if (data.data.length > 0) {
            const ratings = data.data.filter(r => r.rating).map(r => r.rating);
            if (ratings.length > 0) {
                const avg = (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(2);
                avgRatingSpan.textContent = avg;
            }
        }
    }
});
