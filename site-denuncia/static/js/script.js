// Aguarda o carregamento completo da página
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do formulário
    const form = document.getElementById('denunciaForm');
    const lojaSelect = document.getElementById('loja');
    const outroLojaGroup = document.getElementById('outroLojaGroup');
    const outroLojaInput = document.getElementById('outroLoja');
    const suspeitaTextarea = document.getElementById('suspeita');
    const charCount = document.getElementById('charCount');
    const submitBtn = document.getElementById('submitBtn');
    
    // Elementos de upload
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('arquivos');
    const fileList = document.getElementById('fileList');
    
    // Array para armazenar arquivos selecionados
    let selectedFiles = [];
    
    // Configurações de upload
    const MAX_FILES = 5;
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const ALLOWED_TYPES = {
        'image/jpeg': { icon: 'fas fa-image', class: 'image' },
        'image/jpg': { icon: 'fas fa-image', class: 'image' },
        'image/png': { icon: 'fas fa-image', class: 'image' },
        'application/pdf': { icon: 'fas fa-file-pdf', class: 'pdf' },
        'application/msword': { icon: 'fas fa-file-word', class: 'document' },
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': { icon: 'fas fa-file-word', class: 'document' },
        'video/mp4': { icon: 'fas fa-file-video', class: 'video' },
        'video/avi': { icon: 'fas fa-file-video', class: 'video' },
        'video/quicktime': { icon: 'fas fa-file-video', class: 'video' },
        'video/x-ms-wmv': { icon: 'fas fa-file-video', class: 'video' }
    };

    // Funções de upload de arquivos
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function getFileIcon(type) {
        return ALLOWED_TYPES[type] || { icon: 'fas fa-file', class: 'document' };
    }

    function validateFile(file) {
        const errors = [];
        
        // Verifica tipo de arquivo
        if (!ALLOWED_TYPES[file.type]) {
            errors.push('Tipo de arquivo não suportado');
        }
        
        // Verifica tamanho
        if (file.size > MAX_FILE_SIZE) {
            errors.push(`Arquivo muito grande (máximo ${formatFileSize(MAX_FILE_SIZE)})`);
        }
        
        return errors;
    }

    function addFileToList(file) {
        const fileId = 'file_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        const fileInfo = getFileIcon(file.type);
        
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.dataset.fileId = fileId;
        
        fileItem.innerHTML = `
            <div class="file-info">
                <i class="${fileInfo.icon} file-icon ${fileInfo.class}"></i>
                <div class="file-details">
                    <h4>${file.name}</h4>
                    <p>${formatFileSize(file.size)}</p>
                </div>
            </div>
            <div class="file-actions">
                <button type="button" class="btn-remove" onclick="removeFile('${fileId}')">
                    <i class="fas fa-times"></i> Remover
                </button>
            </div>
        `;
        
        fileList.appendChild(fileItem);
        
        // Adiciona arquivo ao array
        selectedFiles.push({
            id: fileId,
            file: file,
            element: fileItem
        });
    }

    function removeFile(fileId) {
        // Remove do array
        selectedFiles = selectedFiles.filter(item => item.id !== fileId);
        
        // Remove do DOM
        const fileItem = document.querySelector(`[data-file-id="${fileId}"]`);
        if (fileItem) {
            fileItem.remove();
        }
        
        // Atualiza input de arquivo
        updateFileInput();
    }

    function updateFileInput() {
        // Cria novo DataTransfer para atualizar o input
        const dt = new DataTransfer();
        selectedFiles.forEach(item => {
            dt.items.add(item.file);
        });
        fileInput.files = dt.files;
    }

    function handleFiles(files) {
        const fileArray = Array.from(files);
        
        // Verifica limite de arquivos
        if (selectedFiles.length + fileArray.length > MAX_FILES) {
            showFormError(`Máximo de ${MAX_FILES} arquivos permitidos`);
            return;
        }
        
        fileArray.forEach(file => {
            const errors = validateFile(file);
            
            if (errors.length > 0) {
                showFormError(`${file.name}: ${errors.join(', ')}`);
                return;
            }
            
            // Verifica se arquivo já foi adicionado
            const exists = selectedFiles.some(item => 
                item.file.name === file.name && 
                item.file.size === file.size
            );
            
            if (exists) {
                showFormError(`Arquivo "${file.name}" já foi adicionado`);
                return;
            }
            
            addFileToList(file);
        });
        
        updateFileInput();
    }

    // Event listeners para upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    // Torna a função removeFile global
    window.removeFile = removeFile;

    // Configuração do campo "Outro"
    lojaSelect.addEventListener('change', function() {
        if (this.value === 'outro') {
            outroLojaGroup.style.display = 'block';
            outroLojaInput.required = true;
            outroLojaInput.focus();
        } else {
            outroLojaGroup.style.display = 'none';
            outroLojaInput.required = false;
            outroLojaInput.value = '';
            removeError(outroLojaInput);
        }
    });

    // Contador de caracteres
    suspeitaTextarea.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count;
        
        // Mudança de cor baseada no comprimento
        if (count < 50) {
            charCount.style.color = '#e53e3e';
        } else if (count < 100) {
            charCount.style.color = '#dd6b20';
        } else {
            charCount.style.color = '#38a169';
        }
    });

    // Validação em tempo real
    const inputs = [lojaSelect, outroLojaInput, suspeitaTextarea];
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });

    // Submissão do formulário
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            submitForm();
        }
    });

    // Função de validação de campo individual
    function validateField(field) {
        const fieldGroup = field.closest('.form-group');
        let isValid = true;
        let errorMessage = '';

        // Remove erros anteriores
        removeError(field);

        // Validação específica por campo
        switch(field.id) {
            case 'loja':
                if (!field.value) {
                    isValid = false;
                    errorMessage = 'Por favor, selecione uma loja.';
                }
                break;
                
            case 'outroLoja':
                if (lojaSelect.value === 'outro' && !field.value.trim()) {
                    isValid = false;
                    errorMessage = 'Por favor, especifique a loja.';
                } else if (field.value.trim() && field.value.trim().length < 3) {
                    isValid = false;
                    errorMessage = 'O nome da loja deve ter pelo menos 3 caracteres.';
                }
                break;
                
            case 'suspeita':
                if (!field.value.trim()) {
                    isValid = false;
                    errorMessage = 'Por favor, descreva sua suspeita.';
                } else if (field.value.trim().length < 20) {
                    isValid = false;
                    errorMessage = 'A descrição deve ter pelo menos 20 caracteres.';
                }
                break;
        }

        if (!isValid) {
            showError(field, errorMessage);
        }

        return isValid;
    }

    // Função de validação completa do formulário
    function validateForm() {
        let isValid = true;
        
        // Valida todos os campos obrigatórios
        if (!validateField(lojaSelect)) isValid = false;
        if (lojaSelect.value === 'outro' && !validateField(outroLojaInput)) isValid = false;
        if (!validateField(suspeitaTextarea)) isValid = false;

        return isValid;
    }

    // Função para mostrar erro
    function showError(field, message) {
        const fieldGroup = field.closest('.form-group');
        fieldGroup.classList.add('error');
        
        // Remove mensagem de erro anterior
        const existingError = fieldGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Adiciona nova mensagem de erro
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
        
        field.parentNode.appendChild(errorDiv);
    }

    // Função para remover erro
    function removeError(field) {
        const fieldGroup = field.closest('.form-group');
        fieldGroup.classList.remove('error');
        
        const errorMessage = fieldGroup.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    // Função para submeter o formulário
    async function submitForm() {
        // Desabilita o botão de envio
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
        submitBtn.classList.add('loading');

        try {
            // Prepara os dados do formulário
            const formData = new FormData();
            formData.append('loja', lojaSelect.value === 'outro' ? outroLojaInput.value : lojaSelect.value);
            formData.append('suspeita', suspeitaTextarea.value);
            
            // Adiciona arquivos se houver
            selectedFiles.forEach((item, index) => {
                formData.append('arquivos', item.file);
            });

            // Envia os dados
            const response = await fetch('/enviar-denuncia', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                
                if (result.success) {
                    // Redireciona para página de confirmação
                    window.location.href = `/confirmacao?protocolo=${result.protocolo}`;
                } else {
                    throw new Error(result.message || 'Erro ao enviar denúncia');
                }
            } else {
                throw new Error('Erro de conexão com o servidor');
            }
        } catch (error) {
            console.error('Erro:', error);
            showFormError('Erro ao enviar denúncia. Tente novamente em alguns instantes.');
        } finally {
            // Reabilita o botão
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar Denúncia';
            submitBtn.classList.remove('loading');
        }
    }

    // Função para mostrar erro geral do formulário
    function showFormError(message) {
        // Remove erro anterior
        const existingError = form.querySelector('.form-error');
        if (existingError) {
            existingError.remove();
        }

        // Cria novo erro
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error error-message';
        errorDiv.style.textAlign = 'center';
        errorDiv.style.marginBottom = '20px';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
        
        form.insertBefore(errorDiv, form.firstChild);
        
        // Remove o erro após 5 segundos
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    // Função para mostrar sucesso
    function showFormSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'form-success success-message';
        successDiv.style.textAlign = 'center';
        successDiv.style.marginBottom = '20px';
        successDiv.style.padding = '15px';
        successDiv.style.backgroundColor = '#f0fff4';
        successDiv.style.border = '1px solid #9ae6b4';
        successDiv.style.borderRadius = '8px';
        successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
        
        form.insertBefore(successDiv, form.firstChild);
    }

    // Animações de entrada
    function animateElements() {
        const elements = document.querySelectorAll('.form-card, .info-card');
        
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.6s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // Inicia animações
    animateElements();

    // Adiciona efeitos de hover nos cards
    const infoCards = document.querySelectorAll('.info-card');
    infoCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Adiciona feedback visual ao focar nos campos
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentNode.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentNode.style.transform = 'scale(1)';
        });
    });
});

