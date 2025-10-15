import streamlit as st

st.set_page_config(page_title='Base de dados de Direito', layout='centered')
st.title('Base de dados de Direito 📚')
st.subheader('Escola de Direito - FGV Direito Rio')

# -----------------------
# Inicializa as listas na sessão, se ainda não existirem
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
                if periodo_val == '1º Período':
                    if materia_val == 'Teoria do Direito':
                        st.session_state.teoria_do_direito.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Teoria do Estado Democrático':
                        st.session_state.teoria_do_estado_democratico.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Pensamento Jurídico Brasileiro':
                        st.session_state.pensamento_juridico_brasileiro.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Economia':
                        st.session_state.economia.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Teoria do Direito Constitucional':
                        st.session_state.teoria_constitucional.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Crime e Sociedade':
                        st.session_state.crime_sociedade.append({'nome': nome_val, 'autor': autor_val})
                    else:
                        st.session_state.teoria_do_direito.append({'nome': nome_val, 'autor': autor_val})
                elif periodo_val == '2º Período':
                    if materia_val == 'Sociologia Jurídica':
                        st.session_state.sociologia_juridica.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Programação para Advogados':
                        st.session_state.programacao_para_advogados.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Teoria Geral do Direito Civil':
                        st.session_state.teoria_geral_direito_civil.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Análise Econômica do Direito':
                        st.session_state.analise_economica_direito.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Penas e Medidas Alternativas':
                        st.session_state.penas_medidas_alternativas.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Design Institucional':
                        st.session_state.design_institucional.append({'nome': nome_val, 'autor': autor_val})
                    elif materia_val == 'Organização do Estado e Direitos Fundamentais':
                        st.session_state.organizacao_estado_direitos_fundamentais.append({'nome': nome_val, 'autor': autor_val})
                    else:
                        st.session_state.programacao_para_advogados.append({'nome': nome_val, 'autor': autor_val})
                else:
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

                # Limpeza opcional após submit (limpa campos do form)
                for k in ("add_nome", "add_autor", "add_materia_p1", "add_materia_p2", "add_materia_other"):
                    if k in st.session_state:
                        del st.session_state[k]

                st.success(f'Obra {nome_val}, de {autor_val}, adicionada com sucesso!')

# -----------------------
# Função view_data (mantida, mas recomendo usar a versão com keys que te enviei antes)
def view_data():
    st.header('Ver obras')
    st.write('Aqui você pode ver as obras na base de dados de Direito.')
    periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'], key='view_periodo')
    if periodo == '1º Período':
        materia = st.selectbox('Matéria', ['Teoria do Direito', 'Teoria do Estado Democrático',
                                          'Pensamento Jurídico Brasileiro', 'Economia',
                                          'Teoria do Direito Constitucional', 'Crime e Sociedade'],
                               key='view_materia_p1')
        if materia == 'Teoria do Direito':
            for item in st.session_state.teoria_do_direito:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Teoria do Estado Democrático':
            for item in st.session_state.teoria_do_estado_democratico:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Pensamento Jurídico Brasileiro':
            for item in st.session_state.pensamento_juridico_brasileiro:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Economia':
            for item in st.session_state.economia:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Teoria do Direito Constitucional':
            for item in st.session_state.teoria_constitucional:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Crime e Sociedade':
            for item in st.session_state.crime_sociedade:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        
    elif periodo == '2º Período':
        materia = st.selectbox('Matéria', ['Sociologia Jurídica', 'Programação para Advogados',
                                          'Teoria Geral do Direito Civil', 'Análise Econômica do Direito',
                                          'Penas e Medidas Alternativas', 'Design Institucional',
                                          'Organização do Estado e Direitos Fundamentais'],
                               key='view_materia_p2')
        if materia == 'Sociologia Jurídica':
            for item in st.session_state.sociologia_juridica:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Programação para Advogados':
            for item in st.session_state.programacao_para_advogados:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Teoria Geral do Direito Civil':
            for item in st.session_state.teoria_geral_direito_civil:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Análise Econômica do Direito':
            for item in st.session_state.analise_economica_direito:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Penas e Medidas Alternativas':
            for item in st.session_state.penas_medidas_alternativas:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Design Institucional':
            for item in st.session_state.design_institucional:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        elif materia == 'Organização do Estado e Direitos Fundamentais':
            for item in st.session_state.organizacao_estado_direitos_fundamentais:
                st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
    else:
        materia = st.text_input('Matéria (digite o nome da matéria)', key='view_materia_other')
        if materia:
            key_map = {'3º Período': 'periodo_3', '4º Período': 'periodo_4', '5º Período': 'periodo_5'}
            key = key_map.get(periodo, None)
            if key and key in st.session_state and materia in st.session_state[key]:
                for item in st.session_state[key][materia]:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")

# -----------------------
# Botões principais (mantidos no fim como no seu código)
st.subheader('O que você deseja fazer?')

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
