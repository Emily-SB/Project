// Show the modal when the page loads
window.onload = function () {
    document.getElementById("welcomeModal").style.display = "block";
  };
  
  // Function to close the modal
  function closeModal() {
    document.getElementById("welcomeModal").style.display = "none";
  }
  
  // Image Upload Preview
  function previewImage() {
    const fileInput = document.getElementById("imageUpload");
    const previewContainer = document.getElementById("imagePreview");
  
    if (fileInput.files && fileInput.files[0]) {
      const reader = new FileReader();
  
      reader.onload = function (e) {
        const imgElement = document.createElement("img");
        imgElement.src = e.target.result;
        imgElement.style.width = "100%";
        previewContainer.innerHTML = "";
        previewContainer.appendChild(imgElement);
        previewContainer.style.display = "block";
      };
  
      reader.readAsDataURL(fileInput.files[0]);
    }
  }
  
  // Generate Story Button - Simulating the story generation
// Fix template literal and ensure functions are defined
function generateStory() {
  const fileInput = document.getElementById('imageUpload');
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload an image first.");
    return;
  }

  const formData = new FormData();
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
      // Fixed: Use backticks (`) for template literal
      document.getElementById("storyText").innerHTML = `<p>${data.story}</p>`;
      console.log("Story URL:", data.story_url);
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Something went wrong while uploading the image.");
  });
}

// Add event listeners (if replacing onclick)
document.addEventListener("DOMContentLoaded", () => {
  const previewBtn = document.getElementById("previewBtn");
  if (previewBtn) {
    previewBtn.addEventListener("click", previewImage); // Assuming previewImage function exists
  }

  const generateBtn = document.getElementById("generateBtn");
  if (generateBtn) {
    generateBtn.addEventListener("click", generateStory);
  }
});

// Assuming a previewImage function might exist
function previewImage() {
  const fileInput = document.getElementById('imageUpload');
  const file = fileInput.files[0];
  const imgPreview = document.getElementById('imgPreview'); // Assuming an element with this ID exists

  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      if (imgPreview) {
        imgPreview.src = e.target.result;
      }
    }
    reader.readAsDataURL(file);
  } else if (imgPreview) {
    imgPreview.src = ""; // Clear preview if no file
  }
}
  
  // Feedback Form Submit Handler
  document.getElementById("feedbackForm")?.addEventListener("submit", function (event) {
    event.preventDefault();
  
    const rating = document.getElementById("rating").value;
    const comment = document.getElementById("comment").value;
  
    if (rating >= 1 && rating <= 5 && comment) {
      alert("Thank you for your feedback!");
      document.getElementById("feedbackForm").reset();
    } else {
      alert("Please provide a valid rating and comment.");
    }
  });
  
  // Load Saved Stories on Page Load
  document.addEventListener("DOMContentLoaded", function () {
    const storiesContainer = document.getElementById("stories-container");
  
    if (storiesContainer) {
      let savedStories = JSON.parse(localStorage.getItem("savedStories")) || [];
  
      if (savedStories.length === 0) {
        storiesContainer.innerHTML = <p class="empty-message">No stories saved yet.</p>;
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
  
  // Save Story
  function saveStory() {
    let storyText = document.getElementById("generated-story")?.innerText;
    if (!storyText) return;
  
    let savedStories = JSON.parse(localStorage.getItem("savedStories")) || [];
    savedStories.push(storyText);
    localStorage.setItem("savedStories", JSON.stringify(savedStories));
  
    alert("Story saved successfully!");
  }
  
  // Delete Story
  function deleteStory(index) {
    let savedStories = JSON.parse(localStorage.getItem("savedStories")) || [];
    savedStories.splice(index, 1);
    localStorage.setItem("savedStories", JSON.stringify(savedStories));
    location.reload(); // Refresh page to update list
  }
  
  // Redirect profile button to profile page
  document.querySelector(".profile-btn")?.addEventListener("click", function () {
    window.location.href = "profile.html";
  });
  
  // Logout Function
  document.getElementById("logout")?.addEventListener("click", function () {
    localStorage.clear();
    window.location.href = "login.html";
  });
  
  // Basic Upload Handler - For standalone JS + HTML projects
  document.getElementById("uploadBtn")?.addEventListener("click", function () {
    const fileInput = document.getElementById("imageUpload");
    const file = fileInput.files[0];
  
    if (!file) {
      alert("Please select a file first.");
      return;
    }
  
    const formData = new FormData();
    formData.append("image", file);
  
    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Upload failed");
        }
        return response.json();
      })
      .then((data) => {
        alert("Image uploaded successfully!");
        console.log(data);
      })
      .catch((error) => {
        console.error("Error uploading image:", error);
        alert("Image upload failed!");
      });
  });