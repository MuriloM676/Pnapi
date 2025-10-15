/* 
 * Advanced Filters for PNCP API Client
 * Provides enhanced filtering capabilities for tenders search
 */

class AdvancedFilters {
    constructor() {
        this.filters = {
            basic: {},
            advanced: {
                valorMinimo: null,
                valorMaximo: null,
                estados: [],
                modalidades: [],
                orgaosExcluidos: [],
                palavrasChave: [],
                prazoMaximo: null
            }
        };
        
        this.initializeComponents();
    }
    
    initializeComponents() {
        // Initialize Select2 for multiple selections
        this.initMultiSelect();
        
        // Initialize range sliders
        this.initRangeSliders();
        
        // Initialize advanced filter toggles
        this.initToggleControls();
        
        // Bind events
        this.bindEvents();
    }
    
    initMultiSelect() {
        // Multiple UF selection
        $('#multipleUf').select2({
            placeholder: "Selecione os estados",
            multiple: true,
            data: [
                {id: 'AC', text: 'Acre'}, {id: 'AL', text: 'Alagoas'},
                {id: 'AP', text: 'Amapá'}, {id: 'AM', text: 'Amazonas'},
                {id: 'BA', text: 'Bahia'}, {id: 'CE', text: 'Ceará'},
                {id: 'DF', text: 'Distrito Federal'}, {id: 'ES', text: 'Espírito Santo'},
                {id: 'GO', text: 'Goiás'}, {id: 'MA', text: 'Maranhão'},
                {id: 'MT', text: 'Mato Grosso'}, {id: 'MS', text: 'Mato Grosso do Sul'},
                {id: 'MG', text: 'Minas Gerais'}, {id: 'PA', text: 'Pará'},
                {id: 'PB', text: 'Paraíba'}, {id: 'PR', text: 'Paraná'},
                {id: 'PE', text: 'Pernambuco'}, {id: 'PI', text: 'Piauí'},
                {id: 'RJ', text: 'Rio de Janeiro'}, {id: 'RN', text: 'Rio Grande do Norte'},
                {id: 'RS', text: 'Rio Grande do Sul'}, {id: 'RO', text: 'Rondônia'},
                {id: 'RR', text: 'Roraima'}, {id: 'SC', text: 'Santa Catarina'},
                {id: 'SP', text: 'São Paulo'}, {id: 'SE', text: 'Sergipe'},
                {id: 'TO', text: 'Tocantins'}
            ]
        });
        
        // Multiple modalities selection
        $('#multipleModalidades').select2({
            placeholder: "Selecione as modalidades",
            multiple: true,
            data: [
                {id: '1', text: 'Concorrência'},
                {id: '2', text: 'Tomada de Preços'},
                {id: '3', text: 'Convite'},
                {id: '6', text: 'Pregão'},
                {id: '7', text: 'Dispensa de Licitação'},
                {id: '8', text: 'Inexigibilidade de Licitação'},
                {id: '12', text: 'Credenciamento'}
            ]
        });
    }
    
    initRangeSliders() {
        // Value range slider
        if ($('#valorRange').length) {
            $('#valorRange').slider({
                range: true,
                min: 0,
                max: 10000000,
                step: 10000,
                values: [0, 10000000],
                slide: (event, ui) => {
                    $('#valorMinimo').val(this.formatCurrency(ui.values[0]));
                    $('#valorMaximo').val(this.formatCurrency(ui.values[1]));
                    this.updateFilters();
                }
            });
        }
    }
    
    initToggleControls() {
        // Advanced filters toggle
        $('#toggleAdvancedFilters').on('click', () => {
            $('#advancedFiltersPanel').slideToggle();
            const icon = $('#toggleAdvancedFilters i');
            icon.toggleClass('fa-chevron-down fa-chevron-up');
        });
        
        // Quick filter buttons
        this.createQuickFilters();
    }
    
    createQuickFilters() {
        const quickFilters = [
            {
                name: 'Pregões SP',
                filters: {uf: 'SP', codigoModalidadeContratacao: '6'},
                color: 'primary'
            },
            {
                name: 'Valores Altos',
                filters: {valorMinimo: 1000000},
                color: 'success'
            },
            {
                name: 'TI',
                filters: {palavraChave: 'tecnologia informação software hardware'},
                color: 'info'
            },
            {
                name: 'Obras',
                filters: {palavraChave: 'construção obra reforma infraestrutura'},
                color: 'warning'
            }
        ];
        
        const quickFiltersContainer = $('#quickFiltersContainer');
        quickFilters.forEach(filter => {
            const button = $(`
                <button class="btn btn-outline-${filter.color} btn-sm me-2 mb-2 quick-filter-btn" 
                        data-filters='${JSON.stringify(filter.filters)}'>
                    <i class="fas fa-filter"></i> ${filter.name}
                </button>
            `);
            
            button.on('click', () => {
                this.applyQuickFilter(filter.filters);
                this.highlightActiveQuickFilter(button);
            });
            
            quickFiltersContainer.append(button);
        });
    }
    
    bindEvents() {
        // Value inputs
        $('#valorMinimo, #valorMaximo').on('input', this.debounce(() => {
            this.updateFilters();
        }, 500));
        
        // Multiple selects
        $('#multipleUf, #multipleModalidades').on('change', () => {
            this.updateFilters();
        });
        
        // Keywords input
        $('#palavrasChaveAvancada').on('input', this.debounce(() => {
            this.updateFilters();
        }, 300));
        
        // Deadline filter
        $('#prazoMaximo').on('change', () => {
            this.updateFilters();
        });
        
        // Reset filters button
        $('#resetFilters').on('click', () => {
            this.resetAllFilters();
        });
        
        // Save search button
        $('#saveSearch').on('click', () => {
            this.saveCurrentSearch();
        });
    }
    
    updateFilters() {
        // Collect all filter values
        const filters = {
            // Basic filters
            uf: $('#uf').val(),
            codigoModalidadeContratacao: $('#codigoModalidadeContratacao').val(),
            palavraChave: $('#palavraChave').val(),
            dataFinal: $('#dataFinal').val(),
            pagina: $('#pagina').val() || 1,
            tamanhoPagina: $('#tamanhoPagina').val() || 10,
            
            // Advanced filters
            valorMinimo: this.parseCurrency($('#valorMinimo').val()),
            valorMaximo: this.parseCurrency($('#valorMaximo').val()),
            estados: $('#multipleUf').val(),
            modalidades: $('#multipleModalidades').val(),
            palavrasChaveAvancada: $('#palavrasChaveAvancada').val(),
            prazoMaximo: $('#prazoMaximo').val()
        };
        
        // Remove empty values
        Object.keys(filters).forEach(key => {
            if (!filters[key] || (Array.isArray(filters[key]) && filters[key].length === 0)) {
                delete filters[key];
            }
        });
        
        // Show active filters count
        this.updateActiveFiltersCount(filters);
        
        // Make API call
        this.searchWithFilters(filters);
    }
    
    searchWithFilters(filters) {
        // Show loading
        App.Utils.showLoading('#loading');
        
        // Transform filters for API
        const apiFilters = this.transformFiltersForAPI(filters);
        
        // Call API
        App.ApiService.get('/licitacoes/abertas', apiFilters)
            .done((data) => {
                this.displayResults(data);
                this.updateResultsInfo(data, apiFilters);
            })
            .fail((xhr) => {
                this.showError('Erro ao carregar licitações: ' + xhr.responseText);
            })
            .always(() => {
                App.Utils.hideLoading('#loading');
            });
    }
    
    transformFiltersForAPI(filters) {
        const apiFilters = {...filters};
        
        // Handle multiple states
        if (filters.estados && filters.estados.length > 0) {
            // For now, use the first state (API limitation)
            apiFilters.uf = filters.estados[0];
            delete apiFilters.estados;
        }
        
        // Handle multiple modalities
        if (filters.modalidades && filters.modalidades.length > 0) {
            apiFilters.codigoModalidadeContratacao = filters.modalidades[0];
            delete apiFilters.modalidades;
        }
        
        // Combine keywords
        if (filters.palavrasChaveAvancada) {
            const combined = [filters.palavraChave, filters.palavrasChaveAvancada]
                .filter(Boolean)
                .join(' ');
            apiFilters.palavraChave = combined;
        }
        
        delete apiFilters.palavrasChaveAvancada;
        delete apiFilters.valorMinimo; // API doesn't support this yet
        delete apiFilters.valorMaximo; // API doesn't support this yet
        delete apiFilters.prazoMaximo; // API doesn't support this yet
        
        return apiFilters;
    }
    
    displayResults(data) {
        // Filter results on client-side for unsupported API filters
        let filteredData = data.data || [];
        
        // Apply value filters
        const valorMin = this.parseCurrency($('#valorMinimo').val());
        const valorMax = this.parseCurrency($('#valorMaximo').val());
        
        if (valorMin || valorMax) {
            filteredData = filteredData.filter(item => {
                const valor = item.valorTotalEstimado || 0;
                return (!valorMin || valor >= valorMin) && 
                       (!valorMax || valor <= valorMax);
            });
        }
        
        // Apply deadline filter
        const prazoMax = $('#prazoMaximo').val();
        if (prazoMax) {
            const maxDate = new Date();
            maxDate.setDate(maxDate.getDate() + parseInt(prazoMax));
            
            filteredData = filteredData.filter(item => {
                if (!item.dataEncerramentoProposta) return true;
                const endDate = this.parseDate(item.dataEncerramentoProposta);
                return endDate <= maxDate;
            });
        }
        
        // Update data object
        const filteredDataObj = {
            ...data,
            data: filteredData,
            totalRegistros: filteredData.length
        };
        
        // Use existing display function
        if (window.displayResults) {
            window.displayResults(filteredDataObj);
        }
    }
    
    updateActiveFiltersCount(filters) {
        const count = Object.keys(filters).length - 3; // Exclude pagination params
        const badge = $('#activeFiltersCount');
        
        if (count > 0) {
            badge.text(count).removeClass('d-none');
        } else {
            badge.addClass('d-none');
        }
    }
    
    updateResultsInfo(data, filters) {
        const info = $('#resultsInfo');
        if (data.totalRegistros) {
            info.html(`
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    Encontradas <strong>${data.totalRegistros}</strong> licitações
                    ${Object.keys(filters).length > 3 ? 'com filtros aplicados' : ''}
                </div>
            `);
        }
    }
    
    applyQuickFilter(filterData) {
        // Reset current filters
        this.resetAllFilters();
        
        // Apply quick filter
        Object.keys(filterData).forEach(key => {
            const element = $(`#${key}`);
            if (element.length) {
                element.val(filterData[key]).trigger('change');
            }
        });
        
        this.updateFilters();
    }
    
    highlightActiveQuickFilter(activeButton) {
        $('.quick-filter-btn').removeClass('active');
        activeButton.addClass('active');
    }
    
    resetAllFilters() {
        // Reset all form elements
        $('#filterForm')[0].reset();
        
        // Reset Select2 elements
        $('#multipleUf, #multipleModalidades').val(null).trigger('change');
        
        // Reset sliders
        if ($('#valorRange').length) {
            $('#valorRange').slider('values', [0, 10000000]);
        }
        
        // Clear currency inputs
        $('#valorMinimo, #valorMaximo').val('');
        
        // Remove active quick filter
        $('.quick-filter-btn').removeClass('active');
        
        // Hide active filters count
        $('#activeFiltersCount').addClass('d-none');
        
        // Clear results info
        $('#resultsInfo').empty();
    }
    
    saveCurrentSearch() {
        const searchData = {
            filters: this.getCurrentFilters(),
            timestamp: new Date().toISOString(),
            name: prompt('Nome para esta pesquisa:') || `Pesquisa ${Date.now()}`
        };
        
        // Save to localStorage
        const savedSearches = JSON.parse(localStorage.getItem('savedSearches') || '[]');
        savedSearches.unshift(searchData);
        
        // Keep only last 10 searches
        if (savedSearches.length > 10) {
            savedSearches.splice(10);
        }
        
        localStorage.setItem('savedSearches', JSON.stringify(savedSearches));
        
        this.showToast('Pesquisa salva com sucesso!', 'success');
    }
    
    getCurrentFilters() {
        const filters = {};
        $('#filterForm input, #filterForm select').each((i, element) => {
            const $el = $(element);
            const value = $el.val();
            if (value) {
                filters[$el.attr('id')] = value;
            }
        });
        return filters;
    }
    
    // Utility functions
    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }
    
    parseCurrency(value) {
        if (!value) return null;
        return parseFloat(value.replace(/[^\d,]/g, '').replace(',', '.'));
    }
    
    parseDate(dateString) {
        if (!dateString) return null;
        if (dateString.length === 8) {
            // Format: YYYYMMDD
            return new Date(
                dateString.substring(0, 4),
                dateString.substring(4, 6) - 1,
                dateString.substring(6, 8)
            );
        }
        return new Date(dateString);
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    showError(message) {
        $('#resultsTable').html(`
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i> ${message}
            </div>
        `);
    }
    
    showToast(message, type = 'info') {
        const toast = $(`
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `);
        
        $('#toastContainer').append(toast);
        const bsToast = new bootstrap.Toast(toast[0]);
        bsToast.show();
        
        // Remove from DOM after hiding
        toast.on('hidden.bs.toast', () => toast.remove());
    }
}

// Initialize when document is ready
$(document).ready(() => {
    if ($('#filterForm').length) {
        window.advancedFilters = new AdvancedFilters();
    }
});