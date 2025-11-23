async function updateStockTable(tableSelector, showDollar = false) {
    const table = document.querySelector(tableSelector);
    if (!table) return;

    const hasActions = table.querySelector("th:nth-child(5)");
    if (hasActions) return;

    try {
        const response = await fetch("/market/stocks");
        const data = await response.json();
        const tbody = table.querySelector("tbody");
        tbody.innerHTML = "";

        data.stocks.forEach(stock => {
            const row = document.createElement("tr");

            const price = showDollar ? `$${stock.price.toFixed(2)}` : stock.price.toFixed(2);

            row.innerHTML = `
                <td>${stock.ticker}</td>
                <td>${stock.company_name}</td>
                <td>${price}</td>
                <td>${stock.volume}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Failed to update stock table:", err);
    }
}

// Run on page load
document.addEventListener("DOMContentLoaded", () => {
    // Index page: show $ before price
    updateStockTable("#stock-table", true);

    // Trade page: show $ before price
    updateStockTable("#market-stocks table", true);

    // Auto-refresh every 10 seconds
    setInterval(() => {
        updateStockTable("#stock-table", true);
        updateStockTable("#market-stocks table", true);
    }, 10000);
});
