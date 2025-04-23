document.addEventListener("DOMContentLoaded", function () {
    const feedbackList = document.getElementById("feedback-list");
    const logoutBtn = document.getElementById("logout-btn");
    const userCountElement = document.getElementById("user-count");
    const storyList = document.getElementById("story-list");

    // Sample static feedback data
    let feedbacks = [
        { id: 1, text: "Great platform! Love the storytelling feature." },
        { id: 2, text: "It would be nice to have more customization options." },
        { id: 3, text: "Really smooth UI. Enjoying the experience!" }
    ];

    // Sample static story data
    let stories = [
        { id: 1, title: "The Lost Kingdom", reference: "story_001" },
        { id: 2, title: "Moonlight Escape", reference: "story_002" },
        { id: 3, title: "Whispers of the Forest", reference: "story_003" }
    ];

    // Placeholder for user count
    const totalUsers = 27; // This will be dynamically fetched from Firebase later

    function renderFeedbacks() {
        feedbackList.innerHTML = "";
        feedbacks.forEach((feedback) => {
            const li = document.createElement("li");
            li.classList.add("feedback-item");
            li.innerHTML = `
                <span>${feedback.text}</span>
                <button class="delete-btn" data-id="${feedback.id}">Delete</button>
            `;
            feedbackList.appendChild(li);
        });
    }

    function renderUserCount() {
        userCountElement.textContent = totalUsers; // Replace with dynamic Firebase count later
    }

    function renderStories() {
        storyList.innerHTML = "";
        stories.forEach((story) => {
            const li = document.createElement("li");
            li.classList.add("story-card");
            li.innerHTML = `
                <h3>${story.title}</h3>
                <p>Reference ID: ${story.reference}</p>
            `;
            storyList.appendChild(li);
        });
    }

    // Delete feedback
    feedbackList.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-btn")) {
            const feedbackId = parseInt(event.target.getAttribute("data-id"));
            feedbacks = feedbacks.filter((feedback) => feedback.id !== feedbackId);
            renderFeedbacks();
        }
    });

    // Logout
    logoutBtn.addEventListener("click", function () {
        window.location.href = "login.html";
    });

    // Initial rendering
    renderFeedbacks();
    renderUserCount();
    renderStories();
});
