const API_BASE_URL = "";

// API Request Helper 
async function apiRequest(endpoint, method = "GET", data = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
        credentials: "include"
    };
    if (data) options.body = JSON.stringify(data);

    try {
        const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || `Request failed: ${res.status}`);
        return json;
    } catch (err) {
        console.error("API error:", err);
        return { error: err.message || "API error" };
    }
}

// Market Status
let marketOpen = true;

async function checkMarketStatus() {
    const settings = await apiRequest("/admin/market_settings");
    if (settings.error) {
        console.warn("Could not fetch market settings:", settings.error);
        marketOpen = true;
        return;
    }

    const now = new Date();
    const todayStr = now.toISOString().slice(0, 10);
    const currentTime = now.getHours() + now.getMinutes() / 60;

    let openHour = 9, closeHour = 16;
    if (settings.open_time) openHour = parseInt(settings.open_time.split(":")[0]) + parseInt(settings.open_time.split(":")[1]) / 60;
    if (settings.close_time) closeHour = parseInt(settings.close_time.split(":")[0]) + parseInt(settings.close_time.split(":")[1]) / 60;

    const weekday = now.getDay(); // 0 = Sunday, 6 = Saturday
    const isWeekend = settings.weekdays_only && (weekday === 0 || weekday === 6);
    const isHoliday = settings.holidays?.includes(todayStr);

    marketOpen = !isWeekend && !isHoliday && currentTime >= openHour && currentTime <= closeHour;

    const tradeMessageEl = document.getElementById("trade-status-message");
    if (!tradeMessageEl) {
        const msg = document.createElement("div");
        msg.id = "trade-status-message";
        msg.style.color = "#b71c1c";
        msg.style.fontWeight = "bold";
        msg.style.margin = "5px 0";
        const parent = document.querySelector("#buy-form")?.parentElement || document.body;
        parent.insertBefore(msg, parent.firstChild);
    }

    document.getElementById("trade-status-message").textContent = marketOpen ? "" : "Cannot trade outside of market hours or on holidays";

    document.querySelector("#buy-form button").disabled = !marketOpen;
    document.querySelector("#sell-form button").disabled = !marketOpen;
}

// Load Stocks
async function loadMarketStocks() {
    const data = await apiRequest("/trade/stocks");
    const tbody = document.querySelector("#market-stocks tbody");
    const buySelect = document.querySelector("#buy-stock-select");
    if (!tbody || !buySelect) return;

    tbody.innerHTML = "";
    buySelect.innerHTML = '<option value="">--Choose Stock--</option>';

    if (data?.stocks?.length) {
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

// Load User Portfolio
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

    if (portfolioData?.portfolio?.length) {
        portfolioData.portfolio.forEach(item => {
            tableBody.insertAdjacentHTML("beforeend", `
                <tr>
                    <td>${item.ticker}</td>
                    <td>${item.quantity}</td>
                    <td>$${item.current_price.toFixed(2)}</td>
                    <td>$${item.total_value.toFixed(2)}</td>
                </tr>
            `);
            sellSelect.insertAdjacentHTML("beforeend",
                `<option value="${item.ticker}" data-price="${item.current_price}">${item.ticker} - ${item.company_name ?? item.ticker}</option>`);
        });
    } else {
        tableBody.innerHTML = `<tr><td colspan="4">No stocks owned</td></tr>`;
        sellSelect.innerHTML = '<option value="">--No stocks owned--</option>';
    }
}

// Trade Handling 
async function handleTrade(event, action) {
    event.preventDefault();
    if (!marketOpen) {
        alert("Cannot trade outside of market hours or on holidays.");
        return;
    }

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
    if (!confirm(`Confirm ${action} of ${quantity} shares of ${stock} for $${total}?`)) {
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

// Initialization
document.addEventListener("DOMContentLoaded", async () => {
    await checkMarketStatus();
    loadMarketStocks();
    loadUserData();

    document.querySelector("#buy-form").addEventListener("submit", e => handleTrade(e, "buy"));
    document.querySelector("#sell-form").addEventListener("submit", e => handleTrade(e, "sell"));
});
