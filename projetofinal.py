import os 
from dotenv import load_dotenv # encontra arquivo env 

import requests # conversa com as apis 

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout, QComboBox,QFrame

import ctypes # mostrar o icone 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("geotemp.v1")# faz conq o windows identifique como um app isolado e nao mais um codigo do python

from PyQt5.QtCore import Qt, QRegularExpression # validadores basicamente cria uma regra e quem vai usart ela  
from PyQt5.QtGui import  QRegularExpressionValidator,QIcon

load_dotenv() # cofre 
chave_da_api = os.getenv("API_KEY") # quem vai usar a chave 

def previsao5D():
    """a logica inicial e a mesma porem a api forecast a mesma
     porem o limite de listas e 40 (3 horas ) q da 5 dias 
        variaveis com o primeiro valor de cada item da lista 
          """


    unitemp, simbolo = validabox(tipoTemp.currentText()) 

    
    entrada = validaCampo()

    if entrada == None:
        return
    else:

        lat,lon = geoLocaliza(entrada)
        
        
        url = "https://api.openweathermap.org/data/2.5/forecast"
        
        parametros = {
            "lat": lat,
            "lon": lon,
            "appid": chave_da_api, 
            "units": unitemp,  
            "lang": "pt_br"   
        }

        try:
        
            pedido = requests.get(url, params=parametros)
            
        
                                    
            if pedido.status_code == 200:
                dados = pedido.json()

                #criacao do titulo 
                textoInfo = ""

                textoInfo =  "╔══════════════════════════════════════╗\n"
                textoInfo += f"   RELATÓRIO SEMANAL: {entrada.upper()}\n"
                textoInfo += "╚══════════════════════════════════════╝\n\n"

                


                dataAtual = dados["list"][0]["dt_txt"].split(" ")[0] # quebra toda a data  em 2 e pega a primeira parte 
                tempMax = dados["list"][0]["main"]["temp_max"]#inicia com o primeiro valor (1 lista )
                tempMin = dados["list"][0]["main"]["temp_min"]

                for i in range(40):
                    data_loop = dados["list"][i]["dt_txt"].split(" ")[0] # pega a data (primeira parte e deixa em uma variavel)
                    
                    if data_loop == dataAtual:
                        """vai percorrer  enquanto a data do lop for igual a dataatual 
                        (verifica se e menor a temp min se for vc atribui um novo valor
                        e verifica se e maior q a temp max se for atribui novo valor )
                        caso o contrario  vai formatar a informaçao e vai cria uma variavel
                        texto info q vai receber todas as informaçoes
                        e depois vc seta novos valores (valor do proximo dia na data atual
                        valor da primeira temp max e min daquele dia )"""

                        if dados["list"][i]["main"]["temp_max"] > tempMax:
                            tempMax = dados["list"][i]["main"]["temp_max"]
                        if dados["list"][i]["main"]["temp_min"] < tempMin:
                            tempMin = dados["list"][i]["main"]["temp_min"]
                    else:
                        # --- FRONT: Formatação de Data e Alinhamento de Colunas ---
                        d = dataAtual.split("-")
                        data_br = f"{d[2]}/{d[1]}" # Ex: 07/03
                        
                        # {:>5.1f} Alinha os números à direita para não "sambar" o texto
                        textoInfo += f" ● {data_br}  ➔  MIN: {tempMin:>5.1f}{simbolo}  ┃  MAX: {tempMax:>5.1f}{simbolo}\n"
                        textoInfo += " ──────────────────────────────────────\n"
                        
                        # Reset (Sua lógica original)
                        dataAtual = data_loop
                        tempMin = dados["list"][i]["main"]["temp_min"]
                        tempMax = dados["list"][i]["main"]["temp_max"]

                # --- FRONT: Adicionando o último dia com o novo visual ---
                d = dataAtual.split("-")
                data_br = f"{d[2]}/{d[1]}"
                textoInfo += f" ● {data_br}  ➔  MIN: {tempMin:>5.1f}{simbolo}  ┃  MAX: {tempMax:>5.1f}{simbolo}\n"
                textoInfo += "\n[ SINAL ESTÁVEL - ATUALIZADO ]"
                
                # Use 'janela' (ou o nome do seu objeto principal) para o QMessageBox
                QMessageBox.information(janela, "TELEMETRIA DE PREVISÃO", textoInfo)

            elif pedido.status_code == 404 or pedido.status_code == 400:
                QMessageBox.critical(janela, "Erro", "Cidade não encontrada na base de dados ") 

            else:
                QMessageBox.critical(janela, "Erro", f"Erro na API: {pedido.status_code}")

        except Exception as e:
            QMessageBox.critical(janela, "Erro", f"Falha na conexão: {str(e)}")

def tempAtual():
    """pega o valor do cmbo box e deixa em 2 variaveis uma para servir como parametro e outra pra setar no front 
     pega a entrada q vai vir do valida campo 
     se o retorno nao for nada ele retorna pro inicio 
     ou pega a entrada (cidade) e converte pra lat e lon 
     e depis envia como paramentro 
     se der  certo ele vai e informa a requisiçao para o usuario """

    unitemp, simbolo = validabox(tipoTemp.currentText()) 

    # 2. Pega o que o usuário digitou (Cidade ou CEP)
    entrada = validaCampo()

    if entrada == None:
        return
    else:

        lat,lon = geoLocaliza(entrada)
        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": chave_da_api,
            "units": unitemp,
            "lang": "pt_br"
        } 

        try:
            resposta = requests.get(url, params=params)
            dados = resposta.json()

            if resposta.status_code == 200:
                print (dados)

                temperatura = dados['main']['temp']
                descricao = dados['weather'][0]['description']
                umidade = dados['main']['humidity']
                vento = dados['wind']['speed'] 
                
                # Atualiza a interface (Front-end)
                label_temperatura.setText(f"{temperatura:.1f}{simbolo}")
                label_descricao.setText(descricao.capitalize())
                label_umidade.setText(f"💧 Umidade: {umidade}%")
                label_vento.setText(f"🌬️ Vento: {vento} m/s")
                lblLatValue.setText(f"LAT: {lat}")
                lblLonValue.setText(f"LON: {lon}")
                lblCidadeConfirmada.setText("SINAL OK")

            elif resposta.status_code == 404 or resposta.status_code == 400 :
                QMessageBox.warning(janela, "Erro", "Cidade não encontrada na base de dados de clima.")
            
            else:
                QMessageBox.warning(janela, "Erro", f"Erro na API de Clima: {resposta.status_code}")

        except Exception as e:
            QMessageBox.critical(janela, "Erro Crítico", f"Falha ao obter clima: {e}")

def previsao24h():
    """a logica inicial e a mesma coisa da outra funcao a unica coisa q muda e pq dados vai ser uma lista de listas e cada lista
    vai conter o main ,weather etc  e cada lista e de 3 em 3 horas 
    entao para ter 24hrs tenq ter 8 listas 
    percorrer essas 8 listas e pegar as informaçoes dela e setar no front como se fosse uma tabela a cada iteraçao vc adiciona um valor ce cada 3 hrs
    if de clima so pra setar um emoji na linha """

    unitemp, simbolo = validabox(tipoTemp.currentText()) 

    entrada = validaCampo()


    if entrada == None:
        return
    else:
    
        lat,lon = geoLocaliza(entrada)
        

        url = "https://api.openweathermap.org/data/2.5/forecast"
        
        
        parametros = {
            "lat": lat,
            "lon": lon,
            "appid": chave_da_api,
            "units": unitemp, 
            "lang": "pt_br"   
        } 

        try:
            
            pedido = requests.get(url, params=parametros)
            
            if pedido.status_code == 200:
                dados = pedido.json()

                # serve para limpar a parte q sera impressa a tabela se eu tiver usado esssa funcao antes ele limpa a tabela anterios
                for i in reversed(range(painel_direito.count())):
                    item = painel_direito.itemAt(i)
                    widget = item.widget()
                    if widget and hasattr(widget, "isPrevisao"):
                        painel_direito.removeWidget(widget)
                        widget.setParent(None) # Remove da tela de vez
                        widget.deleteLater()

                #cria otitulo no painel direito centraliza e aplica um estilo
                titulo24h = QLabel(f"🕒 Previsão próximas 24h - {entrada}")
                titulo24h.setAlignment(Qt.AlignCenter)
                titulo24h.setStyleSheet("font-weight: bold; font-size: 14px; color: #0B3C91;")
                titulo24h.isPrevisao = True
                painel_direito.addWidget(titulo24h)

            
                for i in range(8):# percorre os 8 primeiros itens da lista de previsões cada item representa 3 horas, então 8 itens = 24 horas de previsão
                    hora = dados["list"][i]["dt_txt"].split(" ")[1] 
                    tempMin = dados["list"][i]["main"]["temp_min"]
                    tempMax = dados["list"][i]["main"]["temp_max"]
                    clima = dados["list"][i]["weather"][0]["description"]
                    umidade = dados["list"][i]["main"]["humidity"]
                    vento = dados["list"][i]["wind"]["speed"]
                    direcao = dados["list"][i]["wind"]["deg"]

                    clima_lower = clima.lower()# deixa a descricao em lower e dependendo da descricao coloca um emogi
                    if "chuva" in clima_lower:
                        clima = "🌧️ " + clima
                    elif "nublado" in clima_lower:
                        clima = "☁️ " + clima
                    elif "sol" in clima_lower or "claro" in clima_lower:
                        clima = "☀️ " + clima

                    # --- FRONT --- cria um layout 
                    linhaLayout = QHBoxLayout()
                    
                    # criacao da linha para aparecer na tela 
                    textos = [
                        f"⌚ {hora}", 
                        f"❄️ {tempMin:.1f}{simbolo} / 🌡️ {tempMax:.1f}{simbolo}", 
                        clima, 
                        f"💧 {umidade}%", 
                        f"🌬️ {vento} m/s {direcao}°"
                    ]
                    
                    
                    # --- FRONT --- centraliza adiciona no layout percorre a lista textos e cria um qlabel para cada texto
                    for lblText in textos:
                        lbl = QLabel(lblText)
                        lbl.setAlignment(Qt.AlignCenter)
                        linhaLayout.addWidget(lbl)

                    linhaWidget = QWidget()
                    linhaWidget.setLayout(linhaLayout)#cria como se fosse um container e vazio para colocar todo o for dfentro e depois adiicona na tela 
                    linhaWidget.isPrevisao = True
                    painel_direito.addWidget(linhaWidget)

            elif pedido.status_code == 404 or pedido.status_code == 400 :
                    QMessageBox.warning(janela, "Erro", "Cidade não encontrada na base de dados de clima.")
                
            else:
                QMessageBox.warning(janela, "Erro", f"Erro na API de Clima: {pedido.status_code}")

                    
        except Exception as e:
            QMessageBox.critical(janela, "Erro", f"Falha na previsão: {e}")

def tratarEntradaDupla(cidade,cep):

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            dados = response.json()
            print (dados)

            if dados.get("erro") == "true":
                QMessageBox.warning(janela, "Atenção", "CEP não encontrado.")
                return None
            else:
                localidade = dados.get('localidade', '')                
                bairro = dados.get('bairro','')

                if localidade.lower() != cidade.lower():
                    QMessageBox.warning(janela, "Atenção", "CEP não pertence a essa cidade.")
                    return None
                else:
                    cep = localidade
                    lblEstadoPais.setText(f"{localidade} \n {bairro}")
                    return cep
    except Exception as e:
        QMessageBox.critical(janela, "Erro", f"Falha na conexão: {str(e)}")
        return None

def validabox(tipoTemp):
    """vai pegar o texto que foi selecionado no combo box
       e vai definir aquela forma de temperatura para ir 
       como parametro e vai setar o simbolo na tela 
            meu erro foi tentar usar o set text pq ele ja setava 
            na hora de mostrar o simbolo sumia """

    unitemp = ""
    simbolo = ""

    if tipoTemp == "Celsius":
        simbolo = "°C" # simbolo q retorna para o front 
        unitemp = "metric" # vai para o parametro das apis principais
        return unitemp,simbolo
    elif tipoTemp == "Fahrenheit":
        simbolo = "°F"
        unitemp = "imperial"
        return unitemp,simbolo
    elif tipoTemp == "Kelvin":
        simbolo = "K"
        unitemp = "standard"
        return unitemp,simbolo

def validaCampo():
    """valida os campos para a pesquisa 
        da um strip para retirar todo o espaço 
        e da uma msg se o usuario nao digitou nada ou se usou so espaço
        verifica se o cep foi informado e a cidade nao  se for cep ele envia pra funcao alterar o cep para cidade 
        se for cidade ja vai direto pra funçao principal 
        se os 2 forem inseridos (validar se o cep e da cidade informada se nao eu mando uma mensagem se nao ele pega a cidade e continua o codigo normalmente )"""

    cidade = caixaTextoPesquisaCidade.text().strip().lower()
    cep = caixaTextoPesquisaZip.text().strip()
    
    if (cep == "") and (cidade == ""):
        QMessageBox.critical(janela, "⚠️ Atenção", "Por favor, informe a cidade ou o CEP.")
        caixaTextoPesquisaCidade.setFocus()
        return 
    elif cep == "" and cidade != "":
        return cidade
    elif cidade == "" and cep != "":
        localizacao = converterCidade(cep)
        return localizacao
    else:
        resultado_duplo = tratarEntradaDupla(cidade, cep) 
        return resultado_duplo

def converterCidade(cep):

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            dados = response.json()

            if dados.get("erro") == "true":
                QMessageBox.warning(janela, "Atenção", "CEP não encontrado.")
                return None
            else:

               cidade = dados.get('localidade', '')
               bairro = dados.get('bairro','')
               print(bairro)
               lblEstadoPais.setText(f"{cidade} \n {bairro}")
               return cidade
               
            
        else:
            QMessageBox.critical(janela, "Erro", f"Servidor ViaCEP fora do ar: {response.status_code}")
            return None

    except Exception as e:
        QMessageBox.critical(janela, "Erro", f"Falha na conexão: {str(e)}")
        return None

def geoLocaliza(cidade):

    url = "http://api.openweathermap.org/geo/1.0/direct"

    parametros = {
            "q": cidade,         
            "limit": 1,           # primeiro valor
            "appid": chave_da_api     
        }

    try:
        resposta = requests.get(url, params=parametros)

        if resposta.status_code == 200:
            dados = resposta.json()

            lat = dados[0]["lat"]
            lon = dados[0]["lon"]

            return lat, lon

        else:
            return None, None

    except Exception:
       
        return None, None


regraCidade = QRegularExpression(r"^[A-Za-zÀ-ÿ\s]+$") 
validaCidade = QRegularExpressionValidator(regraCidade)

regraCep = QRegularExpression("^[0-9]{8}$") 
validaCep = QRegularExpressionValidator(regraCep)


# ---------------- Aplicação e Interface ----------------
app = QApplication(sys.argv)
janela = QWidget()
janela.setWindowTitle("GeoTemp")
janela.resize(1100, 600)
janela.setStyleSheet("background-color: #1E1E2F; color: white;")
janela.setWindowIcon(QIcon("logo.png"))# ele pega o icone q eu baixei e coloca um tradutor pro python enternder q e um icone

layout_principal = QHBoxLayout()

# ---------------- Painel esquerdo (Controle e Telemetria) ----------------
painel_esquerdo = QVBoxLayout() # tudo q esta dentro vai ficar na vertical 
painel_esquerdo.setContentsMargins(15, 15, 15, 15) # espa;o ate a borda 
painel_esquerdo.setSpacing(12) # espaco a cada item 

# --- Seção de Busca ---
lblTituloBusca = QLabel("🔎 CONTROLE DE BUSCA")
lblTituloBusca.setStyleSheet("color: #00FFFF; font-size: 12px; font-weight: bold; letter-spacing: 1.5px;")
painel_esquerdo.addWidget(lblTituloBusca)

estilo_input_moderno = """
    QLineEdit {
        background-color: #2E2E3E; border: 1px solid #444466;
        border-radius: 6px; padding: 10px; color: white; font-size: 13px;
    }
    QLineEdit:focus { border: 1px solid #00FFFF; }
"""

caixaTextoPesquisaCidade = QLineEdit()
caixaTextoPesquisaCidade.setPlaceholderText("Nome da Cidade (ex: São Paulo)")
caixaTextoPesquisaCidade.setStyleSheet(estilo_input_moderno)
caixaTextoPesquisaCidade.setValidator(validaCidade)

caixaTextoPesquisaZip = QLineEdit()
caixaTextoPesquisaZip.setPlaceholderText("Ou digite o CEP")
caixaTextoPesquisaZip.setStyleSheet(estilo_input_moderno)
caixaTextoPesquisaZip.setValidator(validaCep) # seta o validaddor na caixa texto 

painel_esquerdo.addWidget(caixaTextoPesquisaCidade) # adiciona no painel esquerdo 
painel_esquerdo.addWidget(caixaTextoPesquisaZip)

# --- Seletor de Unidade ---
lblUnidade = QLabel("UNIDADE MÉTRICA")
lblUnidade.setStyleSheet("color: #777799; font-size: 10px; font-weight: bold; margin-top: 5px;")
tipoTemp = QComboBox()
tipoTemp.addItems(["Celsius", "Fahrenheit", "Kelvin"])
tipoTemp.setStyleSheet("background-color: #2E2E3E; border: 1px solid #444466; border-radius: 6px; padding: 5px; color: white;")
painel_esquerdo.addWidget(lblUnidade)
painel_esquerdo.addWidget(tipoTemp)

# --- Botões de Ação ---
botao_buscar = QPushButton("BUSCAR AGORA")
botao_buscar.setStyleSheet("background-color: #00FFFF; color: #121212; font-weight: bold; border-radius: 6px; padding: 12px;")
botao_buscar.setCursor(Qt.PointingHandCursor)
botao_buscar.clicked.connect(tempAtual)

layout_botoes_previsao = QHBoxLayout()
botaoPrevisao24h = QPushButton("24 HORAS")
botaoPrevisao24h.clicked.connect(previsao24h)
botaoPrevisao5D = QPushButton("5 DIAS")
botaoPrevisao5D.clicked.connect(previsao5D)

estilo_btn_sec = "QPushButton { background-color: transparent; border: 1px solid #FFD700; color: #FFD700; font-weight: bold; border-radius: 6px; padding: 8px; } QPushButton:hover { background-color: #FFD700; color: #121212; }"
botaoPrevisao24h.setStyleSheet(estilo_btn_sec)
botaoPrevisao5D.setStyleSheet(estilo_btn_sec.replace("#FFD700", "#FF4500"))

layout_botoes_previsao.addWidget(botaoPrevisao24h)
layout_botoes_previsao.addWidget(botaoPrevisao5D)

painel_esquerdo.addWidget(botao_buscar)
painel_esquerdo.addLayout(layout_botoes_previsao)

# --- DIVISOR E NOVA TELEMETRIA (A PARTE QUE VOCÊ QUERIA INCLUIR) ---
linha = QFrame()
linha.setFrameShape(QFrame.HLine)
linha.setStyleSheet("background-color: #33334d; max-height: 1px; margin: 10px 0px;")
painel_esquerdo.addWidget(linha)

lblStatusTitulo = QLabel("📍 TELEMETRIA DE POSIÇÃO")
lblStatusTitulo.setStyleSheet("color: #00FFFF; font-size: 10px; font-weight: bold; letter-spacing: 2px;")
painel_esquerdo.addWidget(lblStatusTitulo)

layout_coords = QHBoxLayout()
estilo_box_coord = "background-color: #161625; border: 1px solid #33334d; border-radius: 4px; color: #00FF00; font-family: 'Consolas'; font-size: 13px; padding: 8px;"

lblLatValue = QLabel("LAT: --.----")
lblLatValue.setStyleSheet(estilo_box_coord)
lblLatValue.setAlignment(Qt.AlignCenter)

lblLonValue = QLabel("LON: --.----")
lblLonValue.setStyleSheet(estilo_box_coord)
lblLonValue.setAlignment(Qt.AlignCenter)

layout_coords.addWidget(lblLatValue)
layout_coords.addWidget(lblLonValue)
painel_esquerdo.addLayout(layout_coords)

frame_cidade = QFrame()
frame_cidade.setStyleSheet("background-color: #252538; border-left: 5px solid #00FFFF; border-radius: 5px;")
layout_interna_cidade = QVBoxLayout(frame_cidade)

lblCidadeConfirmada = QLabel("AGUARDANDO SINAL...")
lblCidadeConfirmada.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
lblEstadoPais = QLabel("ESTADO/PAÍS: --")
lblEstadoPais.setStyleSheet("color: #8888AA; font-size: 10px; font-weight: bold; text-transform: uppercase;")

layout_interna_cidade.addWidget(lblCidadeConfirmada)
layout_interna_cidade.addWidget(lblEstadoPais)
painel_esquerdo.addWidget(frame_cidade)

painel_esquerdo.addStretch()

# --- CENTRO (MAPA) ---
area_mapa = QLabel("MAPA MUNDI\n(Espaço para Visualização)")
area_mapa.setStyleSheet("background-color: #2E2E3E; border: 2px solid #00FFFF; border-radius: 15px;")
area_mapa.setAlignment(Qt.AlignCenter)

# ---------------- Painel direito (Onde o Clima brilha) ----------------
painel_direito = QVBoxLayout()
painel_direito.setContentsMargins(15, 15, 15, 15)
painel_direito.setSpacing(15)

# Título do Bloco
lblResultado = QLabel("🌡️ CONDIÇÕES ATUAIS")
lblResultado.setStyleSheet("color: #00FFFF; font-size: 14px; font-weight: bold; letter-spacing: 1px;")
lblResultado.setAlignment(Qt.AlignCenter)

# A Temperatura Principal (O "Herói" da tela)
label_temperatura = QLabel("--°C")
label_temperatura.setStyleSheet("""
    color: white; 
    font-size: 64px; 
    font-weight: 800; 
    margin-top: 10px;
""")
label_temperatura.setAlignment(Qt.AlignCenter)

# Descrição do Clima (Ex: "Céu Limpo")
label_descricao = QLabel("Aguardando busca...")
label_descricao.setStyleSheet("color: #FFD700; font-size: 18px; font-weight: 500; text-transform: capitalize;")
label_descricao.setAlignment(Qt.AlignCenter)

# --- Criando uma sub-grade para Umidade e Vento (Lado a Lado) ---
layout_detalhes = QHBoxLayout()

# Bloco Umidade
quadro_umidade = QVBoxLayout()
lbl_tit_umidade = QLabel("UMIDADE")
lbl_tit_umidade.setStyleSheet("color: #55FFFF; font-size: 10px; font-weight: bold;")
label_umidade = QLabel("--%")
label_umidade.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
quadro_umidade.addWidget(lbl_tit_umidade, 0, Qt.AlignCenter)
quadro_umidade.addWidget(label_umidade, 0, Qt.AlignCenter)

# Bloco Vento
quadro_vento = QVBoxLayout()
lbl_tit_vento = QLabel("VENTO")
lbl_tit_vento.setStyleSheet("color: #55FFFF; font-size: 10px; font-weight: bold;")
label_vento = QLabel("-- km/h")
label_vento.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
quadro_vento.addWidget(lbl_tit_vento, 0, Qt.AlignCenter)
quadro_vento.addWidget(label_vento, 0, Qt.AlignCenter)

layout_detalhes.addLayout(quadro_umidade)
layout_detalhes.addLayout(quadro_vento)

# Adicionando tudo ao painel principal direito
painel_direito.addWidget(lblResultado)
painel_direito.addWidget(label_temperatura)
painel_direito.addWidget(label_descricao)
painel_direito.addSpacing(20)
painel_direito.addLayout(layout_detalhes)
painel_direito.addStretch() # Empurra tudo para cima

layout_principal.addLayout(painel_esquerdo, 2) # define quantas partes da tela cada painel vai ocupar (independente do tamanho )
layout_principal.addWidget(area_mapa, 4)
layout_principal.addLayout(painel_direito, 2)

janela.setLayout(layout_principal)
janela.show()
sys.exit(app.exec_())

"""
icone
    entao primeiro e uma forma do sistema interpretar o codigo pq qundo vc executa o codigo ele ve q e do python 
    e ja entende um codigo do python mas para alterar isso nos criamos essa conexao criamos um identificador do 
    codigo q sera diferente do python (meio q um identificador ) e logo apos eu coloco o icone do identificador
    meio q vai informar q e um app novo e vai mostra q tem icone diferente do python
        import ctypes # cria uma conexao com windows//cria meio q um docomento (uma forma do sistema identificar o codico meio q um cpf)//vai pegar o icone q eu coloquei para aparecer como icone de codigo
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("geotemp.v1")

env 
    pip install python-dotenv
    env e um arquivo q esconde suas chaves para nao aparecer no codigo serve como protecao
    pra usar vc cria um arquivo .env
    o vscode entende ele (mesma pasta)
    vc inporta quem consegue interagir com arquivos do windo
    e quem consegue ler o arquivo
    vc utilixa quem consegue ler o arquivo como uma chave q consegue ver oq esta escondido
    e depois vc cria uma variavel q aconsegue pegar o valor daquolo q vc esta informando
            import os # ele q tem a permicao para interagir com as pastas do windows(ele e meio q o gerente )
            from dotenv import load_dotenv # quem consegue ler o arquivo
            load_dotenv() # Abre o cofre
            chave_da_api = os.getenv("API_KEY") # Pega o que está lá dentro

#Desempacotamento 
    e quando vc retorna 2 ou mais valore e quando vc for chamar vc cria a quantidade 
    de variaveis mas tenq tomar cuidado na ordem de chamada  
    
QVBoxLayout
    VC um painel vertical e tudo q for inserido nesse painel vai ser inserido de cima para baixo

QHBoxLayout          
    cria um painel na horizontal tudo e inserido da esquerda para a direita 
    depois de criar os 3 paineis o frma vai receber (QHBoxLayout) para inserir na janela 

"""
