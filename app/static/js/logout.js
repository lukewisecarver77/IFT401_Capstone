// Logout Script
document.addEventListener("DOMContentLoaded", () => {
    const logoutForm = document.getElementById("logout-form");
    if (logoutForm) {
        logoutForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            try {
                const res = await fetch("/auth/logout", {
                    method: "POST",
                    credentials: "include",
                });
                if (res.ok) {
                    window.location.href = "/";
                } else {
                    alert("Logout failed.");
                }
            } catch (err) {
                console.error("Logout error:", err);
                alert("Logout failed.");
            }
        });
    }
});
