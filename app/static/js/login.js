document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    const response = await fetch("/login/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("session_id", data.session_id);
        window.location.href = "/dashboard";
    } else {
        document.getElementById("errorMessage").textContent = data.detail;
    }
});
