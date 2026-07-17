// Visual Shell logic for the TGIF Photo Gallery

const PHOTOS = [
    {
        id: 1,
        title: "Alpine Sunrise",
        category: "Nature",
        description: "Golden rays breaking over the sharp ridges of the high mountain peaks.",
        url: "https://images.unsplash.com/photo-1501854140801-50d01698950b?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: 2,
        title: "Misty Forest Path",
        category: "Nature",
        description: "A serene trail wandering deep into the quiet, fog-shrouded woodlands.",
        url: "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: 3,
        title: "Metropolis Glow",
        category: "Urban",
        description: "Vibrant neon lights reflecting on wet streets of a bustling city center.",
        url: "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: 4,
        title: "Concrete Geometric",
        category: "Minimal",
        description: "Satisfying angles and shadows forming clean patterns on modern structures.",
        url: "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: 5,
        title: "Woodland Sunbeams",
        category: "Nature",
        description: "Sharp sunbeams filtering through the towering canopy of an ancient forest.",
        url: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: 6,
        title: "Abstract Dunes",
        category: "Minimal",
        description: "Smooth, rolling sand ridges drawing perfect curving lines across the landscape.",
        url: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80"
    }
];

// Render Photo Cards
function renderPhotos(photos) {
    const grid = document.getElementById("photo-grid");
    grid.innerHTML = "";
    
    photos.forEach(photo => {
        const card = document.createElement("div");
        card.className = "photo-card";
        card.innerHTML = `
            <div class="photo-card-image-container">
                <img class="photo-card-img" src="${photo.url}" alt="${photo.title}">
            </div>
            <div class="photo-card-content">
                <span class="photo-card-tag">${photo.category}</span>
                <h3 class="photo-card-title">${photo.title}</h3>
                <p class="photo-card-description">${photo.description}</p>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Evaluate Layout by Calling Python Decision Engine API
async function evaluateLayout() {
    const width = window.innerWidth;
    const photoCount = PHOTOS.length;
    
    try {
        const response = await fetch("/api/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                viewport_width: width,
                photo_count: photoCount
            })
        });
        
        if (response.ok) {
            const decision = await response.json();
            updateUILayout(decision.outcome, decision.rule_ids[0]);
        } else {
            console.error("Layout engine returned error state.");
        }
    } catch (err) {
        console.error("Failed to connect to layout engine backend:", err);
    }
}

// Update Grid DOM based on Core Engine Decision
function updateUILayout(outcome, firingRule) {
    const grid = document.getElementById("photo-grid");
    const outcomeText = document.getElementById("engine-outcome");
    const ruleText = document.getElementById("engine-rule");
    
    grid.setAttribute("data-layout", outcome);
    outcomeText.textContent = outcome;
    ruleText.textContent = firingRule || "N/A";
}

// Simple debouncing for window resize events
let resizeTimeout;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(evaluateLayout, 100);
});

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    renderPhotos(PHOTOS);
    evaluateLayout();
});
