import streamlit as st

st.set_page_config(page_title='Base de dados de Direito', layout='centered')
st.title('Base de dados')

# -----------------------
# Inicializa as listas na sessão, se ainda não existirem
# (mantive sua estrutura de nomes)
# Período 1
if 'teoria_do_direito' not in st.session_state:
    st.session_state.teoria_do_direito = []
if 'teoria_do_estado_democratico' not in st.session_state:
    st.session_state.teoria_do_estado_democratico = []
if 'pensamento_juridico_brasileiro' not in st.session_state:
    st.session_state.pensamento_juridico_brasileiro = []
if 'economia' not in st.session_state:
    st.session_state.economia = []
if 'teoria_constitucional' not in st.session_state:
    st.session_state.teoria_constitucional = []
if 'crime_sociedade' not in st.session_state:
    st.session_state.crime_sociedade = []
 
# Período 2
if 'sociologia_juridica' not in st.session_state:
    st.session_state.sociologia_juridica = []
if 'programacao_para_advogados' not in st.session_state:
    st.session_state.programacao_para_advogados = []
if 'teoria_geral_direito_civil' not in st.session_state:
    st.session_state.teoria_geral_direito_civil = []
if 'analise_economica_direito' not in st.session_state:
    st.session_state.analise_economica_direito = []
if 'penas_medidas_alternativas' not in st.session_state:
    st.session_state.penas_medidas_alternativas = []
if 'design_institucional' not in st.session_state:
    st.session_state.design_institucional = []
if 'organizacao_estado_direitos_fundamentais' not in st.session_state:
    st.session_state.organizacao_estado_direitos_fundamentais = []

# -----------------------
# Mínima adição: flag para manter o modo entre reruns
if 'mode' not in st.session_state:
    st.session_state.mode = None  # valores possíveis: None, 'add', 'view'

# -----------------------
# Funções de UI (mantive nomes e estrutura)
def add_data():
    st.header('Adicionar obra')
    st.write('Aqui você pode adicionar novas obras à base de dados de Direito.')

    # --- selectbox de período FORA do form para controlar o fluxo
    periodo = st.selectbox('Período', [
        '1º Período', '2º Período', '3º Período', '4º Período', '5º Período'
    ], key="add_periodo")

    # Marca o período anterior para detectar mudança
    if "add_periodo_prev" not in st.session_state:
        st.session_state.add_periodo_prev = None

    # Se o período mudou desde o último rerun, limpar os keys das matérias
    if st.session_state.add_periodo_prev != st.session_state.add_periodo:
        for k in ("add_materia_p1", "add_materia_p2", "add_materia_other", "add_nome", "add_autor"):
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.add_periodo_prev = st.session_state.add_periodo

    # --- agora o form com os inputs que só serão submetidos quando o usuário clicar em "Adicionar"
    with st.form("form_adicionar_obra"):
        nome = st.text_input('Nome da obra', key="add_nome")
        autor = st.text_input('Autor', key="add_autor")

        # Escolhe matérias conforme o período (cada widget tem chave distinta)
        if periodo == '1º Período':
            materia = st.selectbox('Matéria', [
                'Teoria do Direito', 'Teoria do Estado Democrático',
                'Pensamento Jurídico Brasileiro', 'Economia',
                'Teoria do Direito Constitucional', 'Crime e Sociedade'
            ], key="add_materia_p1")
        elif periodo == '2º Período':
            materia = st.selectbox('Matéria', [
                'Sociologia Jurídica', 'Programação para Advogados',
                'Teoria Geral do Direito Civil', 'Análise Econômica do Direito',
                'Penas e Medidas Alternativas', 'Design Institucional',
                'Organização do Estado e Direitos Fundamentais'
            ], key="add_materia_p2")
        else:
            materia = st.text_input('Matéria (digite o nome da matéria)', key="add_materia_other")

        submitted = st.form_submit_button('Adicionar')

        if submitted:
            nome_val = st.session_state.get("add_nome", "").strip()
            autor_val = st.session_state.get("add_autor", "").strip()
            materia_val = materia.strip() if isinstance(materia, str) else materia

            if not nome_val or not autor_val or not materia_val:
                st.warning("Preencha 'Nome', 'Autor' e 'Matéria' antes de adicionar.")
            else:
                # Apêndices mantidos igual ao seu código original
                if periodo == '1º Período':
                    if materia_val == 'Teoria do Direito':
                        st.session_state.teoria_do_direito.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Organização do Estado e Direitos Fundamentais':
                        st.session_state.organizacao_estado_direitos_fundamentais.append({'nome': nome_val, 'autor': autor_val})
                    else:
                        st.session_state.programacao_para_advogados.append({'nome': nome_val, 'autor': autor_val})
                else:
                    # Para períodos 3/4/5: cria uma lista nova na sessão dinamicamente
                    key_map = {
                        '3º Período': 'periodo_3',
                        '4º Período': 'periodo_4',
                        '5º Período': 'periodo_5'
                    }
                    key = key_map.get(periodo, 'periodo_outros')
                    if key not in st.session_state:
                        st.session_state[key] = {}
                    if materia_val not in st.session_state[key]:
                        st.session_state[key][materia_val] = []
                    st.session_state[key][materia_val].append({'nome': nome_val, 'autor': autor_val})

                st.success(f'Obra {nome_val}, de {autor_val}, adicionada com sucesso!')



def view_data():
    st.header('Ver obras')
    st.write('Aqui você pode ver as obras na base de dados de Direito.')

    # select do período com key fixa
    periodo = st.selectbox(
        'Período',
        ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'],
        key='view_periodo'
    )

    # Para 1º e 2º período usamos selectboxes com keys distintas
    if periodo == '1º Período':
        materia = st.selectbox('Matéria', [
            'Teoria do Direito', 'Teoria do Estado Democrático',
            'Pensamento Jurídico Brasileiro', 'Economia',
            'Teoria do Direito Constitucional', 'Crime e Sociedade'
        ], key='view_materia_p1')

        # Mapear matéria para a lista correta e mostrar conteúdos com segurança
        map_p1 = {
            'Teoria do Direito': 'teoria_do_direito',
            'Teoria do Estado Democrático': 'teoria_do_estado_democratico',
            'Pensamento Jurídico Brasileiro': 'pensamento_juridico_brasileiro',
            'Economia': 'economia',
            'Teoria do Direito Constitucional': 'teoria_constitucional',
            'Crime e Sociedade': 'crime_sociedade'
        }
        key_list = map_p1.get(materia)
        if key_list and key_list in st.session_state:
            obras = st.session_state[key_list]
            if obras:
                st.write(f"Exibindo {len(obras)} obra(s) para {materia}:")
                for i, item in enumerate(obras, start=1):
                    st.write(f"{i}. **{item['nome']}** — {item['autor']}")
            else:
                st.info(f"Nenhuma obra cadastrada em '{materia}'. (lista vazia)")
        else:
            st.info("Nenhuma obra encontrada para essa matéria.")

    elif periodo == '2º Período':
        materia = st.selectbox('Matéria', [
            'Sociologia Jurídica', 'Programação para Advogados',
            'Teoria Geral do Direito Civil', 'Análise Econômica do Direito',
            'Penas e Medidas Alternativas', 'Design Institucional',
            'Organização do Estado e Direitos Fundamentais'
        ], key='view_materia_p2')

        map_p2 = {
            'Sociologia Jurídica': 'sociologia_juridica',
            'Programação para Advogados': 'programacao_para_advogados',
            'Teoria Geral do Direito Civil': 'teoria_geral_direito_civil',
            'Análise Econômica do Direito': 'analise_economica_direito',
            'Penas e Medidas Alternativas': 'penas_medidas_alternativas',
            'Design Institucional': 'design_institucional',
            'Organização do Estado e Direitos Fundamentais': 'organizacao_estado_direitos_fundamentais'
        }
        key_list = map_p2.get(materia)
        if key_list and key_list in st.session_state:
            obras = st.session_state[key_list]
            if obras:
                st.write(f"Exibindo {len(obras)} obra(s) para {materia}:")
                for i, item in enumerate(obras, start=1):
                    st.write(f"{i}. **{item['nome']}** — {item['autor']}")
            else:
                st.info(f"Nenhuma obra cadastrada em '{materia}'. (lista vazia)")
        else:
            st.info("Nenhuma obra encontrada para essa matéria.")

    else:
        # períodos 3/4/5 — input livre com key própria
        materia = st.text_input('Matéria (digite o nome da matéria)', key='view_materia_other')
        if materia:
            key_map = {'3º Período': 'periodo_3', '4º Período': 'periodo_4', '5º Período': 'periodo_5'}
            key = key_map.get(periodo, None)
            if key and key in st.session_state and materia in st.session_state[key]:
                obras = st.session_state[key][materia]
                if obras:
                    st.write(f'Exibindo {len(obras)} obra(s) para {materia} em {periodo}:')
                    for i, item in enumerate(obras, start=1):
                        st.write(f"{i}. **{item['nome']}** — {item['autor']}")
                else:
                    st.info("Nenhuma obra encontrada para essa matéria neste período.")
            else:
                st.info("Nenhuma obra encontrada para essa matéria neste período.")

    # --- debug auxiliar (remova depois) ---
    # mostra rapidamente quantos itens existem em cada lista para diagnosticar
    if st.checkbox("Mostrar contagem das listas (debug)", key="debug_counts"):
        st.write("Contagem das listas salvas na sessão:")
        keys = [
            'teoria_do_direito','teoria_do_estado_democratico','pensamento_juridico_brasileiro',
            'economia','teoria_constitucional','crime_sociedade',
            'sociologia_juridica','programacao_para_advogados','teoria_geral_direito_civil',
            'analise_economica_direito','penas_medidas_alternativas','design_institucional',
            'organizacao_estado_direitos_fundamentais'
        ]
        for k in keys:
            st.write(f"{k}: {len(st.session_state.get(k, []))}")
        # checa periodos dinamicos
        for pk in ("periodo_3","periodo_4","periodo_5"):
            if pk in st.session_state:
                st.write(f"{pk}: { {m: len(lst) for m, lst in st.session_state[pk].items()} }")


# -----------------------
# Botões principais (mantidos no fim como no seu código)
st.subheader('O que você deseja fazer?')

# Pequenas funções apenas para setar o modo — mínima mudança para preservar estrutura
def _set_mode_add():
    st.session_state.mode = 'add'

def _set_mode_view():
    st.session_state.mode = 'view'

st.button('Adicionar obra', on_click=_set_mode_add)
st.button('Ver obras', on_click=_set_mode_view)

# Renderiza a tela correspondente com base na flag persistente
if st.session_state.mode == 'add':
    add_data()
elif st.session_state.mode == 'view':
    view_data()
else:
    st.info("Escolha 'Adicionar obra' ou 'Ver obras' acima para começar.")

