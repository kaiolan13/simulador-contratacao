import streamlit as st
import pandas as pd
import joblib
from treinador import ajustar_probabilidade

import gdown

url = "https://drive.google.com/uc?id=176u5kEUMqH1rAdZpWCBfceuRyfk8ow2g"
output = "modelo_treinado.pkl"


if "modelo_carregado" not in st.session_state:
    gdown.download(url, output, quiet=False)
    st.session_state["modelo_carregado"] = True

model, colunas_modelo = joblib.load(output)

# Carrega o modelo treinado e as colunas esperadas
opcoes_vagas = [
    "Analista de Dados", "Analista de RH", "Analista de Sistemas", "Analista NOC", "Analista de Suporte",
    "Analistas", "Assistente Administrativo", "Desenvolvedor", "Desenvolvedor .Net", "Desenvolvedor Java",
    "Gerente de Projetos", "SAP MM", "SAP SD", "Scrum Master", "Tech Recruiter"
]

st.set_page_config(page_title="Predição de Contratação", layout="centered")

# --- Início do CSS Embutido ---
st.markdown(
    """
    <style>
    /* Estilos Gerais do Corpo - Definidos principalmente via config.toml */
    /* st.set_page_config já define cores do tema globalmente através do config.toml */
    
    /* Títulos */
    h1 {
        color: #D5D0C4; /* Título principal em cor clara */
    }
    h2, h3, h4 {
        color: #D5D0C4; /* Subtítulos e outros cabeçalhos em cor clara */
    }

    /* Estilo para inputs (Selectbox, Text Input, Number Input, Text Area) */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    div.stNumberInput > div > div input[type="number"],
    .stTextArea > div > div textarea {
        background-color: #D5D0C4 !important; /* Fundo bege claro, com !important para prioridade */
        border: 1px solid #9CA5B1; /* Borda sutil */
        border-radius: 5px; /* Cantos arredondados */
        color: #877C73 !important; /* Texto marrom-cinza, com !important para prioridade */
    }

    /* Garante que a cor do texto nos campos de input permaneça visível ao digitar/focar */
    .stTextInput input,
    .stTextArea textarea,
    div.stNumberInput input {
        color: #877C73 !important; /* Força a cor do texto para marrom-cinza */
    }

    /* Estilo para os botões +/- do NumberInput */
    div.stNumberInput > div > div button {
        background-color: #D5D0C4 !important; /* Fundo bege claro para os botões +/- */
        border: 1px solid #9CA5B1 !important; /* Adiciona borda aos botões +/- */
        color: #877C73 !important; /* Cor dos ícones +/- */
        border-radius: 0 5px 5px 0; /* Arredonda apenas o lado direito */
        margin-left: -1px; /* Ajusta a margem para alinhar com a borda do input */
    }
    /* Estilo específico para o botão de decremento (o primeiro, à esquerda) */
    div.stNumberInput > div > div button:first-of-type {
        border-radius: 5px 0 0 5px; /* Arredonda apenas o lado esquerdo */
        margin-right: -1px; /* Ajusta a margem para alinhar com a borda do input */
    }


    /* Placeholder text para text_input e text_area */
    textarea::placeholder,
    input::placeholder {
        color: #877C73; /* Cor do placeholder em marrom-cinza */
        opacity: 0.7; /* Ligeiramente transparente */
    }

    /* Labels dos inputs */
    .stMarkdown label {
        color: #D5D0C4; /* Cor do texto das labels em claro */
    }
    
    /* Estilo do Botão */
    div.stButton {
        text-align: center; /* Centraliza o contêiner do botão */
    }
    .stButton > button {
        background-color: #3D5E6B; /* Cor forte para o botão de ação */
        color: white !important; /* Texto branco no botão para alto contraste, com !important */
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none; /* Remover borda padrão do botão */
        cursor: pointer;
        transition: background-color 0.3s ease, color 0.3s ease; /* Adiciona transição para a cor do texto */
    }
    
    /* Efeito hover para o botão */
    .stButton > button:hover {
        background-color: #9CA5B1; /* Cor mais clara da paleta ao passar o mouse */
        color: #44474D !important; /* Texto escuro ao passar o mouse, com !important */
    }
    
    /* Estilo da mensagem de alerta (regressão de carreira) */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stMarkdownContainer"] > div[style*="color:#ff8c00"]) > div > div {
        background-color: #D5D0C4; /* Fundo do alerta em bege claro */
        color: #ff8c00 !important; /* Texto laranja forte */
        text-align: center;
        padding: 18px;
        border-radius: 12px;
        font-weight: bold;
        margin-bottom: 15px;
        font-size: 20px;
        border: 1px solid #ffaa00; /* Borda sutil laranja */
    }

    /* Estilização do bloco de resultado da previsão */
    .prediction-result {
        background-color: #3D5E6B; /* Cor mais escura da paleta para o bloco de resultado */
        border-radius: 15px;
        padding: 25px;
        margin-top: 30px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3); /* Sombra para profundidade */
    }
    .prediction-result h3, .prediction-result h4 {
        color: #D5D0C4; /* Texto claro para os resultados */
        margin: 5px 0; /* Ajusta margens */
    }
    .prediction-result .stMarkdown h3[data-testid="stMarkdown"],
    .prediction-result .stMarkdown h4[data-testid="stMarkdown"] {
        color: #D5D0C4; /* Garante que os H3 e H4 internos mantenham a cor */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --- Fim do CSS Embutido ---

# Funções de callback para salvar o estado dos selectbox
def update_experiencia():
    st.session_state["experiencia"] = st.session_state["experiencia_key"]

def update_titulo_vaga():
    st.session_state["titulo_vaga"] = st.session_state["titulo_vaga_key"]

def update_nivel_academico():
    st.session_state["nivel_academico"] = st.session_state["nivel_academico_key"]

def update_nivel_ingles():
    st.session_state["nivel_ingles"] = st.session_state["nivel_ingles_key"]

def update_nivel_espanhol():
    st.session_state["nivel_espanhol"] = st.session_state["nivel_espanhol_key"]

def update_titulo_profissional():
    st.session_state["titulo_profissional"] = st.session_state["titulo_profissional_key"]


st.title("📊 Predição de Contratação")
st.subheader("📝 Preencha os dados do candidato:")

def campo_obrigatorio(valor):
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        return False
    return True

# Linha 1
col1, col2 = st.columns(2)

# Experiência Profissional
experiencia_options = ["Estagiário", "Júnior", "Pleno", "Sênior"]
if "experiencia" not in st.session_state:
    st.session_state["experiencia"] = experiencia_options[0] # Valor inicial padrão
experiencia = col1.selectbox(
    "Experiência Profissional (último cargo ocupado)",
    experiencia_options,
    index=experiencia_options.index(st.session_state["experiencia"]),
    key="experiencia_key",
    on_change=update_experiencia
)

# Vaga para Simulação
if "titulo_vaga" not in st.session_state:
    st.session_state["titulo_vaga"] = opcoes_vagas[0] # Valor inicial padrão
titulo_vaga = col2.selectbox(
    "Vaga para Simulação",
    opcoes_vagas,
    index=opcoes_vagas.index(st.session_state["titulo_vaga"]),
    key="titulo_vaga_key",
    on_change=update_titulo_vaga
)


# Experiência na Área
if "experiencia_na_area" not in st.session_state:
    st.session_state["experiencia_na_area"] = 0
experiencia_na_area = st.number_input(
    "Experiência na Área (anos)",
    min_value=0, max_value=50,
    value=st.session_state["experiencia_na_area"],
    key="experiencia_na_area_key",
    on_change=lambda: st.session_state.update(experiencia_na_area=st.session_state.experiencia_na_area_key) # Salva o valor no session_state
)

# Resumo do CV
if "resumo_cv" not in st.session_state:
    st.session_state["resumo_cv"] = ""
resumo_cv = st.text_area(
    "Resumo do Currículo (experiências, cursos, formações, certificações...) (opcional)",
    value=st.session_state["resumo_cv"],
    key="resumo_cv_key",
    on_change=lambda: st.session_state.update(resumo_cv=st.session_state.resumo_cv_key)
)

# Bloco acadêmico
nivel_academico_options = [
    "Ensino Médio", "Técnico", "Superior Incompleto", "Superior Completo", 
    "Pós-graduação", "Mestrado", "Doutorado"
]
if "nivel_academico" not in st.session_state:
    st.session_state["nivel_academico"] = nivel_academico_options[0]
nivel_academico = st.selectbox(
    "Nível Acadêmico",
    nivel_academico_options,
    index=nivel_academico_options.index(st.session_state["nivel_academico"]),
    key="nivel_academico_key",
    on_change=update_nivel_academico
)

curso_superior = curso_pos = curso_mestrado = curso_doutorado = ""

if nivel_academico in ["Superior Completo", "Pós-graduação", "Mestrado", "Doutorado"]:
    if "curso_superior" not in st.session_state:
        st.session_state["curso_superior"] = ""
    curso_superior = st.text_input(
        "Curso de Graduação",
        value=st.session_state["curso_superior"],
        key="curso_superior_key",
        on_change=lambda: st.session_state.update(curso_superior=st.session_state.curso_superior_key)
    )
if nivel_academico in ["Pós-graduação", "Mestrado", "Doutorado"]:
    if "curso_pos" not in st.session_state:
        st.session_state["curso_pos"] = ""
    curso_pos = st.text_input(
        "Curso de Pós-graduação",
        value=st.session_state["curso_pos"],
        key="curso_pos_key",
        on_change=lambda: st.session_state.update(curso_pos=st.session_state.curso_pos_key)
    )
if nivel_academico in ["Mestrado", "Doutorado"]:
    if "curso_mestrado" not in st.session_state:
        st.session_state["curso_mestrado"] = ""
    curso_mestrado = st.text_input(
        "Curso de Mestrado",
        value=st.session_state["curso_mestrado"],
        key="curso_mestrado_key",
        on_change=lambda: st.session_state.update(curso_mestrado=st.session_state.curso_mestrado_key)
    )
if nivel_academico == "Doutorado":
    if "curso_doutorado" not in st.session_state:
        st.session_state["curso_doutorado"] = ""
    curso_doutorado = st.text_input(
        "Curso de Doutorado",
        value=st.session_state["curso_doutorado"],
        key="curso_doutorado_key",
        on_change=lambda: st.session_state.update(curso_doutorado=st.session_state.curso_doutorado_key)
    )

col3, col4 = st.columns(2)

# Nível de Inglês
nivel_ingles_options = ["Nenhum", "Básico", "Intermediário", "Avançado", "Fluente"]
if "nivel_ingles" not in st.session_state:
    st.session_state["nivel_ingles"] = nivel_ingles_options[0]
nivel_ingles = col3.selectbox(
    "Nível de Inglês",
    nivel_ingles_options,
    index=nivel_ingles_options.index(st.session_state["nivel_ingles"]),
    key="nivel_ingles_key",
    on_change=update_nivel_ingles
)

# Nível de Espanhol
nivel_espanhol_options = ["Nenhum", "Básico", "Intermediário", "Avançado", "Fluente"]
if "nivel_espanhol" not in st.session_state:
    st.session_state["nivel_espanhol"] = nivel_espanhol_options[0]
nivel_espanhol = col4.selectbox(
    "Nível de Espanhol",
    nivel_espanhol_options,
    index=nivel_espanhol_options.index(st.session_state["nivel_espanhol"]),
    key="nivel_espanhol_key",
    on_change=update_nivel_espanhol
)

# Título Profissional Pretendido
titulo_profissional_options = ["Estagiário", "Júnior", "Pleno", "Sênior"]
if "titulo_profissional" not in st.session_state:
    st.session_state["titulo_profissional"] = titulo_profissional_options[0]
titulo_profissional = st.selectbox(
    "Título Profissional Pretendido",
    titulo_profissional_options,
    index=titulo_profissional_options.index(st.session_state["titulo_profissional"]),
    key="titulo_profissional_key",
    on_change=update_titulo_profissional
)


# BOTÃO DE AÇÃO
if st.button("Prever Contratação"):
    experiencia = st.session_state["experiencia"]
    titulo_vaga = st.session_state["titulo_vaga"]
    experiencia_na_area = st.session_state["experiencia_na_area"]
    resumo_cv = st.session_state["resumo_cv"]
    nivel_academico = st.session_state["nivel_academico"]
    curso_superior = st.session_state.get("curso_superior", "") # Usar .get para opcionais
    curso_pos = st.session_state.get("curso_pos", "")
    curso_mestrado = st.session_state.get("curso_mestrado", "")
    curso_doutorado = st.session_state.get("curso_doutorado", "")
    nivel_ingles = st.session_state["nivel_ingles"]
    nivel_espanhol = st.session_state["nivel_espanhol"]
    titulo_profissional = st.session_state["titulo_profissional"]


    obrigatorios = [
        experiencia, titulo_vaga, nivel_academico,
        nivel_ingles, nivel_espanhol, titulo_profissional
    ]
    obrigatorios_nomes = [
        "Experiência Profissional (último cargo ocupado)",
        "Vaga para Simulação",
        "Nível Acadêmico",
        "Nível de Inglês",
        "Nível de Espanhol",
        "Título Profissional Pretendido"
    ]
    if nivel_academico in ["Superior Completo", "Pós-graduação", "Mestrado", "Doutorado"]:
        obrigatorios.append(curso_superior)
        obrigatorios_nomes.append("Curso de Graduação")
    if nivel_academico in ["Pós-graduação", "Mestrado", "Doutorado"]:
        obrigatorios.append(curso_pos)
        obrigatorios_nomes.append("Curso de Pós-graduação")
    if nivel_academico in ["Mestrado", "Doutorado"]:
        obrigatorios.append(curso_mestrado)
        obrigatorios_nomes.append("Curso de Mestrado")
    if nivel_academico == "Doutorado":
        obrigatorios.append(curso_doutorado)
        obrigatorios_nomes.append("Curso de Doutorado")

    campos_preenchidos = [campo_obrigatorio(v) for v in obrigatorios]
    if not all(campos_preenchidos):
        campos_faltando = [nome for nome, ok in zip(obrigatorios_nomes, campos_preenchidos) if not ok]
        st.error("Preencha todos os campos obrigatórios: " + ", ".join(campos_faltando))
    else:
        entrada_dict = {
            "experiencia": experiencia,
            "nivel_academico": nivel_academico,
            "curso_superior": curso_superior,
            "curso_pos": curso_pos,
            "curso_mestrado": curso_mestrado,
            "curso_doutorado": curso_doutorado,
            "nivel_ingles": nivel_ingles,
            "nivel_espanhol": nivel_espanhol,
            "resumo_cv": resumo_cv,
            "titulo_profissional": titulo_profissional,
            "titulo_vaga": titulo_profissional, 
            "experiencia_na_area": experiencia_na_area
        }
        df_input = pd.DataFrame([entrada_dict])
        df_dummies = pd.get_dummies(df_input)
        colunas_faltantes = [col for col in colunas_modelo if col not in df_dummies.columns]
        df_completo = pd.concat([df_dummies, pd.DataFrame(0, index=df_dummies.index, columns=colunas_faltantes)], axis=1)
        df_completo = df_completo[colunas_modelo]

        prob = model.predict_proba(df_completo)[0][1]
        print(f"Probabilidade bruta do modelo: {prob:.4f}")

        prob_ajustada = ajustar_probabilidade(
            prob,
            entrada={
                "nivel_ingles": nivel_ingles,
                "nivel_espanhol": nivel_espanhol,
                "titulo_profissional": experiencia, 
                "titulo_vaga": titulo_profissional, 
                "experiencia_na_area": experiencia_na_area,
                "nivel_academico": nivel_academico,
                "resumo_cv": resumo_cv
            }
        )
        percentual = round(prob_ajustada * 100)

        hierarquia = ["Estagiário", "Júnior", "Pleno", "Sênior"]
        mensagem_alerta = None
        try:
            idx_exp = hierarquia.index(str(experiencia).strip())
            idx_pretendido = hierarquia.index(str(titulo_profissional).strip())
            if idx_pretendido < idx_exp:
                mensagem_alerta = (
                    "⚠️ <b>ATENÇÃO!!!</b><br>🛑 O candidato pleiteia regressão de carreira.<br>⚠️ <b>Proceder com cautela!</b>"
                )
        except Exception:
            mensagem_alerta = None

        if mensagem_alerta:
            st.markdown(
                f"<div style='color:#ff8c00; background:#D5D0C4; text-align:center; padding:18px; border-radius:12px; font-weight:bold; margin-bottom:15px; font-size:20px; border: 1px solid #ffaa00;'>{mensagem_alerta}</div>",
                unsafe_allow_html=True
            )

        if percentual < 20:
            faixa = "🔴 Baixíssima chance de ser contratado"
        elif percentual < 40:
            faixa = "🟠 Baixa chance de ser contratado"
        elif percentual <= 60:
            faixa = "🟡 Média chance de ser contratado"
        elif percentual <= 80:
            faixa = "🟢 Alta chance de ser contratado"
        else:
            faixa = "🔵 Altíssima chance de ser contratado"

        # Bloco de resultado estilizado
        st.markdown(
            f"""
            <div class="prediction-result">
                <h3>{faixa}</h3>
                <h4>Probabilidade de Contratação: <b>{percentual}%</b></h4>
            </div>
            """,
            unsafe_allow_html=True
        )