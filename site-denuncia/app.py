from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from flask_mail import Mail, Message
import sqlite3
import hashlib
import secrets
import datetime
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Permite requisições cross-origin

# Configurações
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Configurações de E-mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@grupodestaque.com.br')

# E-mail de destino para denúncias
DESTINATARIO_DENUNCIA = 'Henrique.auditoria@grupodestaque.com.br'

# Inicializa Flask-Mail
mail = Mail(app)

# Configurações de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB máximo total

# Tipos de arquivo permitidos
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif',  # Imagens
    'pdf',  # PDFs
    'doc', 'docx',  # Documentos Word
    'mp4', 'avi', 'mov', 'wmv'  # Vídeos
}

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'denuncias.db')

def init_database():
    """Inicializa o banco de dados com as tabelas necessárias"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Tabela de denúncias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            protocolo TEXT UNIQUE NOT NULL,
            loja TEXT NOT NULL,
            suspeita TEXT NOT NULL,
            data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pendente',
            hash_verificacao TEXT NOT NULL
        )
    ''')
    
    # Tabela de arquivos anexados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arquivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            protocolo TEXT NOT NULL,
            nome_original TEXT NOT NULL,
            nome_arquivo TEXT NOT NULL,
            tipo_mime TEXT NOT NULL,
            tamanho INTEGER NOT NULL,
            caminho TEXT NOT NULL,
            data_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (protocolo) REFERENCES denuncias (protocolo)
        )
    ''')
    
    # Tabela de logs (para auditoria)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acao TEXT NOT NULL,
            protocolo TEXT,
            data_acao DATETIME DEFAULT CURRENT_TIMESTAMP,
            detalhes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def gerar_protocolo():
    """Gera um número de protocolo único"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = secrets.token_hex(3).upper()
    return f"GD{timestamp}{random_part}"

def gerar_hash_verificacao(protocolo, loja, suspeita):
    """Gera um hash para verificação de integridade"""
    data = f"{protocolo}{loja}{suspeita}{datetime.datetime.now().isoformat()}"
    return hashlib.sha256(data.encode()).hexdigest()

def validar_dados(loja, suspeita):
    """Valida os dados recebidos do formulário"""
    erros = []
    
    # Validação da loja
    if not loja or len(loja.strip()) < 3:
        erros.append("Loja deve ser especificada")
    
    # Validação da suspeita
    if not suspeita or len(suspeita.strip()) < 20:
        erros.append("Descrição da suspeita deve ter pelo menos 20 caracteres")
    
    # Validação de conteúdo suspeito (básica)
    if suspeita and len(suspeita) > 5000:
        erros.append("Descrição muito longa (máximo 5000 caracteres)")
    
    return erros

def sanitizar_texto(texto):
    """Remove caracteres potencialmente perigosos do texto"""
    if not texto:
        return ""
    
    # Remove tags HTML básicas
    texto = re.sub(r'<[^>]+>', '', texto)
    
    # Remove caracteres de controle
    texto = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', texto)
    
    return texto.strip()

def registrar_log(acao, protocolo=None, detalhes=None):
    """Registra ações no log para auditoria"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO logs (acao, protocolo, detalhes)
            VALUES (?, ?, ?)
        ''', (acao, protocolo, detalhes))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao registrar log: {e}")

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Retorna o tipo de arquivo baseado na extensão"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if ext in ['jpg', 'jpeg', 'png', 'gif']:
        return 'image'
    elif ext == 'pdf':
        return 'pdf'
    elif ext in ['doc', 'docx']:
        return 'document'
    elif ext in ['mp4', 'avi', 'mov', 'wmv']:
        return 'video'
    else:
        return 'unknown'

def processar_arquivos(files, protocolo):
    """Processa e salva os arquivos enviados"""
    arquivos_salvos = []
    
    try:
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                # Gera nome único para o arquivo
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                nome_unico = f"{protocolo}_{timestamp}_{filename}"
                
                # Caminho completo do arquivo
                filepath = os.path.join(UPLOAD_FOLDER, nome_unico)
                
                # Salva o arquivo
                file.save(filepath)
                
                # Informações do arquivo
                file_info = {
                    'nome_original': filename,
                    'nome_arquivo': nome_unico,
                    'tipo_mime': file.content_type or 'application/octet-stream',
                    'tamanho': os.path.getsize(filepath),
                    'caminho': filepath,
                    'tipo': get_file_type(filename)
                }
                
                # Salva informações no banco
                conn = sqlite3.connect(DATABASE_PATH)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO arquivos (protocolo, nome_original, nome_arquivo, 
                                        tipo_mime, tamanho, caminho)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (protocolo, file_info['nome_original'], file_info['nome_arquivo'],
                      file_info['tipo_mime'], file_info['tamanho'], file_info['caminho']))
                
                conn.commit()
                conn.close()
                
                arquivos_salvos.append(file_info)
                
                registrar_log("ARQUIVO_SALVO", protocolo, 
                            f"Arquivo: {filename} ({file_info['tamanho']} bytes)")
        
        return arquivos_salvos
        
    except Exception as e:
        registrar_log("ERRO_ARQUIVO", protocolo, f"Erro ao processar arquivos: {str(e)}")
        print(f"Erro ao processar arquivos: {e}")
        return []

def enviar_email_denuncia(protocolo, loja, suspeita, anexos=None):
    """Envia e-mail com os dados da denúncia para o responsável"""
    try:
        # Formata a data atual
        data_envio = datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')
        
        # Cria o assunto do e-mail
        assunto = f"🚨 Nova Denúncia Anônima - Protocolo {protocolo}"
        
        # Renderiza o template HTML
        html_body = render_template('email_denuncia.html',
                                  protocolo=protocolo,
                                  loja=loja,
                                  suspeita=suspeita,
                                  data_envio=data_envio,
                                  anexos=anexos or [])
        
        # Cria versão texto simples
        texto_body = f"""
NOVA DENÚNCIA ANÔNIMA - GRUPO DESTAQUE

Protocolo: {protocolo}
Data/Hora: {data_envio}
Loja/Unidade: {loja}

Descrição da Denúncia:
{suspeita}

{'Arquivos anexados: ' + str(len(anexos)) + ' arquivo(s)' if anexos else 'Nenhum arquivo anexado'}

IMPORTANTE: Esta denúncia é completamente anônima e confidencial.

---
Sistema de Denúncias - Grupo Destaque
        """
        
        # Cria a mensagem
        msg = Message(
            subject=assunto,
            recipients=[DESTINATARIO_DENUNCIA],
            body=texto_body,
            html=html_body
        )
        
        # Anexa arquivos se houver
        if anexos:
            for anexo in anexos:
                if os.path.exists(anexo['caminho']):
                    with open(anexo['caminho'], 'rb') as f:
                        msg.attach(
                            filename=anexo['nome'],
                            content_type=anexo['tipo'],
                            data=f.read()
                        )
        
        # Envia o e-mail
        mail.send(msg)
        
        registrar_log("EMAIL_ENVIADO", protocolo, f"E-mail enviado para {DESTINATARIO_DENUNCIA}")
        return True
        
    except Exception as e:
        registrar_log("ERRO_EMAIL", protocolo, f"Erro ao enviar e-mail: {str(e)}")
        print(f"Erro ao enviar e-mail: {e}")
        return False

@app.route('/')
def index():
    """Página principal com formulário de denúncia"""
    return render_template('index.html')

@app.route('/privacidade')
def privacidade():
    """Página de política de privacidade"""
    return render_template('privacidade.html')

@app.route('/confirmacao')
def confirmacao():
    """Página de confirmação de denúncia enviada"""
    protocolo = request.args.get('protocolo')
    if not protocolo:
        return redirect(url_for('index'))
    
    return render_template('confirmacao.html', protocolo=protocolo)

@app.route('/enviar-denuncia', methods=['POST'])
def enviar_denuncia():
    """Processa o envio de uma nova denúncia"""
    try:
        # Obtém dados do formulário
        loja = request.form.get('loja', '').strip()
        outro_loja = request.form.get('outroLoja', '').strip()
        suspeita = request.form.get('suspeita', '').strip()
        
        # Se "outro" foi selecionado, usa o campo de texto
        if loja == 'outro' and outro_loja:
            loja = f"OUTRO: {outro_loja}"
        
        # Sanitiza os dados
        loja = sanitizar_texto(loja)
        suspeita = sanitizar_texto(suspeita)
        
        # Valida os dados
        erros = validar_dados(loja, suspeita)
        if erros:
            registrar_log("ERRO_VALIDACAO", detalhes="; ".join(erros))
            return jsonify({
                'success': False,
                'message': 'Dados inválidos: ' + '; '.join(erros)
            }), 400
        
        # Gera protocolo e hash
        protocolo = gerar_protocolo()
        hash_verificacao = gerar_hash_verificacao(protocolo, loja, suspeita)
        
        # Processa arquivos enviados
        files = request.files.getlist('arquivos')
        arquivos_salvos = processar_arquivos(files, protocolo)
        
        # Salva no banco de dados
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO denuncias (protocolo, loja, suspeita, hash_verificacao)
            VALUES (?, ?, ?, ?)
        ''', (protocolo, loja, suspeita, hash_verificacao))
        
        conn.commit()
        conn.close()
        
        # Registra no log
        registrar_log("DENUNCIA_CRIADA", protocolo, f"Loja: {loja[:50]}... | Arquivos: {len(arquivos_salvos)}")
        
        # Prepara informações dos anexos para o e-mail
        anexos_email = []
        for arquivo in arquivos_salvos:
            anexos_email.append({
                'nome': arquivo['nome_original'],
                'tamanho': f"{arquivo['tamanho'] / 1024:.1f} KB" if arquivo['tamanho'] < 1024*1024 else f"{arquivo['tamanho'] / (1024*1024):.1f} MB",
                'tipo': arquivo['tipo_mime'],
                'caminho': arquivo['caminho']
            })
        
        # Envia e-mail com a denúncia
        email_enviado = enviar_email_denuncia(protocolo, loja, suspeita, anexos_email)
        
        if not email_enviado:
            # Log do erro, mas não falha a operação
            registrar_log("AVISO_EMAIL", protocolo, "Denúncia salva mas e-mail não foi enviado")
        
        return jsonify({
            'success': True,
            'protocolo': protocolo,
            'message': 'Denúncia enviada com sucesso',
            'email_enviado': email_enviado,
            'arquivos_processados': len(arquivos_salvos)
        })
        
    except Exception as e:
        registrar_log("ERRO_SISTEMA", detalhes=str(e))
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor. Tente novamente.'
        }), 500

@app.route('/api/status')
def api_status():
    """Endpoint para verificar status da API"""
    try:
        # Testa conexão com banco
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM denuncias')
        total_denuncias = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'online',
            'database': 'connected',
            'total_denuncias': total_denuncias,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/estatisticas')
def api_estatisticas():
    """Endpoint para estatísticas básicas (sem dados sensíveis)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total de denúncias
        cursor.execute('SELECT COUNT(*) FROM denuncias')
        total = cursor.fetchone()[0]
        
        # Denúncias por status
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM denuncias 
            GROUP BY status
        ''')
        por_status = dict(cursor.fetchall())
        
        # Denúncias por mês (últimos 12 meses)
        cursor.execute('''
            SELECT strftime('%Y-%m', data_envio) as mes, COUNT(*) 
            FROM denuncias 
            WHERE data_envio >= date('now', '-12 months')
            GROUP BY mes
            ORDER BY mes
        ''')
        por_mes = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'total_denuncias': total,
            'por_status': por_status,
            'por_mes': por_mes,
            'ultima_atualizacao': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Página de erro 404"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Página de erro 500"""
    registrar_log("ERRO_500", detalhes=str(error))
    return jsonify({
        'success': False,
        'message': 'Erro interno do servidor'
    }), 500

if __name__ == '__main__':
    # Inicializa o banco de dados
    init_database()
    
    # Registra inicialização
    registrar_log("SISTEMA_INICIADO")
    
    # Executa a aplicação
    app.run(host='0.0.0.0', port=5000, debug=False)

