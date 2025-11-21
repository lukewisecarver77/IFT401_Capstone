// Account Registration
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form-element");
    const messageEl = document.getElementById("register-message");

    form.reset();
    messageEl.textContent = "";

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        messageEl.textContent = "";

        const full_name = document.getElementById("full_name").value.trim();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirm = document.getElementById("confirm-password").value;
        const is_admin = document.getElementById("is-admin") ? document.getElementById("is-admin").checked : false;

        if (password !== confirm) {
            messageEl.textContent = "Passwords do not match";
            messageEl.style.color = "red";
            return;
        }

        try {
            const res = await fetch("/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ full_name, username, email, password, is_admin })
            });

            const data = await res.json();

            if (!res.ok) {
                messageEl.textContent = data.error || "Registration failed";
                messageEl.style.color = "red";
                return;
            }

            messageEl.textContent = "Registration successful! Redirecting...";
            messageEl.style.color = "green";

            await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            setTimeout(() => {
                window.location.href = "/portfolio";
            }, 1000);

        } catch (err) {
            console.error(err);
            messageEl.textContent = "Network error";
            messageEl.style.color = "red";
        }

        form.reset();
    });
});

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/auth/me", { credentials: "include" });
        if (!res.ok) {
            console.log("Not logged in");
            return;
        }
        const user = await res.json();
        console.log("Current user:", user);
        if (user.is_admin) {
            console.log("User is an admin ✅");
        } else {
            console.log("User is NOT an admin ❌");
        }
    } catch (err) {
        console.error("Error checking user:", err);
    }
});




document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("full_name").value = "";
    document.getElementById("username").value = "";
    document.getElementById("email").value = "";
    document.getElementById("password").value = "";
    document.getElementById("confirm-password").value = "";

    document.querySelector("#register-form form")
        .addEventListener("submit", handleRegister);
});

