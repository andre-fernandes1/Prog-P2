import streamlit as st
import json
import os
import tempfile
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Mapeamento único de todas as matérias
# ----------------------------------------------------------
MAPA_MATERIAS = {
    'teoria_do_direito': {
        'nome_exibido': 'Teoria do Direito',
        'professor': 'Fernando Leal',
        'periodo': 1
    },
    'teoria_do_estado_democratico': {
        'nome_exibido': 'Teoria do Estado Democrático',
        'professor': 'Leandro Molhano',
        'periodo': 1
    },
    'pensamento_juridico_brasileiro': {
        'nome_exibido': 'Pensamento Jurídico Brasileiro',
        'professor': 'Elisa Cruz',
        'periodo': 1
    },
    'economia': {
        'nome_exibido': 'Economia',
        'professor': 'Leonardo Costa',
        'periodo': 1
    },
    'teoria_constitucional': {
        'nome_exibido': 'Teoria do Direito Constitucional',
        'professor': 'Felipe Fonte',
        'periodo': 1
    },
    'crime_sociedade': {
        'nome_exibido': 'Crime e Sociedade',
        'professor': 'Fernanda Prates / Thiago Bottino',
        'periodo': 1
    },

    # ---------- 2º Período ----------
    'sociologia_juridica': {
        'nome_exibido': 'Sociologia Jurídica',
        'professor': 'Camila Alves',
        'periodo': 2
    },
    'programacao_para_advogados': {
        'nome_exibido': 'Programação para Advogados',
        'professor': 'Josir Gomes',
        'periodo': 2
    },
    'teoria_geral_direito_civil': {
        'nome_exibido': 'Teoria Geral do Direito Civil',
        'professor': 'Filipe Medon',
        'periodo': 2
    },
    'analise_economica_direito': {
        'nome_exibido': 'Análise Econômica do Direito',
        'professor': 'Paulo Mello',
        'periodo': 2
    },
    'penas_medidas_alternativas': {
        'nome_exibido': 'Penas e Medidas Alternativas',
        'professor': 'André Mendes',
        'periodo': 2
    },
    'design_institucional': {
        'nome_exibido': 'Design Institucional',
        'professor': 'Wallace Corbo',
        'periodo': 2
    },
    'organizacao_estado_direitos_fundamentais': {
        'nome_exibido': 'Organização do Estado e Direitos Fundamentais',
        'professor': 'Álvaro / Gustavo / Guilherme',
        'periodo': 2
    }
}

# ---------- Config / DB ----------
DB_PATH = Path("db.json")  # arquivo de persistência

def load_db_raw():
    """Retorna dict carregado do arquivo (ou {}). Não altera session_state."""
    if not DB_PATH.exists():
        return {}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        st.warning(f"Não foi possível ler {DB_PATH}: {e}")
        return {}

def save_db(data: dict):
    """Salva dict em JSON de forma atômica (escreve em temp e renomeia)."""
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(dir=str(DB_PATH.parent or "."), text=True)
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmpf:
            json.dump(data, tmpf, ensure_ascii=False, indent=2)
            tmpf.flush()
            os.fsync(tmpf.fileno())
        os.replace(tmp_path, DB_PATH)
    except Exception as e:
        st.error(f"Erro ao salvar DB: {e}")

def build_persistent_db():
    db = {key: st.session_state.get(key, []) for key in MAPA_MATERIAS.keys()}

    # inclui períodos dinâmicos
    for pk in ("periodo_3","periodo_4","periodo_5"):
        if pk in st.session_state:
            db[pk] = st.session_state[pk]

    return db

def merge_db_into_session(db: dict):
    """
    Merge (extend) the loaded db dict into st.session_state.
    Lists are extended; dicts (periodo_3/4/5) are merged by extending their inner lists.
    """
    for k, v in db.items():
        if isinstance(v, list):
            if k not in st.session_state:
                st.session_state[k] = []
            st.session_state[k].extend(v)
        elif isinstance(v, dict):
            # dynamic period dict: {materia: [obra,...], ...}
            if k not in st.session_state:
                st.session_state[k] = {}
            for materia, obras in v.items():
                if materia not in st.session_state[k]:
                    st.session_state[k][materia] = []
                st.session_state[k][materia].extend(obras)
        else:
            # ignore other types
            continue

# ---------- Inicialização segura (trecho que você mandou) ----------
DB_FILE = str(DB_PATH)  # compatibilidade com nomes que você usava

# --- Constantes para inicialização e limpeza ---
LISTAS_FIXAS = list(MAPA_MATERIAS.keys())

PERIODOS_DINAMICOS = ['periodo_3', 'periodo_4', 'periodo_5']


# Inicializa variáveis vazias no session_state
def inicializar_base():
    for key in LISTAS_FIXAS:
        st.session_state.setdefault(key, [])

    for key in PERIODOS_DINAMICOS:
        st.session_state.setdefault(key, {})


# Função para limpar a base de dados
def limpar_base_dados():
    for key in LISTAS_FIXAS:
        st.session_state[key] = []

    for key in PERIODOS_DINAMICOS:
        st.session_state[key] = {}

    save_db(build_persistent_db())
    st.success("✅ Base de dados limpa com sucesso!")


# Carrega do JSON apenas uma vez
def carregar_dados():
    # usa flag para evitar duplicações entre reruns
    if st.session_state.get("dados_carregados", False):
        return
    if DB_PATH.exists():
        data = load_db_raw()
        if data:
            merge_db_into_session(data)
    st.session_state.dados_carregados = True  # 🔐 garante que não duplica

# ---- Uso no início do app ----
inicializar_base()
carregar_dados()

# ---------- Seu UI (mantido, com persistência integrada) ----------
st.set_page_config(page_title='Base de dados de Direito', layout='centered')
st.title('Base de dados de Direito 📚')
st.subheader('Escola de Direito - FGV Direito Rio')

# flag de modo (mantém compatibilidade com seu fluxo)
if 'mode' not in st.session_state:
    st.session_state.mode = None

# -----------------------
# Função add_data com periodo FORA do form e leitura segura no submit
def add_data():
    st.header('Adicionar obra')
    st.write('Aqui você pode adicionar novas obras à base de dados de Direito.')

    # garante chave de período anterior para detectar mudança
    if "add_periodo_prev" not in st.session_state:
        st.session_state.add_periodo_prev = None

    # *** Período fora do form (conforme solicitado) ***
    periodo = st.selectbox('Período', [
        '1º Período', '2º Período', '3º Período', '4º Período', '5º Período'
    ], key="add_periodo")

    # Se o período mudou, removemos keys antigas de matéria para evitar reaproveitamento de estado
    if st.session_state.add_periodo_prev != st.session_state.add_periodo:
        for k in ("add_materia_p1", "add_materia_p2", "add_materia_other"):
            if k in st.session_state:
                del st.session_state[k]
        # atualiza a marca
        st.session_state.add_periodo_prev = st.session_state.add_periodo

    # --- Form com nome e autor (materia é criada condicionalmente dentro do form) ---
    with st.form("form_adicionar_obra"):
        nome = st.text_input('Nome da obra', key="add_nome")
        autor = st.text_input('Autor', key="add_autor")

        # Criamos o widget de matéria correspondente ao periodo selecionado (chaves distintas)
        if periodo == '1º Período':
            _ = st.selectbox('Matéria', [
                'Teoria do Direito', 'Teoria do Estado Democrático',
                'Pensamento Jurídico Brasileiro', 'Economia',
                'Teoria do Direito Constitucional', 'Crime e Sociedade'
            ], key="add_materia_p1")
        elif periodo == '2º Período':
            _ = st.selectbox('Matéria', [
                'Sociologia Jurídica', 'Programação para Advogados',
                'Teoria Geral do Direito Civil', 'Análise Econômica do Direito',
                'Penas e Medidas Alternativas', 'Design Institucional',
                'Organização do Estado e Direitos Fundamentais'
            ], key="add_materia_p2")
        else:
            _ = st.text_input('Matéria (digite o nome da matéria)', key="add_materia_other")

        submitted = st.form_submit_button('Adicionar')

        if submitted:
            # Leitura segura dos campos do session_state (periodo está fora do form)
            nome_val = st.session_state.get("add_nome", "").strip()
            autor_val = st.session_state.get("add_autor", "").strip()
            periodo_val = st.session_state.get("add_periodo", "").strip()

            # Lê matéria com prioridade para p1, p2, other (garante consistência)
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
                # Inserção robusta usando periodo_val lido fora do form
                # ---- aqui usamos um mapeamento para reduzir if/elif
                # Busca automática da chave baseada no nome exibido
                key = None
                for k, info in MAPA_MATERIAS.items():
                    if info["nome_exibido"] == materia_val and info["periodo"] == int(periodo_val[0]):
                        key = k
                        break

                if periodo_val in mapa_local:
                    key = mapa_local[periodo_val].get(materia_val)
                    if key:
                        # garante que a lista existe
                        if key not in st.session_state:
                            st.session_state[key] = []
                        st.session_state[key].append({'nome': nome_val, 'autor': autor_val})
                        where_inserted = key
                    else:
                        # fallback: se materia não estiver mapeada, adiciona numa lista padrão do período
                        if periodo_val == '1º Período':
                            st.session_state.teoria_do_direito.append({'nome': nome_val, 'autor': autor_val})
                            where_inserted = 'teoria_do_direito'
                        elif periodo_val == '2º Período':
                            st.session_state.programacao_para_advogados.append({'nome': nome_val, 'autor': autor_val})
                            where_inserted = 'programacao_para_advogados'
                        else:
                            where_inserted = 'periodo_outros'
                else:
                    # períodos 3/4/5: guarda em dict dinamico
                    key_map = {
                        '3º Período': 'periodo_3',
                        '4º Período': 'periodo_4',
                        '5º Período': 'periodo_5'
                    }
                    key = key_map.get(periodo_val, 'periodo_outros')
                    if key not in st.session_state:
                        st.session_state[key] = {}
                    if materia_val not in st.session_state[key]:
                        st.session_state[key][materia_val] = []
                    st.session_state[key][materia_val].append({'nome': nome_val, 'autor': autor_val})
                    where_inserted = f"{key}:{materia_val}"

                # SALVA O DB EM DISCO (JSON)
                save_db(build_persistent_db())

                # Limpeza opcional após submit (limpa campos do form)
                for k in ("add_nome", "add_autor", "add_materia_p1", "add_materia_p2", "add_materia_other"):
                    if k in st.session_state:
                        del st.session_state[k]

                st.success(f'Obra {nome_val}, de {autor_val}, adicionada com sucesso! (salva em {where_inserted})')

# -----------------------
# Função view_data (mantida, mas com acesso seguro via st.session_state.get)
def view_data():
    st.header('Ver obras')
    st.write('Aqui você pode ver as obras na base de dados de Direito.')
    periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'], key='view_periodo')
    if periodo == '1º Período':
        materia = st.selectbox('Matéria', ['Teoria do Direito', 'Teoria do Estado Democrático',
                                          'Pensamento Jurídico Brasileiro', 'Economia',
                                          'Teoria do Direito Constitucional', 'Crime e Sociedade'],
                               key='view_materia_p1')
        for key, info in MAPA_MATERIAS.items():
          if info["nome_exibido"] == materia and info["periodo"] == int(periodo[0]):
            st.write(f"Professor: {info['professor']}")
            obras = st.session_state.get(key, [])


# Botões principais (mantidos no fim como no seu código)
st.subheader('O que você deseja fazer?')

def _set_mode_add():
    st.session_state.mode = 'add'

def _set_mode_view():
    st.session_state.mode = 'view'

def _set_mode_stats():
    st.session_state.mode = 'stats'

st.button('Adicionar obra', on_click=_set_mode_add)
st.button('Ver obras', on_click=_set_mode_view)
st.button('📊 Estatísticas', on_click=lambda: stats())

# ---------- Exportar / Importar JSON (botões solicitados) ----------
st.write("---")
st.markdown("### Dados (import / export)")

if st.button("🧹 Limpar Base de Dados"):
    limpar_base_dados()

# Exporta o JSON atual (constroi a representação atual do DB)
db_bytes = json.dumps(build_persistent_db(), ensure_ascii=False, indent=2).encode('utf-8')
st.download_button(label="Exportar DB (JSON)", data=db_bytes, file_name="db.json", mime="application/json")

# Importa um JSON e faz merge/extend
uploaded = st.file_uploader("Importar DB (JSON) — será *mesclado* com os dados atuais", type=['json'])
if uploaded is not None:
    try:
        content = uploaded.read().decode('utf-8')
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            st.error("Arquivo JSON inválido: deve ser um objeto/dicionário no topo.")
        else:
            # faz merge into session (extend)
            merge_db_into_session(parsed)
            save_db(build_persistent_db())
            st.success("Arquivo importado e mesclado com sucesso! (dados salvos em db.json)")
    except Exception as e:
        st.error(f"Erro ao importar arquivo: {e}")

def stats():
    st.header("📊 Estatísticas de Obras por Matéria")

    # Monta o contador
    contagem = {}

    for key, info in MAPA_MATERIAS.items():
        contagem[info["nome_exibido"]] = len(st.session_state.get(key, []))


    # Períodos dinâmicos
    for periodo in ['periodo_3', 'periodo_4', 'periodo_5']:
        materias = st.session_state.get(periodo, {})
        for materia, obras in materias.items():
            contagem[materia] = len(obras)

    # Transforma em dataframe
    df = pd.DataFrame(list(contagem.items()), columns=["Matéria", "Quantidade"])
    df = df[df["Quantidade"] > 0].sort_values(by="Quantidade", ascending=False)

    if df.empty:
        st.info("Ainda não há obras cadastradas para gerar estatísticas.")
        return

    st.dataframe(df)

    # Plot
    fig, ax = plt.subplots()
    ax.bar(df["Matéria"], df["Quantidade"])
    ax.set_title("Quantidade de Obras por Matéria")
    ax.set_xticklabels(df["Matéria"], rotation=45, ha="right")

    st.pyplot(fig)


# Renderiza a tela correspondente com base na flag persistente
if st.session_state.mode == 'add':
    add_data()
elif st.session_state.mode == 'view':
    view_data()
elif st.session_state.mode == 'stats':
    stats()
else:
    st.info("Escolha 'Adicionar obra' ou 'Ver obras' acima para começar.")

