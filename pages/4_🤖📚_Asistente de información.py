"""
Página de RAG con PDF - Generación Aumentada por Recuperación
Usa el archivo recomendaciones.pdf de la raíz del proyecto
Compatible con LangChain 0.2.x y OpenAI 1.x
"""
import streamlit as st
import os

st.set_page_config(page_title="RAG PDF", page_icon="📄", layout="wide")

st.title("📄 Asistente de información")
st.markdown("Haz preguntas y te responderá con base en mi conocimiento.")

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

RUTA_PDF = "recomendaciones.pdf"

# ============================================================================
# CONFIGURACIÓN DE API KEY DESDE SECRETS
# ============================================================================

# Verificar si existe la API key en secrets
try:
    openai_api_key = st.secrets["settings"]["key"]
    ia_disponible = True
except:
    ia_disponible = False

if ia_disponible:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# ============================================================================
# CONFIGURACIÓN EN SIDEBAR
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuración RAG")
    
    if ia_disponible:
        st.success("🔑 Credenciales cargadas correctamente")
    else:
        st.error("❌ Error: No se encontraron las credenciales necesarias")
        st.info("💡 Configura las credenciales en los secrets de la aplicación")
    
    # Selección de modelo
    model_name = st.selectbox(
        "🤖 Modelo:",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"],
        index=0,
        help="Modelo usado para generar respuestas"
    )
    
    st.divider()
    
    # Configuración avanzada
    with st.expander("🔧 Configuración avanzada"):
        chunk_size = st.slider("Tamaño de chunks:", 200, 1500, 500, 50)
        chunk_overlap = st.slider("Overlap de chunks:", 0, 200, 50, 10)
        k_results = st.slider("Documentos a recuperar:", 1, 10, 4)
    
    st.divider()

    with st.expander("ℹ️ ¿Cómo funciona esta consulta?"):
       st.markdown("""
          Esta página usa **RAG (Retrieval-Augmented Generation)**:
    
          1. **Indexación**: El documento se divide en fragmentos y se crean embeddings vectoriales
          2. **Búsqueda**: Tu pregunta se convierte en un vector y se buscan los fragmentos (vectores) más similares
          3. **Generación**: GPT genera una respuesta basada en los fragmentos encontrados
    
          """)


# Verificar que existe el PDF
if not os.path.exists(RUTA_PDF):
    st.error(f"❌ No se encontró el archivo `{RUTA_PDF}` en la raíz del proyecto.")
    st.info("Asegúrate de que el archivo PDF esté en la misma carpeta que la aplicación.")
    st.stop()

# Verificar disponibilidad de IA
if not ia_disponible:
    st.error("❌ Asistente no disponible: credenciales no configuradas")
    st.info("💡 Contacta al administrador para configurar las credenciales del sistema")
    st.stop()


# ============================================================================
# IMPORTAR DEPENDENCIAS
# ============================================================================

try:
    from pypdf import PdfReader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_community.vectorstores import FAISS
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
except ImportError as e:
    st.error(f"❌ Error al importar dependencias: {str(e)}")
    st.info("""
    Asegúrate de tener instalados:
    - pypdf
    - langchain
    - langchain-openai
    - langchain-community
    - faiss-cpu
    """)
    st.stop()

# ============================================================================
# FUNCIONES
# ============================================================================

@st.cache_data
def extract_text_from_pdf(ruta):
    """Extrae texto del PDF."""
    try:
        pdf_reader = PdfReader(ruta)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extrayendo texto: {e}")
        return None


@st.cache_data
def create_chunks(text, chunk_size=500, chunk_overlap=50):
    """Divide el texto en chunks."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)


@st.cache_resource
def create_vector_store(_chunks, api_key, chunk_config):
    """Crea el vector store con FAISS. El _chunks evita hashing del objeto."""
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vector_store = FAISS.from_texts(list(_chunks), embeddings)
    return vector_store


def get_qa_chain(vector_store, model_name, api_key, k=4):
    """Crea la cadena de QA."""
    llm = ChatOpenAI(
        model=model_name,
        temperature=0.1,
        openai_api_key=api_key
    )
    
    prompt_template = """Eres un asistente experto que responde preguntas basándose en el documento proporcionado.
Usa el siguiente contexto para responder la pregunta del usuario.
Si no encuentras la respuesta en el contexto, di claramente que no tienes suficiente información en el documento.
Responde siempre en español de manera clara, precisa y concisa.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": k}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    
    return qa_chain


# ============================================================================
# CARGAR Y PROCESAR PDF
# ============================================================================

# Extraer texto
text = extract_text_from_pdf(RUTA_PDF)

if not text:
    st.error("❌ No se pudo extraer texto del PDF")
    st.stop()

# Crear chunks
chunks = create_chunks(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

# Crear vector store
try:
    chunk_config = f"{chunk_size}_{chunk_overlap}"
    vector_store = create_vector_store(tuple(chunks), openai_api_key, chunk_config)
    st.success(f"Asistente de información configurado ✅ Documento listo: {len(chunks)} secciones indexadas")
except Exception as e:
    st.error(f"❌ Error creando embeddings: {str(e)}")
    st.info("Verifica que la API key sea válida y tenga créditos disponibles.")
    st.stop()

# ============================================================================
# INTERFAZ DE CONSULTA
# ============================================================================

# Inicializar historial
if 'rag_chat_history' not in st.session_state:
    st.session_state.rag_chat_history = []

st.divider()

# Ejemplos de preguntas
st.subheader("💡 Ejemplos de preguntas que puedes hacer:")
col1, col2 = st.columns(2)
    
with col1:
    examples1 = [
            "Que significa un alto valor de Aluminio?",
            "¿Que hacer si tengo un ph de agua Bajo?",
            "¿Qué significa la métrica de Completitud dentro del Índice de Calidad de Datos y qué recomendación se dá cuando está baja?"
    ]
    for example in examples1:
        st.write(f"• {example}")
    
with col2:
    examples2 = [
            "¿Qué indica un Coeficiente de Variación (CV) cercano a 0 o mayor a 200% ?",
            "Qué diferencia hay entre asimetría positiva y asimetría negativa?",
            "¿Cómo se interpreta un valor muy alto de acidez KCl o aluminio intercambiable en el suelo y qué acción recomienda aplica?"
    ]
    for example in examples2:
        st.write(f"• {example}")
    
st.divider()

# Función callback para limpiar historial (evita el loop)
def limpiar_historial_rag():
    st.session_state.rag_chat_history = []

# Formulario de pregunta
st.subheader("🔍 Haz tu consulta")
with st.form(key="rag_question_form", clear_on_submit=True):
    user_question = st.text_area(
        "Escribe tu pregunta sobre el documento:",
        placeholder="Ej: ¿Cuáles son las principales recomendaciones?",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        ask_button = st.form_submit_button("🚀 Preguntar", type="primary")

# Botón limpiar historial usando callback (sin rerun manual)
st.button("🗑️ Limpiar historial", on_click=limpiar_historial_rag)

# Procesar pregunta
if ask_button and user_question.strip():
    with st.spinner("🔍 Buscando en el documento..."):
        try:
            qa_chain = get_qa_chain(
                vector_store,
                model_name,
                openai_api_key,
                k=k_results
            )
            
            result = qa_chain.invoke({"query": user_question})
            
            st.session_state.rag_chat_history.append({
                "question": user_question,
                "answer": result["result"],
                "sources": [doc.page_content[:300] + "..." for doc in result.get("source_documents", [])]
            })
            
        except Exception as e:
            st.error(f"❌ Error al procesar la pregunta: {str(e)}")
            import traceback
            with st.expander("🔧 Detalles del error"):
                st.code(traceback.format_exc())

# ============================================================================
### HISTORIAL DE CONSULTAS
# ============================================================================

if st.session_state.rag_chat_history:
    st.divider()
    st.subheader("💬 Historial de consultas")
    
    for i, chat in enumerate(reversed(st.session_state.rag_chat_history)):
        question_preview = chat['question'][:60] + "..." if len(chat['question']) > 60 else chat['question']
        
        with st.expander(f"❓ {question_preview}", expanded=(i == 0)):
            st.markdown("**Pregunta:**")
            st.write(chat['question'])
            
            st.markdown("**Respuesta:**")
            st.write(chat['answer'])
# ============================================================================
### INFORMACIÓN ADICIONAL
# ============================================================================


