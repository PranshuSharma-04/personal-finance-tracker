
document.addEventListener("DOMContentLoaded", function () {

    const monthlyData = JSON.parse(
        document.getElementById("monthly-data").textContent
    );

    const categoryData = JSON.parse(
        document.getElementById("category-data").textContent
    );

    Chart.defaults.color = "#94a3b8";
    Chart.defaults.font.family = "Inter, Arial";

    // Monthly Income vs Expenses
    new Chart(document.getElementById("monthlyChart"), {
        type: "bar",
        data: {
            labels: monthlyData.map(item => item.month),
            datasets: [
                {
                    label: "Income",
                    data: monthlyData.map(item => item.income),
                    backgroundColor: "#34d399",
                    borderRadius: 6
                },
                {
                    label: "Expenses",
                    data: monthlyData.map(item => item.expenses),
                    backgroundColor: "#8b7cff",
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom" }
            },
            scales: {
                x: { grid: { display: false } },
                y: {
                    beginAtZero: true,
                    grid: { color: "#273449" }
                }
            }
        }
    });

    // Category-wise Expenses
    new Chart(document.getElementById("categoryChart"), {
        type: "doughnut",
        data: {
            labels: categoryData.map(item => item.category),
            datasets: [{
                data: categoryData.map(item => item.total),
                backgroundColor: [
                    "#8b7cff",
                    "#34d399",
                    "#fb7185",
                    "#38bdf8",
                    "#fbbf24",
                    "#c084fc",
                    "#f97316"
                ],
                borderColor: "#111a2a",
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "68%",
            plugins: {
                legend: { position: "bottom" }
            }
        }
    });

});

