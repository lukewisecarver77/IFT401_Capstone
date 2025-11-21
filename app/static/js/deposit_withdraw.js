document.addEventListener("DOMContentLoaded", () => {
    const depositForm = document.querySelector("#deposit-funds form");
    const withdrawForm = document.querySelector("#withdraw-funds form");

    // Load current balance
    async function loadCashBalance() {
        const data = await apiRequest("/users/me");
        const balanceContainer = document.querySelector("#cash-balance p");
        if (data && data.balance !== undefined) {
            balanceContainer.textContent = `$${data.balance.toFixed(2)}`;
        } else {
            balanceContainer.textContent = "Unable to fetch balance";
        }
    }

    // Deposit event
    depositForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const amount = parseFloat(document.querySelector("#deposit-amount").value);
        const res = await apiRequest("/users/me/deposit", "POST", { amount });
        if (res && !res.error) {
            alert(`Deposit successful! New balance: $${res.new_balance.toFixed(2)}`);
        } else {
            alert(res.error || "Deposit failed");
        }
        loadCashBalance();
        depositForm.reset();
    });

    // Withdraw event
    withdrawForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const amount = parseFloat(document.querySelector("#withdraw-amount").value);
        const res = await apiRequest("/users/me/withdraw", "POST", { amount });
        if (res && !res.error) {
            alert(`Withdrawal successful! New balance: $${res.new_balance.toFixed(2)}`);
        } else {
            alert(res.error || "Withdrawal failed");
        }
        loadCashBalance();
        withdrawForm.reset();
    });

    loadCashBalance();
});
