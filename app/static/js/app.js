const API_BASE_URL = "";

// --- Helper for API calls ---
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

// Loads Current Market Stocks
async function loadMarketOverview() {
    const data = await apiRequest("/market/stocks");
    const tbody = document.querySelector("#stock-table tbody");

    if (!tbody) {
        console.error("Table body #stock-table tbody not found.");
        return;
    }

    tbody.innerHTML = "";

    if (data && Array.isArray(data.stocks) && data.stocks.length > 0) {

        data.stocks.forEach(stock => {
            const row = `
                <tr>
                    <td>${stock.ticker}</td>
                    <td>${stock.company_name}</td>
                    <td>${stock.price.toFixed(2)}</td>
                    <td>${stock.volume}</td>
                </tr>
            `;
            tbody.insertAdjacentHTML("beforeend", row);
        });

    } else {
        tbody.innerHTML = `<tr><td colspan="4">No stocks available.</td></tr>`;
    }
}


document.addEventListener("DOMContentLoaded", loadMarketOverview);
