// Helper Functions
function showMessage(text, isError = false) {
    let box = document.getElementById("admin-message-box");
    if (!box) {
        box = document.createElement("div");
        box.id = "admin-message-box";
        box.style.padding = "10px";
        box.style.margin = "10px 0";
        box.style.borderRadius = "5px";
        box.style.fontWeight = "bold";
        document.querySelector("main").prepend(box);
    }
    box.style.background = isError ? "#ffcccc" : "#ccffcc";
    box.style.border = isError ? "2px solid red" : "2px solid green";
    box.textContent = text;
}

async function apiRequest(endpoint, method = "GET", data = null) {
    const options = { method, headers: { "Content-Type": "application/json" }, credentials: "include" };
    if (data) options.body = JSON.stringify(data);
    try {
        const res = await fetch(endpoint, options);
        const json = await res.json();
        return { ok: res.ok, data: json };
    } catch (err) {
        console.error("API error:", err);
        return { ok: false, data: { error: "Network error" } };
    }
}

function showAdminIndicator(username) {
    let el = document.getElementById("admin-indicator");
    if (!el) {
        el = document.createElement("div");
        el.id = "admin-indicator";
        el.style.padding = "8px";
        el.style.margin = "8px 0";
        el.style.backgroundColor = "#e0f7fa";
        el.style.color = "#006064";
        el.style.fontWeight = "bold";
        el.style.borderRadius = "4px";
        document.querySelector("header").appendChild(el);
    }
    el.textContent = `Currently logged in as admin: ${username}`;
}

// Stock Table
async function loadStocks() {
    const tableBody = document.querySelector("#stock-table tbody");
    const { ok, data } = await apiRequest("/admin/stocks");

    if (!ok || !data.stocks) {
        tableBody.innerHTML = `<tr><td colspan="5">Failed to load stocks</td></tr>`;
        return;
    }
    if (data.stocks.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="5">No stocks available</td></tr>`;
        return;
    }

    tableBody.innerHTML = "";
    data.stocks.forEach(stock => {
        const row = `
            <tr>
                <td>${stock.company_name}</td>
                <td>${stock.ticker}</td>
                <td>${stock.volume}</td>
                <td>${stock.price.toFixed(2)}</td>
                <td>
                    <button class="edit-btn" data-ticker="${stock.ticker}">Edit</button>
                    <button class="delete-btn" data-ticker="${stock.ticker}">Delete</button>
                </td>
            </tr>`;
        tableBody.insertAdjacentHTML("beforeend", row);
    });
}

async function handleTableActions(e) {
    const ticker = e.target.dataset.ticker;
    if (!ticker) return;
    const row = e.target.closest("tr");

    if (e.target.classList.contains("edit-btn")) {
        row.children[0].innerHTML = `<input type="text" value="${row.children[0].textContent}" />`;
        row.children[1].innerHTML = `<input type="text" value="${row.children[1].textContent}" />`;
        row.children[2].innerHTML = `<input type="number" value="${row.children[2].textContent}" min="1" />`;
        row.children[3].innerHTML = `<input type="number" value="${row.children[3].textContent}" step="0.01" />`;
        e.target.textContent = "Save";
        e.target.classList.replace("edit-btn", "save-btn");
    } else if (e.target.classList.contains("save-btn")) {
        const company_name = row.children[0].querySelector("input").value;
        const new_ticker = row.children[1].querySelector("input").value;
        const volume = row.children[2].querySelector("input").value;
        const price = row.children[3].querySelector("input").value;

        const { ok, data } = await apiRequest(`/admin/update_stock/${ticker}`, "POST", { company_name, ticker: new_ticker, volume, price });
        if (!ok) return showMessage(data.error || "Failed to update stock", true);
        showMessage(data.message);
        loadStocks();
    } else if (e.target.classList.contains("delete-btn")) {
        if (!confirm(`Are you sure you want to delete ${ticker}?`)) return;
        const { ok, data } = await apiRequest(`/admin/delete_stock/${ticker}`, "DELETE");
        if (!ok) return showMessage(data.error || "Failed to delete stock", true);
        showMessage(data.message);
        loadStocks();
    }
}

async function handleCreateStock(e) {
    e.preventDefault();
    const company_name = document.getElementById("company-name").value;
    const ticker = document.getElementById("ticker").value;
    const volume = document.getElementById("volume").value;
    const initial_price = document.getElementById("initial-price").value;

    const { ok, data } = await apiRequest("/admin/create_stock", "POST", { company_name, ticker, volume, initial_price });
    if (!ok) return showMessage(data.error || "Error creating stock", true);

    showMessage(data.message);
    loadStocks();

    ["company-name", "ticker", "volume", "initial-price"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
}

// Market Settings
let interactiveHolidays = [];

async function loadMarketSettings() {
    const { ok, data } = await apiRequest("/admin/market_settings");
    if (!ok) return showMessage("Failed to load market settings", true);

    document.querySelector("#display-market-hours .value").textContent = `${data.open_time || 'N/A'} – ${data.close_time || 'N/A'}`;
    document.querySelector("#weekdays-value").textContent = data.weekdays_only ? "Yes" : "No";

    interactiveHolidays = data.holidays || [];
    renderHolidayCalendar(interactiveHolidays, data.weekdays_only);
}

async function handleMarketHours(e) {
    e.preventDefault();
    const open = document.getElementById("market-open").value.split(":");
    const close = document.getElementById("market-close").value.split(":");

    const { ok, data } = await apiRequest("/admin/update_market_hours", "POST", {
        open_hour: open[0], open_minute: open[1], close_hour: close[0], close_minute: close[1]
    });
    if (!ok) return showMessage(data.error || "Failed to update market hours", true);

    showMessage(data.message);
    document.getElementById("market-open").value = "";
    document.getElementById("market-close").value = "";
    loadMarketSettings();
}

async function toggleWeekdays(up = true) {
    const weekdaysEl = document.querySelector("#weekdays-value");
    const newValue = up;

    const { ok, data } = await apiRequest("/admin/update_market_schedule", "POST", { weekdays_only: newValue, holidays: interactiveHolidays });
    if (!ok) return showMessage(data.error || "Failed to toggle weekdays", true);

    weekdaysEl.textContent = newValue ? "Yes" : "No";
    loadMarketSettings();
}

// Holiday Calendar
function renderHolidayCalendar(holidays = [], weekdaysOnly = true) {
    let calendarEl = document.getElementById("holiday-calendar");
    if (!calendarEl) {
        calendarEl = document.createElement("div");
        calendarEl.id = "holiday-calendar";
        calendarEl.style.display = "grid";
        calendarEl.style.gridTemplateColumns = "repeat(7, 1fr)";
        calendarEl.style.gap = "3px";
        document.querySelector("#display-holidays").appendChild(calendarEl);
    }
    calendarEl.innerHTML = "";

    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) calendarEl.appendChild(document.createElement("div"));

    for (let day = 1; day <= lastDate; day++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const dayEl = document.createElement("div");
        dayEl.textContent = day;
        dayEl.classList.add("calendar-day");
        dayEl.style.padding = "5px";
        dayEl.style.textAlign = "center";
        dayEl.style.borderRadius = "4px";
        dayEl.style.cursor = "pointer";
        dayEl.style.userSelect = "none";

        const weekDay = new Date(year, month, day).getDay();
        if ((weekdaysOnly && (weekDay === 0 || weekDay === 6))) dayEl.style.opacity = "0.3";
        if (holidays.includes(dateStr)) dayEl.style.backgroundColor = "#ffcccc";
        if (day === today.getDate()) dayEl.style.border = "2px solid #007bff";

        dayEl.addEventListener("click", () => {
            if (interactiveHolidays.includes(dateStr)) {
                interactiveHolidays = interactiveHolidays.filter(d => d !== dateStr);
                dayEl.style.backgroundColor = "";
            } else {
                interactiveHolidays.push(dateStr);
                dayEl.style.backgroundColor = "#ffcccc";
            }
        });

        calendarEl.appendChild(dayEl);
    }
}

async function saveHolidays() {
    const { ok, data } = await apiRequest("/admin/update_market_schedule", "POST", {
        weekdays_only: document.querySelector("#weekdays-value").textContent === "Yes",
        holidays: interactiveHolidays
    });
    if (!ok) return showMessage(data.error || "Failed to save holidays", true);
    showMessage("Holidays saved successfully!");
    loadMarketSettings(); // refresh calendar and display
}


// Init
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/auth/me", { credentials: "include" });
        const user = await res.json();

        if (!user.is_admin) {
            alert("You're not an admin, can't access admin page");
            window.location.href = "/";
            return;
        }

        showAdminIndicator(user.username);

        loadStocks();
        loadMarketSettings();

        document.getElementById("create-stock-form").addEventListener("submit", handleCreateStock);
        document.getElementById("market-hours-form").addEventListener("submit", handleMarketHours);
        document.querySelector("#stock-table tbody").addEventListener("click", handleTableActions);

        document.getElementById("weekdays-up").addEventListener("click", () => toggleWeekdays(true));
        document.getElementById("weekdays-down").addEventListener("click", () => toggleWeekdays(false));
        document.getElementById("save-holidays-btn").addEventListener("click", saveHolidays);


    } catch (err) {
        console.error(err);
        alert("Error checking admin status");
        window.location.href = "/";
    }
});
