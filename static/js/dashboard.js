/**
 * Analytixa Dashboard Logic
 * Este script se encarga de renderizar los gráficos usando Chart.js
 */

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('graficoPerformance');
    
    // Si no hay canvas (ej: antes de la búsqueda), salimos de la función
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    
    // Obtenemos los datos que el HTML dejó en la variable global
    const rawData = window.datosGrafico || [];

    // Mapeamos los datos para Chart.js
    const labels = rawData.map(item => item.name);
    const values = rawData.map(item => item.clicks);

    // Creamos el gráfico de barras
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Clics Totales',
                data: values,
                backgroundColor: 'rgba(59, 130, 246, 0.8)', // Azul Analytixa
                borderColor: '#3b82f6',
                borderWidth: 1,
                borderRadius: 6,
                hoverBackgroundColor: '#2563eb'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false // Ocultamos la leyenda para un look más limpio
                },
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleColor: '#f8fafc',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: { size: 11 }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: { size: 10 },
                        maxRotation: 45,
                        minRotation: 0
                    }
                }
            }
        }
    });
});