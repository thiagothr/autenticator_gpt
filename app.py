from flask import Flask, render_template_string, url_for
import pyotp
import os

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Definindo uma chave secreta fixa
SECRET_KEY = "kcififz273illdvwebsietiqmagjf5jv"  # Use uma chave segura em produção

# Função para gerar o código TOTP
def gerar_codigo_totp():
    totp = pyotp.TOTP(SECRET_KEY, interval=60)  # Código expira em 60 segundos
    return totp.now()

# Rota principal
@app.route("/")
def home():
    codigo = gerar_codigo_totp()
    expiration_time = 60
    logo_url = url_for("static", filename="imagem.jpg")
    
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
                background: linear-gradient(45deg, #000, #333);
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: linear-gradient(135deg, #444, #222);
                border-radius: 10px;
                padding: 40px;
                width: 400px;
                text-align: center;
                color: white;
            }
            h1 {
                font-size: 32px;
                color: #fff;
                margin-bottom: 20px;
            }
            .codigo-container {
                background: linear-gradient(135deg, #555, #333);
                border-radius: 8px;
                padding: 20px;
                font-size: 24px;
                margin-bottom: 20px.
            }
            .codigo {
                font-weight: bold;
                font-size: 30px;
                background-color: #666;
                border-radius: 8px;
                padding: 10px.
            }
            .contador {
                font-size: 20px;
                color: red;
                font-weight: bold.
                margin-top: 10px.
            }
            .btn {
                background-color: #FF5733;
                color: white;
                padding: 15px 25px;
                border: none.
                border-radius: 5px.
                font-size: 18px.
                cursor: pointer.
                margin-top: 20px.
                transition: background-color 0.3s ease.
            }
            .btn:hover {
                background-color: #FF7F50.
            }
            .logo {
                display: block;
                margin: 0 auto 20px.
                width: 150px.
                height: 150px.
                border-radius: 50%.
                object-fit: cover.
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
