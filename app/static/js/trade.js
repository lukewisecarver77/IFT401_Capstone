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

// Load Current Market Stocks
async function loadMarketStocks() {
    const data = await apiRequest("/trade/stocks");
    const tbody = document.querySelector("#market-stocks tbody");
    const buySelect = document.querySelector("#buy-stock-select");

    if (!tbody || !buySelect) return;

    tbody.innerHTML = "";
    buySelect.innerHTML = '<option value="">--Choose Stock--</option>';

    if (data && Array.isArray(data.stocks)) {
        data.stocks.forEach(stock => {
            tbody.insertAdjacentHTML("beforeend", `
                <tr>
                    <td>${stock.ticker}</td>
                    <td>${stock.company_name}</td>
                    <td>$${(stock.price ?? 0).toFixed(2)}</td>
                    <td>${stock.volume ?? 0}</td>
                </tr>
            `);

            buySelect.insertAdjacentHTML("beforeend",
                `<option value="${stock.ticker}" data-price="${stock.price ?? 0}">${stock.ticker} - ${stock.company_name}</option>`);
        });
    } else {
        tbody.innerHTML = `<tr><td colspan="4">No stocks available</td></tr>`;
    }
}


async function loadUserData() {
    const userData = await apiRequest("/users/me");
    if (!userData) return;

    const balanceContainer = document.querySelector("#cash-balance p");
    if (balanceContainer) balanceContainer.textContent = `$${userData.balance.toFixed(2)}`;

    const tableBody = document.querySelector("#owned-stocks tbody");
    if (!tableBody) return;

    const portfolioData = await apiRequest(`/users/${userData.username}/portfolio`);
    tableBody.innerHTML = "";

    const sellSelect = document.querySelector("#sell-stock-select");
    if (!sellSelect) return;
    sellSelect.innerHTML = '<option value="">--Choose Stock--</option>';

    if (portfolioData && Array.isArray(portfolioData.portfolio) && portfolioData.portfolio.length > 0) {
        portfolioData.portfolio.forEach(item => {
            const row = `
                <tr>
                    <td>${item.ticker}</td>
                    <td>${item.quantity}</td>
                    <td>$${item.current_price.toFixed(2)}</td>
                    <td>$${item.total_value.toFixed(2)}</td>
                </tr>
            `;
            tableBody.insertAdjacentHTML("beforeend", row);

            sellSelect.insertAdjacentHTML("beforeend",
                `<option value="${item.ticker}" data-price="${item.current_price}">${item.ticker} - ${item.company_name ?? item.ticker}</option>`);
        });
    } else {
        tableBody.innerHTML = `<tr><td colspan="4">No stocks owned</td></tr>`;
        sellSelect.innerHTML = '<option value="">--No stocks owned--</option>';
    }
}

async function handleTrade(event, action) {
    event.preventDefault();

    const selectEl = action === "buy" ? document.querySelector("#buy-stock-select") : document.querySelector("#sell-stock-select");
    const qtyEl = action === "buy" ? document.querySelector("#buy-quantity") : document.querySelector("#sell-quantity");

    const stock = selectEl.value;
    const quantity = parseInt(qtyEl.value);
    const price = parseFloat(selectEl.selectedOptions[0]?.dataset.price ?? 0);

    if (!stock || !quantity || quantity <= 0) {
        alert("Please select a stock and enter a valid quantity.");
        return;
    }

    const total = (price * quantity).toFixed(2);
    const confirmMsg = `Confirm ${action} of ${quantity} shares of ${stock} for $${total}?`;

    if (!confirm(confirmMsg)) {
        alert("Trade cancelled.");
        return;
    }

    const response = await apiRequest(`/trade/${action}`, "POST", { ticker: stock, quantity });

    if (!response) {
        alert("Trade failed due to API error.");
        return;
    }

    if (response.error) {
        alert(`Error: ${response.error}`);
    } else {
        alert(response.message || `Successfully ${action}ed ${quantity} shares of ${stock}`);
        await loadUserData();
        await loadMarketStocks();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadMarketStocks();
    loadUserData();

    document.querySelector("#buy-form").addEventListener("submit", e => handleTrade(e, "buy"));
    document.querySelector("#sell-form").addEventListener("submit", e => handleTrade(e, "sell"));
    document.querySelector("#buy-quantity").value = "";
    document.querySelector("#sell-quantity").value = "";

});
