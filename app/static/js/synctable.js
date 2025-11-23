const stockHighLow = {};

async function updateStockTables() {
    try {
        const response = await fetch("/market/stocks/data");
        const stocks = await response.json();

        stocks.forEach(stock => {
            // Initialize high/low if not set
            if (!stockHighLow[stock.ticker]) {
                stockHighLow[stock.ticker] = {
                    high: stock.price,
                    low: stock.price
                };
            } else {
                // Update high/low dynamically
                if (stock.price > stockHighLow[stock.ticker].high) {
                    stockHighLow[stock.ticker].high = stock.price;
                }
                if (stock.price < stockHighLow[stock.ticker].low) {
                    stockHighLow[stock.ticker].low = stock.price;
                }
            }
            stock.high = stockHighLow[stock.ticker].high;
            stock.low = stockHighLow[stock.ticker].low;
        });

        // Update home page table
        const homeTableBody = document.querySelector("#stock-table tbody");
        if (homeTableBody) {
            homeTableBody.innerHTML = "";
            stocks.forEach(stock => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${stock.ticker}</td>
                    <td>${stock.company_name}</td>
                    <td>$${stock.price.toFixed(2)}</td>
                    <td>${stock.volume}</td>
                    <td>$${(stock.price * stock.volume).toFixed(2)}</td>
                    <td>$${stock.high.toFixed(2)}</td>
                    <td>$${stock.low.toFixed(2)}</td>
                    <td>$${stock.price.toFixed(2)}</td>
                `;
                homeTableBody.appendChild(row);
            });
        }

        // Update trade page table
        const tradeTableBody = document.querySelector("#trade-stock-table tbody");
        if (tradeTableBody) {
            tradeTableBody.innerHTML = "";
            stocks.forEach(stock => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${stock.ticker}</td>
                    <td>${stock.company_name}</td>
                    <td>$${stock.price.toFixed(2)}</td>
                    <td>${stock.volume}</td>
                    <td>$${(stock.price * stock.volume).toFixed(2)}</td>
                    <td>$${stock.high.toFixed(2)}</td>
                    <td>$${stock.low.toFixed(2)}</td>
                    <td>$${stock.price.toFixed(2)}</td>
                `;
                tradeTableBody.appendChild(row);
            });
        }

    } catch (error) {
        console.error("Error updating stock tables:", error);
    }
}

// Poll every 10 seconds (10000 ms)
setInterval(updateStockTables, 10000);

// Initial load
updateStockTables();
