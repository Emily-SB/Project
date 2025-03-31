document.addEventListener("DOMContentLoaded", function () {
    const feedbackList = document.getElementById("feedback-list");
    const logoutBtn = document.getElementById("logout-btn");

    // Sample feedback data (this should ideally come from a backend)
    let feedbacks = [
        { id: 1, text: "Great platform! Love the storytelling feature." },
        { id: 2, text: "It would be nice to have more customization options." },
        { id: 3, text: "Really smooth UI. Enjoying the experience!" }
    ];

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

    // Delete Feedback
    feedbackList.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-btn")) {
            const feedbackId = parseInt(event.target.getAttribute("data-id"));
            feedbacks = feedbacks.filter((feedback) => feedback.id !== feedbackId);
            renderFeedbacks();
        }
    });

    // Logout Functionality
    logoutBtn.addEventListener("click", function () {
        window.location.href = "login.html";
    });

    // Render initial feedback list
    renderFeedbacks();
});
