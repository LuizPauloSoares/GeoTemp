![Python](https://img.shields.io/badge/Python_3-3776AB?style=flat&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-41CD52?style=flat&logo=qt&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

# 🌍 GeoTemp — Clima em Tempo Real

Aplicação desktop dark com interface estilo painel de controle que exibe temperatura atual, previsão para 24 horas e previsão semanal de qualquer cidade. A busca pode ser feita por nome da cidade ou CEP, com conversão automática de localidade via API ViaCEP.

> 🚧 Projeto em andamento — funcionalidades principais implementadas, melhorias visuais e mapa em desenvolvimento.

---

## ⚡ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Temperatura atual | Busca clima em tempo real — temperatura, descrição, umidade e vento |
| Previsão 24 horas | Tabela com intervalos de 3 horas mostrando temp, clima e vento |
| Previsão 5 dias | Relatório com mínima e máxima por dia |
| Busca por cidade ou CEP | Aceita nome da cidade ou CEP — converte automaticamente via ViaCEP |
| Validação dupla | Se cidade e CEP forem informados, verifica se o CEP pertence àquela cidade |
| Unidade de temperatura | Celsius, Fahrenheit ou Kelvin — selecionável na interface |
| Telemetria de posição | Exibe latitude e longitude da cidade buscada |

---

## 🛠️ Tecnologias

- Linguagem: **Python 3**
- Interface: **PyQt5**
- APIs: **OpenWeatherMap** (clima e geolocalização) · **ViaCEP** (conversão de CEP)
- Segurança: **.env** para proteger a chave da API (primeira vez usando variáveis de ambiente)
- Controle de versão: **.gitignore** configurado para não expor a chave no GitHub

---

## 🔐 Primeira vez com .env e .gitignore

Este projeto marca a primeira vez usando boas práticas de segurança:

- A chave da API fica no arquivo `.env` — nunca aparece no código
- O `.gitignore` impede que o `.env` seja enviado ao GitHub
- O repositório inclui um `.env.exemplo` mostrando quais variáveis são necessárias

---

## ⚙️ Como executar

<details>
<summary>🔑 Configurar a chave da API</summary>

Crie uma conta gratuita em [openweathermap.org](https://openweathermap.org/api) e gere sua API key.

Renomeie o arquivo `.env.exemplo` para `.env` e cole sua chave:

```
API_KEY=sua_chave_aqui
```

</details>

<details>
<summary>📥 Instalar e rodar</summary>

### 1. Instale as dependências
```bash
pip install PyQt5 requests python-dotenv
```

### 2. Configure o .env (veja acima)

### 3. Execute
```bash
python projetofinal.py
```

</details>

<details>
<summary>🔀 Clonar o repositório</summary>

### 1. Clone
```bash
git clone https://github.com/LuizPauloSoares/GeoTemp.git
```

### 2. Acesse a pasta
```bash
cd GeoTemp
```

### 3. Instale as dependências
```bash
pip install PyQt5 requests python-dotenv
```

### 4. Configure o .env e execute
```bash
python projetofinal.py
```

</details>

---

## 👤 Autor

**Luiz Paulo Soares**  
Desenvolvedor back-end | Python · Java · SQL Server  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/luiz-paulo-soares)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/LuizPauloSoares)
