// Gráfico de barras - Movimentação por zona
const zonaCtx = document.getElementById('zonaChart').getContext('2d');
const zonaChart = new Chart(zonaCtx, {
    type: 'bar',
    data: {
        labels: ['Zona 1', 'Zona 2', 'Zona 3', 'Zona 4'],
        datasets: [{
            label: 'Visitas',
            data: [320, 450, 280, 198],
            backgroundColor: [
                'rgba(52, 152, 219, 0.7)',
                'rgba(46, 204, 113, 0.7)',
                'rgba(155, 89, 182, 0.7)',
                'rgba(241, 196, 15, 0.7)'
            ],
            borderColor: [
                'rgba(52, 152, 219, 1)',
                'rgba(46, 204, 113, 1)',
                'rgba(155, 89, 182, 1)',
                'rgba(241, 196, 15, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Gráfico de pizza - Distribuição por zona
const pieCtx = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Zona 1 - Cardio', 'Zona 2 - Musculação', 'Zona 3 - Funcional', 'Zona 4 - Alongamento'],
        datasets: [{
            data: [25, 35, 20, 20],
            backgroundColor: [
                'rgba(52, 152, 219, 0.7)',
                'rgba(46, 204, 113, 0.7)',
                'rgba(155, 89, 182, 0.7)',
                'rgba(241, 196, 15, 0.7)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});

// Gráfico de linha - Padrão de uso por horário
const horarioCtx = document.getElementById('horarioChart').getContext('2d');
const horarioChart = new Chart(horarioCtx, {
    type: 'line',
    data: {
        labels: ['6h', '8h', '10h', '12h', '14h', '16h', '18h', '20h', '22h'],
        datasets: [{
            label: 'Visitas por hora',
            data: [30, 85, 60, 45, 55, 90, 150, 180, 70],
            fill: false,
            backgroundColor: 'rgba(231, 76, 60, 0.7)',
            borderColor: 'rgba(231, 76, 60, 1)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Gráfico de linha - Tendência de ocupação
const tendenciaCtx = document.getElementById('tendenciaChart').getContext('2d');
const tendenciaChart = new Chart(tendenciaCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
        datasets: [{
            label: 'Taxa de ocupação (%)',
            data: [65, 59, 70, 71, 68, 72, 75],
            fill: false,
            backgroundColor: 'rgba(52, 152, 219, 0.7)',
            borderColor: 'rgba(52, 152, 219, 1)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false,
                min: 50,
                max: 100
            }
        }
    }
});