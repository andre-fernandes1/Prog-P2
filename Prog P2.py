import streamlit as st

st.set_page_config(page_title='Base de dados de Direito', layout='centered')
st.title('Base de dados')

def add_data():
    with st.form(key='add_data'):
        st.header('Adicionar obra')
        st.write('Aqui você pode adicionar novas obras à base de dados de Direito.')
     # Adicione campos de entrada para os dados que você deseja coletar
        nome = st.text_input('Nome da obra')
        autor = st.text_input('Autor')
        periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'])
        if periodo == '1º Período':
            materia = st.selectbox('Matéria', ['Teoria do Direito', 'Teoria do Estado Democrático', 'Pensamento Jurídico Brasileiro', 'Economia', 'Teoria do Direito Constitucional', 'Crime e Sociedade'])
            if materia == 'Teoria do Direito':
                st.session_state.teoria_do_direito.append({'nome': nome, 'autor': autor})
            if materia == 'Teoria do Estado Democrático':
                st.session_state.teoria_do_estado_democratico.append({'nome': nome, 'autor': autor})
            if materia == 'Pensamento Jurídico Brasileiro':
                st.session_state.pensamento_juridico_brasileiro.append({'nome': nome, 'autor': autor})
            if materia == 'Economia':
                st.session_state.economia.append({'nome': nome, 'autor': autor})
            if materia == 'Teoria do Direito Constitucional':
                st.session_state.teoria_constitucional.append({'nome': nome, 'autor': autor})
            if materia == 'Crime e Sociedade':
                st.session_state.crime_sociedade.append({'nome': nome, 'autor': autor})
        elif periodo == '2º Período':
            materia = st.selectbox('Matéria', ['Sociologia Jurídica', 'Programação para Advogados', 'Teoria Geral do Direito Civil', 'Análise Econômica do Direito', 'Penas e Medidas Alternativas', 'Design Institucional', 'Organização do Estado e Direitos Fundamentais'])
            if materia == 'Sociologia Jurídica':
                st.session_state.sociologia_juridica.append({'nome': nome, 'autor': autor})
            if materia == 'Programação para Advogados':
                st.session_state.programacao_para_advogados.append({'nome': nome, 'autor': autor})
            if materia == 'Teoria Geral do Direito Civil':
                st.session_state.teoria_geral_direito_civil.append({'nome': nome, 'autor': autor})
            if materia == 'Análise Econômica do Direito':
                st.session_state.analise_economica_direito.append({'nome': nome, 'autor': autor})
            if materia == 'Penas e Medidas Alternativas':
                st.session_state.penas_medidas_alternativas.append({'nome': nome, 'autor': autor})
            if materia == 'Design Institucional':
                st.session_state.design_institucional.append({'nome': nome, 'autor': autor})
            if materia == 'Organização do Estado e Direitos Fundamentais':
                st.session_state.organizacao_estado_direitos_fundamentais.append({'nome': nome, 'autor': autor})
        if st.form_submit_button('Adicionar'):
            # Lógica para adicionar os dados à base de dados
            st.success(f'Obra {nome}, de {autor}, adicionada com sucesso!')

# Inicializa as listas na sessão, se ainda não existirem
    #Período 1
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
 
    #Período 2
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

def view_data():
        st.header('Ver obras')
        st.write('Aqui você pode ver as obras na base de dados de Direito.')
        periodo = st.selectbox('Período', ['1º Período', '2º Período', '3º Período', '4º Período', '5º Período'])
        if periodo == '1º Período':
            materia = st.selectbox('Matéria', ['Teoria do Direito', 'Teoria do Estado Democrático', 'Pensamento Jurídico Brasileiro', 'Economia', 'Teoria do Direito Constitucional', 'Crime e Sociedade'])
            if materia == 'Teoria do Direito':
                st.write('Exibindo obras para Teoria do Direito')
                for item in st.session_state.teoria_do_direito:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Teoria do Estado Democrático':
                st.write('Exibindo obras para Teoria do Estado Democrático')
                for item in st.session_state.teoria_do_estado_democratico:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Pensamento Jurídico Brasileiro':
                st.write('Exibindo obras para Pensamento Jurídico Brasileiro')
                for item in st.session_state.pensamento_juridico_brasileiro:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Economia':
                st.write('Exibindo obras para Economia')
                for item in st.session_state.economia:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Teoria do Direito Constitucional':
                st.write('Exibindo obras para Teoria do Direito Constitucional')
                for item in st.session_state.teoria_constitucional:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Crime e Sociedade':
                st.write('Exibindo obras para Crime e Sociedade')
                for item in st.session_state.crime_sociedade:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
        
        elif periodo == '2º Período':
            materia = st.selectbox('Matéria', ['Sociologia Jurídica', 'Programação para Advogados', 'Teoria Geral do Direito Civil', 'Análise Econômica do Direito', 'Penas e Medidas Alternativas', 'Design Institucional', 'Organização do Estado e Direitos Fundamentais'])
            if materia == 'Sociologia Jurídica':
                st.write('Exibindo obras para Sociologia Jurídica')
                for item in st.session_state.sociologia_juridica:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Programação para Advogados':
                st.write('Exibindo obras para Programação para Advogados')
                for item in st.session_state.programacao_para_advogados:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Teoria Geral do Direito Civil':
                st.write('Exibindo obras para Teoria Geral do Direito Civil')
                for item in st.session_state.teoria_geral_direito_civil:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Análise Econômica do Direito':
                st.write('Exibindo obras para Análise Econômica do Direito')
                for item in st.session_state.analise_economica_direito:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Penas e Medidas Alternativas':
                st.write('Exibindo obras para Penas e Medidas Alternativas')
                for item in st.session_state.penas_medidas_alternativas:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Design Institucional':
                st.write('Exibindo obras para Design Institucional')
                for item in st.session_state.design_institucional:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")
            elif materia == 'Organização do Estado e Direitos Fundamentais':
                st.write('Exibindo obras para Organização do Estado e Direitos Fundamentais')
                for item in st.session_state.organizacao_estado_direitos_fundamentais:
                    st.write(f"Nome: {item['nome']}, Autor: {item['autor']}")

st.subheader('O que você deseja fazer?')
st.button('Adicionar obra', on_click=add_data)
st.button('Ver obras', on_click=view_data)

