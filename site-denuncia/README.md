# Canal de Denúncia - Grupo Destaque

Um sistema web completo para denúncias anônimas, desenvolvido especificamente para o Grupo Destaque com base no formulário original fornecido.

## 🚀 Características Principais

- **Anonimato Garantido**: Sistema desenvolvido para manter completo anonimato dos denunciantes
- **Interface Moderna**: Design responsivo e profissional com gradientes e animações
- **Envio de E-mail**: Denúncias são automaticamente enviadas para Henrique.auditoria@grupodestaque.com.br
- **Upload de Arquivos**: Suporte para anexar fotos, PDFs, documentos e vídeos
- **Segurança**: Validações robustas, sanitização de dados e medidas de proteção
- **Banco de Dados**: Armazenamento seguro com SQLite e logs de auditoria
- **Responsivo**: Funciona perfeitamente em desktop e dispositivos móveis

## 📋 Funcionalidades

### Frontend
- Formulário de denúncia com validação em tempo real
- Seleção de loja/cidade organizada por marca
- Campo "Outro" para lojas não listadas
- Contador de caracteres no campo de descrição
- **NOVO**: Área de upload com drag & drop para arquivos
- **NOVO**: Suporte para múltiplos tipos de arquivo (fotos, PDFs, vídeos, documentos)
- **NOVO**: Validação de tipos e tamanhos de arquivo
- Página de confirmação com número de protocolo
- Página de política de privacidade completa
- Design responsivo para todos os dispositivos

### Backend
- API Flask para processamento de denúncias
- **NOVO**: Sistema de envio automático de e-mail
- **NOVO**: Processamento e armazenamento seguro de arquivos
- **NOVO**: Template HTML profissional para e-mails
- Geração automática de protocolos únicos
- Validação e sanitização de dados
- Sistema de logs para auditoria
- Endpoints de status e estatísticas
- Medidas de segurança e proteção de dados

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask (Python), Flask-Mail
- **Banco de Dados**: SQLite
- **Upload**: Werkzeug para processamento seguro de arquivos
- **E-mail**: SMTP com templates HTML
- **Estilo**: CSS Grid, Flexbox, Gradientes, Animações
- **Segurança**: CORS, Sanitização, Validação, HTTPS ready

## 📁 Estrutura do Projeto

```
site-denuncia/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Documentação do projeto
├── CONFIGURACAO_EMAIL.md # Guia de configuração de e-mail
├── static/
│   ├── css/
│   │   └── style.css     # Estilos CSS responsivos
│   ├── js/
│   │   └── script.js     # JavaScript para interatividade
│   └── images/           # Diretório para imagens
├── templates/
│   ├── index.html        # Página principal do formulário
│   ├── confirmacao.html  # Página de confirmação
│   ├── privacidade.html  # Política de privacidade
│   └── email_denuncia.html # Template de e-mail
├── uploads/              # Diretório para arquivos enviados
└── database/
    └── denuncias.db      # Banco de dados SQLite (criado automaticamente)
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação e Execução

1. **Instalar dependências:**
   ```bash
   cd site-denuncia
   pip install -r requirements.txt
   ```

2. **⚠️ IMPORTANTE - Configurar E-mail:**
   
   Consulte o arquivo `CONFIGURACAO_EMAIL.md` para configurar o envio automático de e-mails.
   
   Configuração rápida:
   ```bash
   export MAIL_USERNAME="seu-email@gmail.com"
   export MAIL_PASSWORD="sua-senha-de-app"
   ```

3. **Executar a aplicação:**
   ```bash
   python app.py
   ```

4. **Acessar o site:**
   - Abra o navegador e acesse: `http://localhost:5000`

### Configuração para Produção

Para usar em produção, considere:

1. **Configurar HTTPS**: O site está preparado para HTTPS
2. **Configurar E-mail**: Essencial para funcionamento completo
3. **Banco de Dados**: Considere migrar para PostgreSQL ou MySQL para maior robustez
4. **Servidor Web**: Use Gunicorn + Nginx para melhor performance
5. **Monitoramento**: Implemente logs mais detalhados e monitoramento
6. **Backup**: Configure backup automático dos arquivos enviados

## 📊 Funcionalidades do Sistema

### Formulário de Denúncia
- **Seleção de Loja**: Dropdown organizado por marca com 33 opções
- **Campo Outro**: Permite especificar lojas não listadas
- **Descrição**: Campo de texto com validação mínima de 20 caracteres
- **Upload de Arquivos**: Até 5 arquivos, 10MB cada
- **Tipos Suportados**: JPG, PNG, PDF, DOC, DOCX, MP4, AVI, MOV, WMV
- **Validação**: Validação em tempo real e no servidor
- **Protocolo**: Geração automática de número único para acompanhamento

### Sistema de E-mail
- **Envio Automático**: Para Henrique.auditoria@grupodestaque.com.br
- **Template Profissional**: E-mail HTML formatado
- **Anexos**: Arquivos enviados são anexados automaticamente
- **Informações Completas**: Protocolo, loja, descrição, data/hora
- **Segurança**: Lembretes sobre anonimato e confidencialidade

### Upload de Arquivos
- **Drag & Drop**: Interface intuitiva para arrastar arquivos
- **Múltiplos Arquivos**: Até 5 arquivos por denúncia
- **Validação Rigorosa**: Tipos MIME, extensões e tamanhos
- **Armazenamento Seguro**: Nomes únicos e organização por protocolo
- **Integração**: Arquivos anexados automaticamente aos e-mails

### Segurança e Privacidade
- **Anonimato**: Nenhum dado pessoal é coletado
- **Sanitização**: Todos os dados são sanitizados antes do armazenamento
- **Validação de Arquivos**: Verificação rigorosa de tipos e conteúdo
- **Logs**: Sistema de auditoria sem dados identificáveis
- **Criptografia**: Preparado para conexões HTTPS

### Páginas do Sistema
1. **Página Principal** (`/`): Formulário de denúncia com upload
2. **Confirmação** (`/confirmacao`): Exibe protocolo e próximos passos
3. **Privacidade** (`/privacidade`): Política de privacidade detalhada

### APIs Disponíveis
- `POST /enviar-denuncia`: Processa nova denúncia com arquivos
- `GET /api/status`: Status do sistema e banco de dados
- `GET /api/estatisticas`: Estatísticas básicas (sem dados sensíveis)

## 🎨 Design e UX

### Paleta de Cores
- **Azul Escuro** (#1a365d): Confiança e seriedade
- **Azul Claro** (#3182ce): Elementos interativos
- **Verde** (#38a169): Confirmações e sucesso
- **Gradiente**: Fundo com gradiente roxo/azul moderno

### Características Visuais
- Cards com backdrop-filter e transparência
- Animações suaves e micro-interações
- Área de upload com drag & drop visual
- Ícones Font Awesome para melhor UX
- Typography moderna com fonte Inter
- Responsividade completa para mobile

## 📱 Responsividade

O site foi desenvolvido com abordagem mobile-first:
- **Desktop**: Layout em grid com cards lado a lado
- **Tablet**: Adaptação automática dos elementos
- **Mobile**: Layout em coluna única, botões full-width
- **Upload**: Interface touch-friendly para dispositivos móveis

## 🔒 Conformidade e Segurança

### LGPD (Lei Geral de Proteção de Dados)
- Política de privacidade completa e transparente
- Minimização de dados coletados
- Anonimização garantida
- Base legal clara para processamento

### Medidas de Segurança
- Validação rigorosa de entrada
- Sanitização de dados e nomes de arquivo
- Proteção contra XSS e injection
- Validação de tipos MIME para uploads
- Logs de auditoria
- Controle de acesso

## 📈 Monitoramento

### Logs Disponíveis
- Criação de denúncias
- Upload de arquivos
- Envio de e-mails
- Erros de validação
- Erros de sistema
- Inicialização do sistema

### Estatísticas
- Total de denúncias
- Denúncias por status
- Denúncias por período
- Arquivos processados
- Status do sistema

## 🔧 Manutenção

### Backup
- Banco de dados SQLite pode ser facilmente copiado
- Diretório `uploads/` contém todos os arquivos enviados
- Recomenda-se backup diário de ambos

### Atualizações
- Sistema modular permite atualizações fáceis
- Logs ajudam no diagnóstico de problemas
- Estrutura preparada para escalabilidade

### Limpeza
- Arquivos antigos podem ser removidos periodicamente
- Logs podem ser arquivados após período determinado
- Considere rotação de logs para performance

## 📞 Suporte

Para dúvidas sobre o sistema:
- Consulte `CONFIGURACAO_EMAIL.md` para configuração de e-mail
- Consulte os logs em caso de erros
- Verifique o status via `/api/status`
- Analise as estatísticas via `/api/estatisticas`

## 📄 Licença

Este projeto foi desenvolvido especificamente para o Grupo Destaque. Todos os direitos reservados.

---

**Desenvolvido com ❤️ para promover um ambiente de trabalho ético e transparente no Grupo Destaque.**

## 🆕 Novidades da Versão Atual

### ✅ Implementado
- ✅ Envio automático de e-mail para Henrique.auditoria@grupodestaque.com.br
- ✅ Upload de múltiplos arquivos (fotos, PDFs, documentos, vídeos)
- ✅ Interface drag & drop para upload
- ✅ Validação rigorosa de arquivos
- ✅ Template HTML profissional para e-mails
- ✅ Anexação automática de arquivos aos e-mails
- ✅ Logs detalhados de todas as operações
- ✅ Armazenamento seguro de arquivos

### 🔧 Configuração Necessária
- ⚠️ **E-mail**: Configure credenciais SMTP (ver CONFIGURACAO_EMAIL.md)
- ⚠️ **Permissões**: Verifique permissões do diretório uploads/
- ⚠️ **Firewall**: Libere porta 587 para SMTP (se necessário)

