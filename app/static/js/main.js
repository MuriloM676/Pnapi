// Main JavaScript file for PNCP API Client

// Global configuration
const CONFIG = {
    API_BASE: '/api',
    TIMEOUT: 30000
};

// Utility functions
const Utils = {
    formatCurrency: function(value) {
        return parseFloat(value).toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    },
    
    formatDate: function(dateString) {
        if (!dateString) return 'N/A';
        // Handle both date formats that might come from the API
        let date;
        if (dateString.includes('T')) {
            date = new Date(dateString);
        } else if (dateString.length === 8) {
            // Assume format is YYYYMMDD
            const year = dateString.substring(0, 4);
            const month = dateString.substring(4, 6);
            const day = dateString.substring(6, 8);
            date = new Date(year, month - 1, day);
        } else {
            return dateString;
        }
        return date.toLocaleDateString('pt-BR');
    },
    
    getModalidadeName: function(code) {
        const modalidades = {
            '1': 'Concorrência',
            '2': 'Tomada de Preços',
            '3': 'Convite',
            '4': 'Concurso',
            '5': 'Leilão',
            '6': 'Pregão',
            '7': 'Dispensa de Licitação',
            '8': 'Inexigibilidade de Licitação',
            '12': 'Credenciamento'
        };
        return modalidades[code] || code;
    },
    
    showLoading: function(elementId) {
        $(elementId).removeClass('d-none');
    },
    
    hideLoading: function(elementId) {
        $(elementId).addClass('d-none');
    },
    
    showError: function(elementId, message) {
        $(elementId).removeClass('d-none').text(message);
    },
    
    hideError: function(elementId) {
        $(elementId).addClass('d-none');
    },
    
    truncateText: function(text, maxLength) {
        if (!text) return 'N/A';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
};

// API Service
const ApiService = {
    get: function(endpoint, params = {}) {
        return $.get({
            url: CONFIG.API_BASE + endpoint,
            data: params,
            timeout: CONFIG.TIMEOUT
        });
    }
};

// Chart Service
const ChartService = {
    createBarChart: function(canvasId, data, config) {
        // Destroy existing chart if it exists
        if (window[canvasId + 'Chart']) {
            window[canvasId + 'Chart'].destroy();
        }
        
        const ctx = document.getElementById(canvasId).getContext('2d');
        const labels = data.labels;
        const values = data.values;
        
        // Generate different colors for each bar
        const backgroundColors = labels.map((_, i) => {
            const colors = config.colors.background;
            return colors[i % colors.length];
        });
        
        const borderColors = labels.map((_, i) => {
            const colors = config.colors.border;
            return colors[i % colors.length];
        });
        
        window[canvasId + 'Chart'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: config.label,
                    data: values,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: config.tooltipCallbacks
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: config.yAxisTitle
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: config.xAxisTitle
                        }
                    }
                }
            }
        });
    }
};

// Export for global access
window.App = {
    Utils: Utils,
    ApiService: ApiService,
    ChartService: ChartService
};