document.addEventListener("DOMContentLoaded", function () {
    const userLoginForm = document.getElementById("user-login");
    const adminLoginForm = document.getElementById("admin-login");
    const signupForm = document.getElementById("signup-form");
    const tabButtons = document.querySelectorAll(".tab-btn");

    // --- Tab switch logic ---
    tabButtons.forEach(button => {
        button.addEventListener("click", function () {
            const tab = this.getAttribute("data-tab");

            // Hide all forms
            userLoginForm.classList.add("hidden");
            adminLoginForm.classList.add("hidden");
            signupForm.classList.add("hidden");

            // Show the selected form
            document.getElementById(tab).classList.remove("hidden");

            // Update active button styling
            tabButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // --- User Login (AJAX) ---
    userLoginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const email = userLoginForm.querySelector("input[name='email']").value.trim();
        const password = userLoginForm.querySelector("input[name='password']").value.trim();

        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/user"; // Redirect to user dashboard
            } else {
                alert("Invalid login credentials!");
            }
        })
        .catch(error => {
            console.error("Error during login:", error);
        });
    });

    // --- Signup ---
    signupForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const username = document.getElementById("signup-username").value.trim();
        const email = document.getElementById("signup-email").value.trim();
        const password = document.getElementById("signup-password").value.trim();

        fetch("/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                // Go back to user login after successful signup
                signupForm.classList.add("hidden");
                userLoginForm.classList.remove("hidden");
                tabButtons.forEach(btn => btn.classList.remove("active"));
                document.querySelector("[data-tab='user-login']").classList.add("active");
            }
        })
        .catch(error => console.error("Signup error:", error));
    });

    // --- Admin Login ---
    adminLoginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const adminUsername = document.querySelector("#admin-login input[name='username']").value.trim();
        const adminPassword = document.querySelector("#admin-login input[name='password']").value.trim();

        if (adminUsername === "Emil" && adminPassword === "123") {
            window.location.href = "/admin"; // Adjust to your actual admin route
        } else {
            alert("Invalid admin credentials! Please try again.");
        }
    });
});