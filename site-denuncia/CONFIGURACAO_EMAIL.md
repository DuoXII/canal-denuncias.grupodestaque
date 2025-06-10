# Configuração de E-mail - Canal de Denúncia Grupo Destaque

## ⚠️ IMPORTANTE: Configuração de E-mail Necessária

Para que o sistema envie e-mails automaticamente para `Henrique.auditoria@grupodestaque.com.br`, você precisa configurar as credenciais de e-mail.

## 🔧 Configuração Rápida

### Opção 1: Variáveis de Ambiente (Recomendado)

Defina as seguintes variáveis de ambiente antes de executar o sistema:

```bash
# Para Gmail (recomendado)
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USERNAME="seu-email@gmail.com"
export MAIL_PASSWORD="sua-senha-de-app"
export MAIL_DEFAULT_SENDER="noreply@grupodestaque.com.br"

# Execute o sistema
python app.py
```

### Opção 2: Editar Diretamente no Código

Edite o arquivo `app.py` nas linhas 19-25:

```python
# Configurações de E-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Servidor SMTP
app.config['MAIL_PORT'] = 587                 # Porta SMTP
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'seu-email@gmail.com'        # SEU E-MAIL
app.config['MAIL_PASSWORD'] = 'sua-senha-de-app'           # SUA SENHA
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@grupodestaque.com.br'
```

## 📧 Configuração para Gmail

### 1. Ativar Verificação em 2 Etapas
- Acesse sua conta Google
- Vá em "Segurança" > "Verificação em duas etapas"
- Ative a verificação em 2 etapas

### 2. Gerar Senha de App
- Ainda em "Segurança", procure por "Senhas de app"
- Selecione "E-mail" e "Computador Windows/Mac/Linux"
- Copie a senha gerada (16 caracteres)
- Use esta senha no campo `MAIL_PASSWORD`

## 🏢 Configuração para E-mail Corporativo

Se você tem um servidor de e-mail corporativo:

```python
app.config['MAIL_SERVER'] = 'smtp.seudominio.com.br'
app.config['MAIL_PORT'] = 587  # ou 465 para SSL
app.config['MAIL_USERNAME'] = 'sistema@grupodestaque.com.br'
app.config['MAIL_PASSWORD'] = 'senha-do-sistema'
```

## 🧪 Teste de E-mail

Para testar se o e-mail está funcionando:

1. Configure as credenciais
2. Execute o sistema
3. Envie uma denúncia de teste
4. Verifique se o e-mail chegou em `Henrique.auditoria@grupodestaque.com.br`

## 📋 Conteúdo do E-mail

O e-mail enviado contém:
- **Assunto**: 🚨 Nova Denúncia Anônima - Protocolo [NÚMERO]
- **Dados da denúncia**: Loja, descrição, data/hora
- **Arquivos anexados**: Se houver uploads
- **Template HTML**: Formatação profissional
- **Informações de segurança**: Lembretes sobre anonimato

## 🔒 Segurança

- As credenciais de e-mail são mantidas seguras
- Não são registradas nos logs do sistema
- Use sempre senhas de aplicativo, nunca a senha principal
- Configure firewall para permitir conexões SMTP

## ❌ Solução de Problemas

### E-mail não está sendo enviado:

1. **Verifique as credenciais**:
   ```bash
   curl -X GET http://localhost:5000/api/status
   ```

2. **Verifique os logs**:
   - Logs são salvos no banco de dados
   - Procure por entradas com "ERRO_EMAIL"

3. **Teste conexão SMTP**:
   ```python
   # Teste rápido no Python
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('seu-email@gmail.com', 'sua-senha-de-app')
   print("Conexão OK!")
   ```

### Erros comuns:

- **"Authentication failed"**: Senha incorreta ou 2FA não configurado
- **"Connection refused"**: Firewall bloqueando porta 587
- **"SSL Error"**: Configuração TLS/SSL incorreta

## 📞 Suporte

Se precisar de ajuda com a configuração:
1. Verifique se as credenciais estão corretas
2. Teste com uma conta Gmail primeiro
3. Consulte a documentação do seu provedor de e-mail
4. Verifique logs do sistema para erros específicos

---

**⚡ Após configurar o e-mail, todas as denúncias serão automaticamente enviadas para Henrique.auditoria@grupodestaque.com.br**

