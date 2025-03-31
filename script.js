// Show the modal when the page loads
window.onload = function() {
    document.getElementById("welcomeModal").style.display = "block";
}

// Function to close the modal
function closeModal() {
    document.getElementById("welcomeModal").style.display = "none";
}

// Image Upload Preview
function previewImage() {
    const fileInput = document.getElementById('imageUpload');
    const previewContainer = document.getElementById('imagePreview');
    
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const imgElement = document.createElement('img');
            imgElement.src = e.target.result;
            imgElement.style.width = '100%';
            previewContainer.innerHTML = '';
            previewContainer.appendChild(imgElement);
            previewContainer.style.display = 'block';
        };
        
        reader.readAsDataURL(fileInput.files[0]);
    }
}

// Generate Story Button - Simulating the story generation
function generateStory() {
    let fileInput = document.getElementById('imageUpload');
    let file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    fetch("/generate_story", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            document.getElementById("storyText").innerHTML = `<p>${data.story}</p>`;
        }
    })
    .catch(error => console.error("Error:", error));
}


// Feedback Form Submit Handler
document.getElementById('feedbackForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;
    
    if (rating >= 1 && rating <= 5 && comment) {
        alert('Thank you for your feedback!');
        document.getElementById('feedbackForm').reset();
    } else {
        alert('Please provide a valid rating and comment.');
    }
});
// Check if localStorage has saved stories
document.addEventListener("DOMContentLoaded", function () {
    const storiesContainer = document.getElementById("stories-container");

    if (storiesContainer) {
        let savedStories = JSON.parse(localStorage.getItem("savedStories")) || [];

        if (savedStories.length === 0) {
            storiesContainer.innerHTML = `<p class="empty-message">No stories saved yet.</p>`;
        } else {
            storiesContainer.innerHTML = "";
            savedStories.forEach((story, index) => {
                let storyElement = document.createElement("div");
                storyElement.classList.add("story-card");
                storyElement.innerHTML = `
                    <p>${story}</p>
                    <button class="delete-btn" onclick="deleteStory(${index})">Delete</button>
                `;
                storiesContainer.appendChild(storyElement);
            });
        }
    }
});

// Function to save story
function saveStory() {
    let storyText = document.getElementById("generated-story").innerText;
    if (!storyText) return;

    let savedStories = JSON.parse(localStorage.getItem("savedStories")) || [];
    savedStories.push(storyText);
    localStorage.setItem("savedStories", JSON.stringify(savedStories));

    alert("Story saved successfully!");
}

// Function to delete a story
function deleteStory(index) {
    let savedStories = JSON.parse(localStorage.getItem("savedStories")) || [];
    savedStories.splice(index, 1);
    localStorage.setItem("savedStories", JSON.stringify(savedStories));

    location.reload(); // Refresh page to update list
}

// Redirect profile button to profile page
document.querySelector(".profile-btn").addEventListener("click", function () {
    window.location.href = "profile.html";
});

// Logout Function
document.getElementById("logout")?.addEventListener("click", function () {
    localStorage.clear();
    window.location.href = "login.html";
});
