document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const pilgrimagesContainer = document.getElementById('pilgrimages');

    if (searchInput) {
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value;
            if (query.length > 2) {
                const response = await fetch(`/api/search?q=${query}`);
                const results = await response.json();
                updatePilgrimages(results);
            } else if (query.length === 0) {
                location.reload();
            }
        });
    }

    function updatePilgrimages(pilgrimages) {
        pilgrimagesContainer.innerHTML = '';
        pilgrimages.forEach(pilgrimage => {
            const card = document.createElement('div');
            card.className = 'col';
            card.innerHTML = `
                <div class="card h-100">
                    <img src="/static/images/placeholder.jpg" class="card-img-top" alt="${pilgrimage.name}">
                    <div class="card-body">
                        <h5 class="card-title">${pilgrimage.name}</h5>
                        <p class="card-text">${pilgrimage.location}</p>
                        <a href="/pilgrimage/${pilgrimage.id}" class="btn btn-primary">Learn More</a>
                    </div>
                </div>
            `;
            pilgrimagesContainer.appendChild(card);
        });
    }
});