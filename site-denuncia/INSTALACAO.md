# Guia de Instalação e Uso - Canal de Denúncia Grupo Destaque

## 🚀 Instalação Rápida

### Passo 1: Preparar o Ambiente
```bash
# Certifique-se de ter Python 3.7+ instalado
python --version

# Navegue até o diretório do projeto
cd site-denuncia
```

### Passo 2: Instalar Dependências
```bash
# Instale as dependências necessárias
pip install -r requirements.txt
```

### Passo 3: Executar o Sistema
```bash
# Execute a aplicação
python app.py
```

### Passo 4: Acessar o Site
- Abra seu navegador
- Acesse: `http://localhost:5000`
- O site estará funcionando!

## 📋 Verificação do Sistema

### Teste de Funcionamento
1. **Acesse a página principal**: `http://localhost:5000`
2. **Preencha o formulário**:
   - Selecione uma loja
   - Digite uma descrição com pelo menos 20 caracteres
   - Clique em "Enviar Denúncia"
3. **Verifique a confirmação**: Você deve ver uma página com número de protocolo
4. **Teste a política de privacidade**: Clique no link no rodapé

### Verificação da API
```bash
# Teste o status do sistema
curl http://localhost:5000/api/status

# Visualize estatísticas
curl http://localhost:5000/api/estatisticas
```

## 🔧 Configurações Avançadas

### Para Ambiente de Produção

1. **Configure um servidor web** (recomendado: Nginx + Gunicorn):
```bash
# Instale Gunicorn
pip install gunicorn

# Execute com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Configure HTTPS** (obrigatório para produção):
   - Obtenha certificado SSL
   - Configure proxy reverso no Nginx
   - Atualize URLs para HTTPS

3. **Banco de Dados para Produção**:
   - Considere migrar para PostgreSQL
   - Configure backups automáticos
   - Implemente rotação de logs

### Configurações de Segurança

1. **Variáveis de Ambiente**:
```bash
# Defina uma chave secreta forte
export SECRET_KEY="sua-chave-secreta-muito-forte-aqui"

# Configure modo de produção
export FLASK_ENV=production
```

2. **Firewall e Acesso**:
   - Configure firewall para permitir apenas portas necessárias
   - Restrinja acesso ao banco de dados
   - Configure logs de acesso

## 📊 Monitoramento e Manutenção

### Verificação de Logs
```bash
# Os logs são armazenados no banco de dados
# Acesse via API ou diretamente no SQLite

# Exemplo de consulta de logs
sqlite3 database/denuncias.db "SELECT * FROM logs ORDER BY data_acao DESC LIMIT 10;"
```

### Backup do Sistema
```bash
# Backup do banco de dados
cp database/denuncias.db backup/denuncias_$(date +%Y%m%d).db

# Backup completo do sistema
tar -czf backup_site_$(date +%Y%m%d).tar.gz site-denuncia/
```

### Estatísticas de Uso
- Acesse `http://localhost:5000/api/estatisticas` para ver:
  - Total de denúncias
  - Denúncias por status
  - Denúncias por período

## 🛠️ Personalização

### Modificar Lojas/Cidades
Edite o arquivo `templates/index.html` na seção do `<select>`:
```html
<optgroup label="NOVA_MARCA">
    <option value="NOVA_MARCA - CIDADE">NOVA_MARCA - CIDADE</option>
</optgroup>
```

### Alterar Cores e Design
Modifique o arquivo `static/css/style.css`:
- Paleta de cores nas variáveis CSS
- Layout e espaçamentos
- Animações e efeitos

### Personalizar Textos
- **Página principal**: `templates/index.html`
- **Confirmação**: `templates/confirmacao.html`
- **Privacidade**: `templates/privacidade.html`

## 🔍 Solução de Problemas

### Problemas Comuns

1. **Erro "Module not found"**:
```bash
# Reinstale as dependências
pip install -r requirements.txt
```

2. **Banco de dados não criado**:
```bash
# Verifique permissões do diretório
chmod 755 database/
```

3. **Site não carrega**:
```bash
# Verifique se a porta 5000 está livre
netstat -an | grep 5000

# Tente uma porta diferente
python app.py --port 8080
```

4. **Formulário não envia**:
   - Verifique console do navegador (F12)
   - Confirme que JavaScript está habilitado
   - Teste API diretamente: `curl -X POST http://localhost:5000/api/status`

### Logs de Debug
Para ativar logs detalhados, modifique `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📞 Suporte Técnico

### Informações do Sistema
- **Versão Python**: 3.7+
- **Framework**: Flask 2.3.3
- **Banco**: SQLite 3
- **Frontend**: HTML5, CSS3, JavaScript ES6

### Contato para Suporte
Em caso de problemas técnicos:
1. Verifique os logs do sistema
2. Consulte a documentação completa no README.md
3. Teste as APIs de status
4. Verifique configurações de rede e firewall

---

**Sistema desenvolvido e testado com sucesso! ✅**

