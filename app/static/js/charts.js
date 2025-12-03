// Chart Configuration
Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.color = '#64748b';
Chart.defaults.scale.grid.color = 'rgba(148, 163, 184, 0.1)';

function renderBarChart(ctx, data) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Income',
                    data: data.income,
                    backgroundColor: '#10b981', // Emerald 500
                    borderRadius: 4,
                },
                {
                    label: 'Expense',
                    data: data.expense,
                    backgroundColor: '#ef4444', // Red 500
                    borderRadius: 4,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    padding: 12,
                    cornerRadius: 8,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return '₹' + value;
                        }
                    }
                }
            }
        }
    });
}

function renderPieChart(ctx, data) {
    const categories = Object.keys(data);
    const amounts = Object.values(data);

    // Generate colors
    const colors = [
        '#6366f1', '#ec4899', '#8b5cf6', '#10b981', '#f59e0b',
        '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#64748b'
    ];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                data: amounts,
                backgroundColor: colors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += '₹' + context.parsed.toFixed(2);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}
