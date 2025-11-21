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

// Transaction Display
async function loadTransactions() {
    const userData = await apiRequest("/users/me");
    if (!userData) return;

    const tableBody = document.querySelector("#transaction-history tbody");
    if (!tableBody) return;

    const transactionsData = await apiRequest(`/users/${userData.username}/transactions`);
    tableBody.innerHTML = "";

    if (transactionsData && Array.isArray(transactionsData.transactions) && transactionsData.transactions.length > 0) {
        transactionsData.transactions.forEach(tx => {
            const total = (tx.price * tx.quantity).toFixed(2);
            const row = `
                <tr>
                    <td>${tx.timestamp}</td>
                    <td>${tx.type}</td>
                    <td>${tx.ticker}</td>
                    <td>${tx.quantity}</td>
                    <td>$${tx.price.toFixed(2)}</td>
                    <td>$${total}</td>
                </tr>
            `;
            tableBody.insertAdjacentHTML("beforeend", row);
        });
    } else {
        tableBody.innerHTML = "<tr><td colspan='6'>No transactions found</td></tr>";
    }
}

document.addEventListener("DOMContentLoaded", loadTransactions);
