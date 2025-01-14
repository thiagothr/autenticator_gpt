from flask import Flask, render_template_string, url_for
import pyotp
import os

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Chave secreta fixa para autenticação 2FA (deve ser a mesma configurada no Google Authenticator)
SECRET_KEY = "qm6tgqummidvbsz2p2g5mxcfsk34l7ep"

# Instância de TOTP com a chave secreta e intervalo de 30 segundos
totp = pyotp.TOTP(SECRET_KEY, interval=30)

# Função para gerar o código TOTP
def gerar_codigo_totp():
    return totp.now()

# Rota principal
@app.route("/")
def home():
    codigo = gerar_codigo_totp()  # Gera o código de autenticação
    expiration_time = 30  # Tempo de expiração do código
    logo_url = url_for("static", filename="imagem.jpg")  # URL da logo

    # HTML com o layout atualizado
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ItaguarioGPT</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(45deg, #1a1a1a, #333);
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: linear-gradient(135deg, #2a2a2a, #444);
                border-radius: 12px;
                padding: 30px;
                width: 400px;
                text-align: center;
                color: white;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
            }
            h1 {
                font-size: 28px;
                color: #ffffff;
                margin-bottom: 20px;
            }
            .codigo-container {
                background: #3a3a3a;
                border-radius: 8px;
                padding: 15px;
                font-size: 20px;
                margin-bottom: 20px;
            }
            .codigo {
                font-weight: bold;
                font-size: 26px;
                background-color: #555;
                border-radius: 8px;
                padding: 8px 0;
                color: white;
                display: block;
                margin: 10px auto;
            }
            .contador {
                font-size: 18px;
                color: red;
                font-weight: bold;
                margin-top: 10px;
            }
            .btn {
                background-color: #FF5733;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 15px;
                transition: background-color 0.3s ease;
            }
            .btn:hover {
                background-color: #FF7F50;
            }
            .logo {
                display: block;
                margin: 0 auto 15px;
                width: 120px;
                height: 120px;
                border-radius: 50%;
                object-fit: cover;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="{{ logo_url }}" alt="Logo" class="logo">
            <h1>ItaguarioGPT</h1>
            <p>Clique abaixo para gerar o código de autenticação.</p>
            <div class="codigo-container">
                <p><strong>Código Gerado:</strong></p>
                <div class="codigo" id="codigo">{{ codigo }}</div>
                <p><strong>Este código expira em:</strong> <span id="contador" class="contador">{{ expiration_time }}</span> segundos.</p>
            </div>
            <button class="btn" id="gerarCodigoBtn">Gerar Código</button>
        </div>

        <script>
            var tempoRestante = {{ expiration_time }};
            var contadorElement = document.getElementById('contador');
            var gerarCodigoBtn = document.getElementById('gerarCodigoBtn');

            // Função de contagem regressiva
            function iniciarContagemRegressiva() {
                if (tempoRestante > 0) {
                    tempoRestante--;
                    contadorElement.innerHTML = tempoRestante;
                } else {
                    contadorElement.innerHTML = 'Expirado';
                }
            }

            // Atualiza a contagem regressiva a cada segundo
            setInterval(iniciarContagemRegressiva, 1000);

            // Função para gerar novo código
            gerarCodigoBtn.addEventListener('click', function() {
                location.reload();
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html, codigo=codigo, expiration_time=expiration_time, logo_url=logo_url)

# Inicialização do servidor Flask
if __name__ == "__main__":
    
    app.run()
