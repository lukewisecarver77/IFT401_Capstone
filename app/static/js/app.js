// static/js/app.js

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

async function loadMarketOverview() {
    const data = await apiRequest("/market/stocks");
    const container = document.querySelector(".stock-table-placeholder");

    if (data && Array.isArray(data.stocks) && data.stocks.length > 0) {
        // Build table
        let html = `<table>
                        <thead>
                            <tr>
                                <th>Ticker</th>
                                <th>Company</th>
                                <th>Price</th>
                                <th>Volume</th>
                            </tr>
                        </thead>
                        <tbody>`;
        data.stocks.forEach(stock => {
            html += `<tr>
                        <td>${stock.ticker}</td>
                        <td>${stock.company_name}</td>
                        <td>${stock.price.toFixed(2)}</td>
                        <td>${stock.volume}</td>
                    </tr>`;
        });
        html += `</tbody></table>`;
        container.innerHTML = html;
    } else {
        container.innerHTML = "<p>No stocks available.</p>";
    }
}

