import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    df = pd.read_csv("dados_processados.csv")
    X = df[["nivel_academico", "nivel_ingles", "nivel_espanhol", "titulo_profissional", "titulo_vaga"]]
    X = pd.get_dummies(X)
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    joblib.dump((model, X.columns.tolist()), "modelo_treinado.pkl")

hierarquia = ["estagiário", "júnior", "pleno", "sênior"]

idioma_pesos = {
    "nenhum": -8,
    "básico": 5,
    "intermediário": 10,
    "avançado": 12,
    "fluente": 14
}

def bonus_nivel_acad_cargo(nivel, vaga):
    nivel = nivel.lower()
    vaga = vaga.lower()
    if "ensino médio" in nivel:
        return {"estagiário": 30, "júnior": -8, "pleno": -80, "sênior": -90}.get(vaga, 0)
    elif "técnico" in nivel:
        return {"estagiário": 55, "júnior": -10, "pleno": -80, "sênior": -90}.get(vaga, 0)
    elif "superior incompleto" in nivel:
        return {"estagiário": 50, "júnior": 10, "pleno": -80, "sênior": -90}.get(vaga, 0)
    elif "superior completo" in nivel:
        return {"estagiário": 40, "júnior": 20, "pleno": 0, "sênior": -60}.get(vaga, 0)
    elif "pós" in nivel:
        return {"estagiário": 60, "júnior": 40, "pleno": 15, "sênior": 10}.get(vaga, 0)
    elif "mestrado" in nivel:
        return {"estagiário": 77, "júnior": 46, "pleno": 21, "sênior": 14}.get(vaga, 0)
    elif "doutorado" in nivel:
        return {"estagiário": 81, "júnior": 57, "pleno": 26, "sênior": 17}.get(vaga, 0)
    return 0

def ajustar_probabilidade(prob, entrada):
    ajuste = 0

    titulo = str(entrada.get("titulo_profissional", "")).strip().lower()
    vaga = str(entrada.get("titulo_vaga", "")).strip().lower()

    try:
        idx_titulo = hierarquia.index(titulo)
        idx_vaga = hierarquia.index(vaga)
        diff = idx_vaga - idx_titulo

        if diff == 0:
            ajuste += 15
        elif diff == 1:
            ajuste += 6
        elif diff > 1:
            ajuste -= 60
    except Exception:
        diff = None

    nivel_acad = str(entrada.get("nivel_academico", "")).strip().lower()
    bonus_acad = bonus_nivel_acad_cargo(nivel_acad, vaga)
    ajuste += bonus_acad

    soma_idiomas = 0
    for col in ["nivel_ingles", "nivel_espanhol"]:
        nivel = str(entrada.get(col, "")).strip().lower()
        soma_idiomas += idioma_pesos.get(nivel, 0)
    if soma_idiomas < -12:
        soma_idiomas = -12
    if soma_idiomas > 20:
        soma_idiomas = 20
    ajuste += soma_idiomas

    experiencia = entrada.get("experiencia_na_area", 0)
    try:
        experiencia = float(experiencia)
    except:
        experiencia = 0

    if experiencia == 0 and "estagiário" not in vaga:
        ajuste -= 10
    else:
        ajuste += experiencia * 2

    resumo_cv = str(entrada.get("resumo_cv", "")).strip()
    if resumo_cv:
        num_palavras = len(resumo_cv.split())
        bonus_cv = min(num_palavras * 2, 18)
    else:
        bonus_cv = -2
    ajuste += bonus_cv

    ajuste = min(ajuste, 72)
    ajuste_clipped = min(max(ajuste, -99), 99)
    prob_percent = prob * 100
    prob_ajustada = prob_percent + ajuste_clipped
    prob_ajustada = min(max(prob_ajustada, 1), 99)

    return prob_ajustada / 100
