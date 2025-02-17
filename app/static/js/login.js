document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const errorMessage = document.getElementById("errorMessage");

    async function handleFormSubmit(event, url, userData) {
        event.preventDefault();
        errorMessage.textContent = "";

        try {
            const button = event.target.querySelector("button");
            button.disabled = true;
            button.textContent = "Processing...";

            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("session_id", data.session_id);
                window.location.href = "/dashboard";
            } else {
                throw new Error(data.detail);
            }
        } catch (error) {
            errorMessage.textContent = error.message;
        } finally {
            event.target.querySelector("button").disabled = false;
            event.target.querySelector("button").textContent = url.includes("login") ? "Login" : "Register";
        }
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();

            if (!username || !password) {
                errorMessage.textContent = "Please fill in all fields.";
                return;
            }

            handleFormSubmit(event, "/login/", { username, password });
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const firstName = document.getElementById("firstName").value.trim();
            const lastName = document.getElementById("lastName").value.trim();
            const email = document.getElementById("email").value.trim();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();
            const confirmPassword = document.getElementById("confirmPassword").value.trim();

            if (!firstName || !lastName || !email || !username || !password || !confirmPassword) {
                errorMessage.textContent = "Please fill in all fields.";
                return;
            }

            if (password !== confirmPassword) {
                errorMessage.textContent = "Passwords do not match.";
                return;
            }

            handleFormSubmit(
                event, "/register/", { username, email, password }
            );
        });
    }
});
