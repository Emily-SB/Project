document.addEventListener("DOMContentLoaded", function () {
    const userLoginForm = document.getElementById("user-login");
    const adminLoginForm = document.getElementById("admin-login");
    const tabButtons = document.querySelectorAll(".tab-btn");

    function openTab(tab) {
        if (tab === "user") {
            userLoginForm.classList.remove("hidden");
            adminLoginForm.classList.add("hidden");
            tabButtons[0].classList.add("active");
            tabButtons[1].classList.remove("active");
        } else {
            userLoginForm.classList.add("hidden");
            adminLoginForm.classList.remove("hidden");
            tabButtons[1].classList.add("active");
            tabButtons[0].classList.remove("active");
        }
    }

    tabButtons.forEach(button => {
        button.addEventListener("click", function () {
            openTab(this.innerText.toLowerCase().includes("user") ? "user" : "admin");
        });
    });
//
    document.addEventListener("DOMContentLoaded", function () {
        const userLoginForm = document.getElementById("user-login");
        const signupForm = document.getElementById("signup-form");
    
        function openSignup() {
            userLoginForm.classList.add("hidden");
            signupForm.classList.remove("hidden");
        }
    
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
                    signupForm.classList.add("hidden");
                    userLoginForm.classList.remove("hidden");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });

    //

  adminLoginForm.addEventListener("submit", function (event) {
    //event.preventDefault();
    const adminUsername = document.getElementById("admin-username").value.trim();
    const adminPassword = document.getElementById("admin-password").value.trim();

    if (adminUsername === "Emil" && adminPassword === "123") {
        window.location.href = "admin.html";  // Redirect to admin page
    } else {
        alert("Invalid admin credentials! Please try again.");
    }
});


    adminLoginForm.addEventListener("submit", function (event) {
        const adminUsername = document.getElementById("admin-username").value.trim();
        const adminPassword = document.getElementById("admin-password").value.trim();
    
        if (adminUsername === "Emil" && adminPassword === "123") {
            window.location.href = "admin.html";  // Redirect to admin page
        } else {
            alert("Invalid admin credentials! Please try again.");
            event.preventDefault();  // Prevents incorrect login submission
        }
    });
    
    
});

