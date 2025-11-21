document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#login-form form");
    const messageEl = document.querySelector("#login-form #login-message");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.querySelector("#username").value.trim();
        const password = document.querySelector("#password").value;

        messageEl.textContent = "";

        if (!username || !password) {
            messageEl.textContent = "Please enter both username/email and password.";
            messageEl.style.color = "red";
            return;
        }

        try {
            const res = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ username, password }),
            });

            const data = await res.json();

            if (!res.ok) {
                messageEl.textContent = data.error || "Login failed.";
                messageEl.style.color = "red";
            } else {
                messageEl.textContent = "Login successful! Redirecting...";
                messageEl.style.color = "green";

                setTimeout(() => {
                    window.location.href = "/portfolio";
                }, 1000);
            }
        } catch (err) {
            console.error("Login error:", err);
            messageEl.textContent = "Network error. Please try again.";
            messageEl.style.color = "red";
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
});