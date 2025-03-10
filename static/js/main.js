document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const pilgrimagesContainer = document.getElementById('pilgrimages-container'); // Corrected ID

    if (searchInput && pilgrimagesContainer) {
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value.trim(); // Trim whitespace

            if (query.length > 2) {
                try {
                    // Show loading state
                    pilgrimagesContainer.innerHTML = '<p class="text-center">Loading...</p>';

                    // Fetch results from the API
                    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const results = await response.json();

                    // Update the pilgrimages
                    updatePilgrimages(results);
                } catch (error) {
                    console.error('Error:', error);
                    pilgrimagesContainer.innerHTML = '<p class="text-center text-danger">Failed to load results. Please try again.</p>';
                }
            } else if (query.length === 0) {
                // Reload the page if the search query is empty
                location.reload();
            }
        });
    }

    function updatePilgrimages(pilgrimages) {
        pilgrimagesContainer.innerHTML = '';

        if (pilgrimages.length === 0) {
            // Show empty state
            pilgrimagesContainer.innerHTML = '<p class="text-center">No pilgrimages found.</p>';
            return;
        }

        // Display the pilgrimages
        pilgrimages.forEach(pilgrimage => {
            const card = document.createElement('div');
            card.className = 'col';
            card.innerHTML = `
                <div class="card h-100 shadow-sm">
                    <img src="${pilgrimage.image_url || '/static/images/placeholder.jpg'}" class="card-img-top" alt="${pilgrimage.name}">
                    <div class="card-body">
                        <h5 class="card-title">${pilgrimage.name}</h5>
                        <p class="card-text text-muted">${pilgrimage.location}</p>
                        <a href="/pilgrimage/${pilgrimage.id}" class="btn btn-primary">Learn More</a>
                    </div>
                </div>
            `;
            pilgrimagesContainer.appendChild(card);
        });
    }
});