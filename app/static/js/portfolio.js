const API_BASE_URL = "";

async function apiRequest(endpoint, method = "GET", data = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
        credentials: "include"
    };
    if (data) options.body = JSON.stringify(data);

    try {
        const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!res.ok) throw new Error(`Request failed: ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error("API error:", err);
        return null;
    }
}

// Load users cash balance 
async function loadCashBalance() {
    const data = await apiRequest("/users/me");
    const balanceContainer = document.querySelector("#cash-balance p");

    if (data && data.balance !== undefined) {
        balanceContainer.textContent = `$${data.balance.toFixed(2)}`;
        return data.username;
    } else {
        balanceContainer.textContent = "Unable to fetch balance";
        return null;
    }
}

// Load users portfolio 
async function loadPortfolio() {
    const username = await loadCashBalance();
    if (!username) return;

    const data = await apiRequest(`/users/${username}/portfolio`);
    const tableBody = document.querySelector("#owned-stocks tbody");
    const summarySection = document.querySelector("#portfolio-summary p");

    if (data && Array.isArray(data.portfolio) && data.portfolio.length > 0) {
        let html = "";
        let totalValue = 0;

        data.portfolio.forEach(item => {
            html += `<tr>
                        <td>${item.ticker}</td>
                        <td>${item.quantity}</td>
                        <td>$${item.current_price.toFixed(2)}</td>
                        <td>$${item.total_value.toFixed(2)}</td>
                    </tr>`;
            totalValue += item.total_value;
        });

        tableBody.innerHTML = html;

        if (summarySection) {
            summarySection.textContent = `Total Portfolio Value: $${totalValue.toFixed(2)}`;
        }

    } else if (data && data.error) {
        tableBody.innerHTML = `<tr><td colspan="4">${data.error}</td></tr>`;
        if (summarySection) summarySection.textContent = "";
    } else {
        tableBody.innerHTML = "<tr><td colspan='4'>No stocks in portfolio</td></tr>";
        if (summarySection) summarySection.textContent = "";
    }
}

document.addEventListener("DOMContentLoaded", loadPortfolio);

