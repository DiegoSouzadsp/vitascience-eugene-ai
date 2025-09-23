/* Enhanced JavaScript for Eugene Schwartz VSL Analyzer */

// Global application state
window.EugeneAnalyzer = {
    config: {
        minTextLength: 100,
        maxTextLength: 50000,
        debounceDelay: 300,
        animationDuration: 300
    },
    state: {
        isAnalyzing: false,
        lastAnalysis: null,
        currentPage: 'index'
    },
    utils: {},
    ui: {},
    api: {}
};

// Utility functions
EugeneAnalyzer.utils = {
    // Debounce function for input handling
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Format numbers with thousands separator
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },

    // Calculate reading time
    calculateReadingTime: function(text) {
        const wordsPerMinute = 200;
        const words = text.trim().split(/\s+/).length;
        const minutes = Math.ceil(words / wordsPerMinute);
        return minutes;
    },

    // Generate unique ID
    generateId: function() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    // Copy text to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    }
};

// UI enhancement functions
EugeneAnalyzer.ui = {
    // Initialize page animations
    initAnimations: function() {
        // Add fade-in animation to main content
        const mainContent = document.querySelector('.main-container');
        if (mainContent) {
            mainContent.classList.add('fade-in');
        }

        // Stagger animation for analysis sections
        const sections = document.querySelectorAll('.analysis-section');
        sections.forEach((section, index) => {
            setTimeout(() => {
                section.style.opacity = '0';
                section.style.transform = 'translateY(20px)';
                section.style.transition = 'all 0.6s ease';

                setTimeout(() => {
                    section.style.opacity = '1';
                    section.style.transform = 'translateY(0)';
                }, 100);
            }, index * 200);
        });
    },

    // Enhanced loading overlay
    showLoadingOverlay: function(message = 'Processando...', submessage = '') {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.id = 'loadingOverlay';

        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner-enhanced"></div>
                <h4 class="mb-2">${message}</h4>
                ${submessage ? `<p class="text-muted">${submessage}</p>` : ''}
                <div class="progress mt-3" style="width: 300px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated"
                         role="progressbar" style="width: 100%">
                        Analisando...
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Add animation
        setTimeout(() => {
            overlay.style.opacity = '1';
        }, 10);
    },

    // Hide loading overlay
    hideLoadingOverlay: function() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    },

    // Show toast notification
    showToast: function(message, type = 'info', duration = 5000) {
        const toastContainer = document.getElementById('toastContainer') || this.createToastContainer();

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${this.getToastIcon(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto"
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toastContainer.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast, { delay: duration });
        bsToast.show();

        // Remove toast element after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },

    // Create toast container if it doesn't exist
    createToastContainer: function() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    },

    // Get appropriate icon for toast type
    getToastIcon: function(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle',
            'primary': 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    // Update character and word counts with enhanced visualization
    updateTextStats: function(textarea) {
        const text = textarea.value;
        const chars = text.length;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const readingTime = EugeneAnalyzer.utils.calculateReadingTime(text);

        // Update displays
        const charCount = document.getElementById('charCount');
        const wordCount = document.getElementById('wordCount');

        if (charCount) {
            charCount.textContent = EugeneAnalyzer.utils.formatNumber(chars);
            charCount.className = chars >= EugeneAnalyzer.config.minTextLength ? 'text-success' : 'text-warning';
        }

        if (wordCount) {
            wordCount.textContent = EugeneAnalyzer.utils.formatNumber(words);
        }

        // Add reading time if element exists
        const readingTimeEl = document.getElementById('readingTime');
        if (readingTimeEl) {
            readingTimeEl.textContent = `${readingTime} min`;
        }

        return { chars, words, readingTime };
    },

    // Enhanced form validation
    validateForm: function(form) {
        const vslText = form.querySelector('#vsl_text');
        const text = vslText.value.trim();

        // Clear previous validation states
        vslText.classList.remove('is-invalid', 'is-valid');

        if (text.length < EugeneAnalyzer.config.minTextLength) {
            vslText.classList.add('is-invalid');
            this.showToast(
                `Texto muito curto. Mínimo: ${EugeneAnalyzer.config.minTextLength} caracteres`,
                'warning'
            );
            return false;
        }

        if (text.length > EugeneAnalyzer.config.maxTextLength) {
            vslText.classList.add('is-invalid');
            this.showToast(
                `Texto muito longo. Máximo: ${EugeneAnalyzer.config.maxTextLength} caracteres`,
                'warning'
            );
            return false;
        }

        vslText.classList.add('is-valid');
        return true;
    }
};

// API functions
EugeneAnalyzer.api = {
    // Check system health
    checkHealth: async function() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error', error: error.message };
        }
    },

    // Submit VSL for analysis
    analyzeVSL: async function(vslText, analysisType = 'complete') {
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    vsl_text: vslText,
                    analysis_type: analysisType,
                    timestamp: new Date().toISOString(),
                    client: 'frontend-enhanced'
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erro na análise');
            }

            return data;
        } catch (error) {
            console.error('Analysis failed:', error);
            throw error;
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Eugene Analyzer Enhanced JS loaded');

    // Initialize animations
    EugeneAnalyzer.ui.initAnimations();

    // Check system health on page load
    EugeneAnalyzer.api.checkHealth().then(health => {
        const statusIndicator = document.getElementById('systemStatus');
        if (statusIndicator) {
            const statusClass = health.status === 'healthy' ? 'status-healthy' : 'status-error';
            statusIndicator.className = `status-indicator ${statusClass}`;
            statusIndicator.setAttribute('data-tooltip',
                `Sistema: ${health.status} | N8N: ${health.n8n_status || 'unknown'}`
            );
        }
    });

    // Enhanced textarea handling
    const vslTextarea = document.getElementById('vsl_text');
    if (vslTextarea) {
        const debouncedUpdate = EugeneAnalyzer.utils.debounce(
            () => EugeneAnalyzer.ui.updateTextStats(vslTextarea),
            EugeneAnalyzer.config.debounceDelay
        );

        vslTextarea.addEventListener('input', debouncedUpdate);
        vslTextarea.addEventListener('paste', () => {
            setTimeout(debouncedUpdate, 100);
        });

        // Initial update
        EugeneAnalyzer.ui.updateTextStats(vslTextarea);
    }

    // Enhanced form submission
    const analysisForm = document.getElementById('vslForm') || document.getElementById('demoForm');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Validate form
            if (!EugeneAnalyzer.ui.validateForm(this)) {
                return false;
            }

            // Check if already analyzing
            if (EugeneAnalyzer.state.isAnalyzing) {
                EugeneAnalyzer.ui.showToast('Análise já em progresso', 'warning');
                return false;
            }

            // Set analyzing state
            EugeneAnalyzer.state.isAnalyzing = true;

            // Show loading with enhanced messaging
            const vslText = this.querySelector('#vsl_text').value;
            const analysisType = this.querySelector('[name="analysis_type"]').value;

            EugeneAnalyzer.ui.showLoadingOverlay(
                'Analisando seu VSL...',
                'Aplicando metodologia Eugene Schwartz'
            );

            // Update button state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnContent = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<div class="spinner-border spinner-border-sm me-2"></div>Analisando...';

            // Use API for analysis (if available) or fall back to form submission
            if (window.location.pathname === '/demo' || analysisType === 'api') {
                EugeneAnalyzer.api.analyzeVSL(vslText, analysisType)
                    .then(result => {
                        EugeneAnalyzer.state.lastAnalysis = result;
                        EugeneAnalyzer.ui.hideLoadingOverlay();
                        EugeneAnalyzer.ui.showToast('Análise concluída com sucesso!', 'success');

                        // Redirect to results or update page content
                        window.location.href = '/analyze';
                    })
                    .catch(error => {
                        EugeneAnalyzer.ui.hideLoadingOverlay();
                        EugeneAnalyzer.ui.showToast(
                            `Erro na análise: ${error.message}`,
                            'danger'
                        );

                        // Reset button
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalBtnContent;
                        EugeneAnalyzer.state.isAnalyzing = false;
                    });
            } else {
                // Submit form normally
                this.submit();
            }
        });
    }

    // Add copy-to-clipboard functionality for analysis results
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const targetSelector = this.getAttribute('data-copy');
            const targetElement = document.querySelector(targetSelector);

            if (targetElement) {
                const textToCopy = targetElement.textContent || targetElement.value;

                EugeneAnalyzer.utils.copyToClipboard(textToCopy)
                    .then(() => {
                        EugeneAnalyzer.ui.showToast('Copiado para a área de transferência!', 'success');

                        // Update button temporarily
                        const originalText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-check me-2"></i>Copiado!';
                        setTimeout(() => {
                            this.innerHTML = originalText;
                        }, 2000);
                    })
                    .catch(() => {
                        EugeneAnalyzer.ui.showToast('Erro ao copiar texto', 'danger');
                    });
            }
        });
    });

    // Enhanced keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.querySelector('form');
            if (activeForm) {
                activeForm.dispatchEvent(new Event('submit', { bubbles: true }));
            }
        }

        // Escape to close modals/overlays
        if (e.key === 'Escape') {
            EugeneAnalyzer.ui.hideLoadingOverlay();
        }
    });

    // Progressive enhancement for browsers with JavaScript disabled
    document.documentElement.classList.add('js-enabled');
});

// Export for global access
window.EugeneAnalyzer = EugeneAnalyzer;