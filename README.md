# Simulador de Contratação – POSTECH Datathon

Este projeto foi desenvolvido como parte da Fase 5 do Datathon da pós-graduação em Data Analytics da PUC-Rio (POSTECH). Trata-se de um simulador de empregabilidade que estima a chance de um candidato ser contratado para uma vaga específica, com base em seu perfil.

## 🎯 Objetivo

A aplicação tem como foco auxiliar equipes de RH a simularem a chance de contratação de candidatos em diferentes perfis, considerando uma base histórica de dados reais.

## 🧠 Tecnologias e Bibliotecas Utilizadas

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Pandas](https://pandas.pydata.org/)
- [Joblib](https://joblib.readthedocs.io/)
- HTML e CSS para customização visual

## 📁 Estrutura de Arquivos

```
📦 Projeto
├── simulador_final.py         # Interface principal do app Streamlit
├── treinador.py               # Script de treinamento e lógica e escalonamento
├── modelo_treinado.pkl        # Modelo RandomForest treinado e serializado
├── dados_processados.csv      # Dados processados utilizados no treinamento
├── config.toml                # Arquivo de configuração do Streamlit
└── README.md                  # Este arquivo
```

## 🚀 Como Executar Localmente

1. Clone este repositório:

```bash
git clone https://github.com/seuusuario/simulador-contratacao.git
cd simulador-contratacao
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate       # Windows
```

3. Instale os requisitos:

```bash
pip install -r requirements.txt
```

Ou, instale manualmente:

```bash
pip install streamlit pandas scikit-learn joblib
```

4. Execute o aplicativo:

```bash
python -m streamlit run simulador_final.py
```

## 🎨 Aparência

O visual da aplicação planejado com as seguintes definições:

- **Cor de fundo principal:** `#030085` (azul escuro).
- **Fundo de campos de entrada (inputs):** `#E031EB` (violeta).
- **Cor do texto principal:** `#060126` (preto arroxeado).
- **Fonte:** Ubuntu.
- **Sombreamento das letras:** `#1BF2B5` (verde água).
- **Cartões e alertas de resultado:** também em `#1BF2B5`, criando contraste visual e legibilidade.
- **Botão de ação:** centralizado, sem ícones, com hover em tom harmônico.

## 🔍 Lógica de Predição e Balanceamento

O modelo utilizado é um `RandomForestClassifier`, complementado por uma lógica de ajuste baseada em senso comum de mercado, isso foi necessário pois o modelo foi treinado utilizando dados reais que não foram preenchidos da maneira mais efetiva, existiam muitos dados ausentes para a maioria dos candidatos. Conforme Segue:

- Bonificação por experiência na área
- Penalização por progressão irregular de carreira
- Avaliação de nível acadêmico versus vaga
- Avaliação de fluência em idiomas

Essa lógica foi aplicada **após a predição bruta** do modelo, garantindo interpretabilidade.

## 👨‍💼 Autor

**Kaio Ribeiro Rocha**  
Aluno da Pós-graduação em Data Analytics – FIAP (POSTECH)  
[GitHub](https://github.com/kaiolan13) | [LinkedIn](https://www.linkedin.com/in/kaio-ribeiro-rocha/)