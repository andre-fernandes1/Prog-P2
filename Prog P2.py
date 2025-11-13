import streamlit as st
import json
import os
import tempfile
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


DB_PATH = Path("db.json")

def load_db_raw():
    """Carrega JSON sem alterar session_state."""
    if not DB_PATH.exists():
        return {}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        st.warning(f"Erro lendo banco de dados: {e}")
        return {}

def save_db(data: dict):
    """Salva JSON de forma atômica."""
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(dir=".", text=True)
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, DB_PATH)
    except Exception as e:
        st.error(f"Erro salvando DB: {e}")

#    MAPA UNIFICADO DE MATÉRIAS POR PERÍODO


MAPA_PERIODOS = {
    1: {
        "Teoria do Direito": {
            "key": "teoria_do_direito",
            "professor": "Prof. Fernando Leal"
        },
        "Teoria do Estado Democrático": {
            "key": "teoria_do_estado_democratico",
            "professor": "Prof. Leandro Molhano"
        },
        "Pensamento Jurídico Brasileiro": {
            "key": "pensamento_juridico_brasileiro",
            "professor": "Profª Elisa Cruz"
        },
        "Economia": {
            "key": "economia",
            "professor": "Prof. Leonardo Costa"
        },
        "Teoria do Direito Constitucional": {
            "key": "teoria_constitucional",
            "professor": "Prof. Felipe Fonte"
        },
        "Crime e Sociedade": {
            "key": "crime_sociedade",
            "professor": "Profs. Fernanda Prates e Thiago Bottino"
        }
    },

    2: {
        "Sociologia Jurídica": {
            "key": "sociologia_juridica",
            "professor": "Prof. Camila Alves"
        },
        "Programação para Advogados": {
            "key": "programacao_para_advogados",
            "professor": "Prof. Josir Gomes"
        },
        "Teoria Geral do Direito Civil": {
            "key": "teoria_geral_direito_civil",
            "professor": "Prof. Filipe Medon"
        },
        "Análise Econômica do Direito": {
            "key": "analise_economica_direito",
            "professor": "Prof. Paulo Mello"
        },
        "Penas e Medidas Alternativas": {
            "key": "penas_medidas_alternativas",
            "professor": "Prof. André Mendes"
        },
        "Design Institucional": {
            "key": "design_institucional",
            "professor": "Prof. Wallace Corbo"
        },
        "Organização do Estado e Direitos Fundamentais": {
            "key": "organizacao_estado_direitos_fundamentais",
            "professor": "Profs. Alvaro Palma, Gustavo Schmidt e Guilherme Aleixo"
        }
    }
}

# período 3,4,5 são dinâmicos
PERIODOS_DINAMICOS = ["periodo_3", "periodo_4", "periodo_5"]

# Conjunto das LISTAS FIXAS (extraído automaticamente do mapa)
LISTAS_FIXAS = [info["key"] for periodo in MAPA_PERIODOS.values() for info in periodo.values()]

# ============================================
#    INICIALIZAÇÃO
# ============================================

def inicializar_base():
    for key in LISTAS_FIXAS:
        st.session_state.setdefault(key, [])
    for pdyn in PERIODOS_DINAMICOS:
        st.session_state.setdefault(pdyn, {})

def merge_db_into_session(db: dict):
    for k, v in db.items():
        if isinstance(v, list):
            st.session_state.setdefault(k, [])
            st.session_state[k].extend(v)
        elif isinstance(v, dict):
            st.session_state.setdefault(k, {})
            for materia, obras in v.items():
                st.session_state[k].setdefault(materia, [])
                st.session_state[k][materia].extend(obras)

def build_persistent_db():
    db = {key: st.session_state.get(key, []) for key in LISTAS_FIXAS}
    for pdyn in PERIODOS_DINAMICOS:
        if pdyn in st.session_state:
            db[pdyn] = st.session_state[pdyn]
    return db

def carregar_dados():
    if not st.session_state.get("dados_carregados"):
        data = load_db_raw()
        merge_db_into_session(data)
        st.session_state.dados_carregados = True

inicializar_base()
carregar_dados()

st.set_page_config(page_title='Base de dados de Direito', layout='centered')
st.title('Base de dados de Direito 📚')
st.subheader('Escola de Direito - FGV Direito Rio')

# modo persistente
if 'mode' not in st.session_state:
    st.session_state.mode = None

# --------------------------------------------
# Função: adicionar obra (usa MAPA_PERIODOS)
# --------------------------------------------
def add_data():
    st.header('Adicionar obra')
    st.write('Aqui você pode adicionar novas obras à base de dados de Direito.')

    # mantém prev para evitar reaproveitamento indevido de widgets
    if "add_periodo_prev" not in st.session_state:
        st.session_state.add_periodo_prev = None

    periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'], key="add_periodo")

    # se mudou o período, removemos keys de matéria para evitar estado "vazado"
    if st.session_state.add_periodo_prev != st.session_state.add_periodo:
        for k in ("add_materia_p1", "add_materia_p2", "add_materia_other"):
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.add_periodo_prev = st.session_state.add_periodo

    with st.form("form_adicionar_obra"):
        nome = st.text_input('Nome da obra', key="add_nome")
        autor = st.text_input('Autor', key="add_autor")

        # cria widget de matéria conforme o período selecionado (widgets com chaves distintas)
        if periodo == '1º Período':
            materias = list(MAPA_PERIODOS[1].keys())
            _ = st.selectbox('Matéria', materias, key="add_materia_p1")
        elif periodo == '2º Período':
            materias = list(MAPA_PERIODOS[2].keys())
            _ = st.selectbox('Matéria', materias, key="add_materia_p2")
        else:
            _ = st.text_input('Matéria (digite o nome da matéria)', key="add_materia_other")

        submitted = st.form_submit_button('Adicionar')

        if submitted:
            nome_val = st.session_state.get("add_nome", "").strip()
            autor_val = st.session_state.get("add_autor", "").strip()
            periodo_val = st.session_state.get("add_periodo", "").strip()

            # lê matéria com prioridade p1, p2, other
            materia_val = ""
            if st.session_state.get("add_materia_p1", None):
                materia_val = st.session_state.get("add_materia_p1")
            elif st.session_state.get("add_materia_p2", None):
                materia_val = st.session_state.get("add_materia_p2")
            elif st.session_state.get("add_materia_other", "").strip():
                materia_val = st.session_state.get("add_materia_other").strip()

            materia_val = materia_val.strip() if isinstance(materia_val, str) else materia_val

            if not nome_val or not autor_val or not materia_val:
                st.warning("Preencha 'Nome', 'Autor' e 'Matéria' antes de adicionar.")
            else:
                # converte label do período em número
                periodo_map_label_to_num = {'1º Período': 1, '2º Período': 2, '3º Período': 3, '4º Período': 4, '5º Período': 5}
                pnum = periodo_map_label_to_num.get(periodo_val)

                where_inserted = None

                if pnum in (1, 2):
                    # tenta mapear pelo MAPA_PERIODOS
                    entry = MAPA_PERIODOS.get(pnum, {}).get(materia_val)
                    if entry:
                        key = entry["key"]
                        st.session_state.setdefault(key, [])
                        st.session_state[key].append({'nome': nome_val, 'autor': autor_val})
                        where_inserted = key
                    else:
                        # fallback para caso de matéria não mapeada (coloca na primeira lista do período)
                        first_key = list(MAPA_PERIODOS[pnum].values())[0]["key"]
                        st.session_state.setdefault(first_key, [])
                        st.session_state[first_key].append({'nome': nome_val, 'autor': autor_val})
                        where_inserted = first_key
                else:
                    # períodos dinâmicos: armazena em dict por matéria
                    key_map = {'3º Período': 'periodo_3', '4º Período': 'periodo_4', '5º Período': 'periodo_5'}
                    dyn_key = key_map.get(periodo_val, 'periodo_outros')
                    st.session_state.setdefault(dyn_key, {})
                    st.session_state[dyn_key].setdefault(materia_val, [])
                    st.session_state[dyn_key][materia_val].append({'nome': nome_val, 'autor': autor_val})
                    where_inserted = f"{dyn_key}:{materia_val}"

                # salva
                save_db(build_persistent_db())

                # limpa campos do form para próxima inclusão
                for k in ("add_nome", "add_autor", "add_materia_p1", "add_materia_p2", "add_materia_other"):
                    if k in st.session_state:
                        del st.session_state[k]

                st.success(f'Obra "{nome_val}" — {autor_val} adicionada com sucesso! (salva em {where_inserted})')

# --------------------------------------------
# Função: ver obras (usa MAPA_PERIODOS)
# --------------------------------------------
def view_data():
    st.header('Ver obras')
    st.write('Aqui você pode ver as obras na base de dados de Direito.')

    periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'], key='view_periodo')

    periodo_map_label_to_num = {'1º Período': 1, '2º Período': 2}
    pnum = periodo_map_label_to_num.get(periodo)

    if pnum in (1, 2):
        materias = list(MAPA_PERIODOS[pnum].keys())
        materia = st.selectbox('Matéria', materias, key=f'view_materia_p{pnum}')
        entry = MAPA_PERIODOS[pnum].get(materia, {})
        professor = entry.get("professor")
        if professor:
            st.write(f"Professor(a): {professor}")

        key_list = entry.get("key")
        obras = st.session_state.get(key_list, []) if key_list else []
        if obras:
            st.write(f"Exibindo {len(obras)} obra(s) para *{materia}*:")
            for i, item in enumerate(obras, start=1):
                st.write(f"{i}. *{item['nome']}* — {item['autor']}")
        else:
            st.info(f"Nenhuma obra cadastrada em '{materia}'.")
    else:
        materia = st.text_input('Matéria (digite o nome da matéria)', key='view_materia_other')
        if materia:
            key_map = {'3º Período': 'periodo_3', '4º Período': 'periodo_4', '5º Período': 'periodo_5'}
            key = key_map.get(periodo, None)
            if key and key in st.session_state and materia in st.session_state[key]:
                obras = st.session_state[key][materia]
                st.write(f"Exibindo {len(obras)} obra(s) para *{materia}*:")
                for i, item in enumerate(obras, start=1):
                    st.write(f"{i}. *{item['nome']}* — {item['autor']}")
            else:
                st.info(f"Nenhuma obra cadastrada em '{materia}' para {periodo}.")

# --------------------------------------------
# Botões principais (controle de modo)
# --------------------------------------------
def _set_mode_add():
    st.session_state.mode = 'add'

def _set_mode_view():
    st.session_state.mode = 'view'

def _set_mode_stats():
    st.session_state.mode = 'stats'

st.subheader('O que você deseja fazer?')
st.button('Adicionar obra', on_click=_set_mode_add)
st.button('Ver obras', on_click=_set_mode_view)
st.button('📊 Estatísticas', on_click=_set_mode_stats)

# --------------------------------------------
# Import / Export / Limpar
# --------------------------------------------
st.write("---")
st.markdown("### Dados (import / export)")

def limpar_base_dados():
    # limpa listas fixas
    for key in LISTAS_FIXAS:
        st.session_state[key] = []
    # limpa períodos dinâmicos
    for key in PERIODOS_DINAMICOS:
        st.session_state[key] = {}
    save_db(build_persistent_db())
    st.success("✅ Base de dados limpa com sucesso!")

if st.button("🧹 Limpar Base de Dados"):
    limpar_base_dados()

# exporta
db_bytes = json.dumps(build_persistent_db(), ensure_ascii=False, indent=2).encode('utf-8')
st.download_button(label="Exportar DB (JSON)", data=db_bytes, file_name="db.json", mime="application/json")

# importa
uploaded = st.file_uploader("Importar DB (JSON) — será mesclado com os dados atuais", type=['json'])
if uploaded is not None:
    try:
        content = uploaded.read().decode('utf-8')
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            st.error("Arquivo JSON inválido: deve ser um objeto/dicionário no topo.")
        else:
            merge_db_into_session(parsed)
            save_db(build_persistent_db())
            st.success("Arquivo importado e mesclado com sucesso! (dados salvos em db.json)")
    except Exception as e:
        st.error(f"Erro ao importar arquivo: {e}")

# --------------------------------------------
# Renderiza a tela correspondente ao modo
# (stats será implementado na PARTE 3)
# --------------------------------------------
if st.session_state.mode == 'add':
    add_data()
elif st.session_state.mode == 'view':
    view_data()
elif st.session_state.mode == 'stats':
    st.header("📊 Estatísticas")
    st.info("Aguarde — função de estatísticas (gráficos e contagem) será exibida na próxima parte.")
else:
    st.info("Escolha 'Adicionar obra' ou 'Ver obras' acima para começar.")

# ============================================
#  PARTE 3 — Estatísticas, finalização e polimentos
# ============================================

def stats():
    st.header("📊 Estatísticas de Obras por Matéria")

    # monta contagem inicial a partir das listas fixas (usando os nomes exibidos do MAPA_PERIODOS)
    contagem = {}

    # preenche a partir do MAPA_PERIODOS para garantir nomes humanos consistentes
    for pnum, materias in MAPA_PERIODOS.items():
        for materia_label, info in materias.items():
            key = info["key"]
            contagem[materia_label] = len(st.session_state.get(key, []))

    # inclui períodos dinâmicos (periodo_3/4/5) — as chaves são as matérias digitadas pelo usuário
    for periodo in PERIODOS_DINAMICOS:
        materias = st.session_state.get(periodo, {})
        for materia_label, obras in materias.items():
            # Se já existir (mesma matéria em lista fixa), somamos; caso contrário criamos
            contagem[materia_label] = contagem.get(materia_label, 0) + len(obras)

    # converte em dataframe
    df = pd.DataFrame(list(contagem.items()), columns=["Matéria", "Quantidade"])
    # filtra zeros e ordena
    df = df[df["Quantidade"] > 0].sort_values(by="Quantidade", ascending=False).reset_index(drop=True)

    if df.empty:
        st.info("Ainda não há obras cadastradas para gerar estatísticas.")
        return

    # apresenta tabela e um gráfico de barras
    st.subheader("Tabela de contagem")
    st.dataframe(df)

    # Gráfico com matplotlib (detalhes de estilo mínimos para boa legibilidade)
    fig, ax = plt.subplots(figsize=(10, max(4, len(df) * 0.4)))
    ax.bar(df["Matéria"], df["Quantidade"])
    ax.set_title("Quantidade de Obras por Matéria")
    ax.set_xlabel("Matéria")
    ax.set_ylabel("Quantidade")
    ax.set_xticks(range(len(df["Matéria"])))
    ax.set_xticklabels(df["Matéria"], rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)

# Substitui placeholder de stats (caso já estivesse setado)
if st.session_state.mode == 'stats':
    stats()

# -------------------------
# Pequeno ajuste: quando trocamos de modo, garantimos rerun adequado
# -------------------------
# (Os botões já setam st.session_state.mode; a lógica acima renderiza a tela correta.)

# Mensagem final para o usuário
st.write("---")
