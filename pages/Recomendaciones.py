"""
Página de Consulta de Recomendaciones (RAG con TF-IDF)
"""
import streamlit as st
import os
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

st.set_page_config(page_title="Recomendaciones", page_icon="📚", layout="wide")

st.title("📚 Consulta de Recomendaciones")
st.markdown("**Haz preguntas sobre el documento de recomendaciones usando IA**")

# ============================================================================
# FUNCIONES PARA RAG CON TF-IDF
# ============================================================================

@st.cache_resource
def cargar_pdf(ruta_pdf: str) -> str:
    """Carga y extrae texto de un PDF"""
    try:
        import pypdf
        
        with open(ruta_pdf, 'rb') as archivo:
            lector = pypdf.PdfReader(archivo)
            texto_completo = ""
            for pagina in lector.pages:
                texto_completo += pagina.extract_text() + "\n"
        
        return texto_completo
    except ImportError:
        st.error("❌ Falta la librería pypdf. Instálala con: pip install pypdf")
        return None
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo: {ruta_pdf}")
        return None
    except Exception as e:
        st.error(f"❌ Error al leer el PDF: {str(e)}")
        return None


def dividir_en_chunks(texto: str, tamano_chunk: int = 500, solapamiento: int = 100) -> list:
    """Divide el texto en chunks con solapamiento"""
    if not texto:
        return []
    
    # Limpiar texto
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    palabras = texto.split()
    chunks = []
    
    i = 0
    while i < len(palabras):
        chunk = ' '.join(palabras[i:i + tamano_chunk])
        chunks.append(chunk)
        i += tamano_chunk - solapamiento
    
    return chunks


class RAGSimple:
    """Sistema RAG simple usando TF-IDF"""
    
    def __init__(self, chunks: list):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),  # Unigramas y bigramas
            max_df=0.95,
            min_df=1,
            stop_words=None  # Mantener stopwords en español
        )
        
        # Crear matriz TF-IDF de los chunks
        self.tfidf_matrix = self.vectorizer.fit_transform(chunks)
    
    def buscar(self, query: str, top_k: int = 3) -> list:
        """Busca los chunks más relevantes para una consulta"""
        # Vectorizar la consulta
        query_vector = self.vectorizer.transform([query])
        
        # Calcular similitud coseno
        similitudes = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Obtener los top_k índices más similares
        indices_top = similitudes.argsort()[-top_k:][::-1]
        
        resultados = []
        for idx in indices_top:
            if similitudes[idx] > 0:  # Solo incluir si hay alguna similitud
                resultados.append({
                    'chunk': self.chunks[idx],
                    'similitud': similitudes[idx],
                    'indice': idx
                })
        
        return resultados
    
    def generar_respuesta(self, query: str, top_k: int = 3) -> dict:
        """Genera una respuesta basada en los chunks relevantes"""
        resultados = self.buscar(query, top_k)
        
        if not resultados:
            return {
                'respuesta': "No encontré información relevante en el documento para tu pregunta.",
                'contextos': [],
                'confianza': 0
            }
        
        # Combinar contextos relevantes
        contextos = [r['chunk'] for r in resultados]
        confianza_promedio = np.mean([r['similitud'] for r in resultados])
        
        # Construir respuesta
        contexto_combinado = "\n\n".join(contextos)
        
        # Respuesta simple: mostrar el contexto más relevante
        if confianza_promedio > 0.3:
            respuesta = f"Basándome en el documento, encontré la siguiente información relevante:\n\n{contextos[0]}"
        elif confianza_promedio > 0.1:
            respuesta = f"Encontré información que podría estar relacionada con tu pregunta:\n\n{contextos[0]}"
        else:
            respuesta = "La información encontrada tiene baja relevancia. Te muestro lo más cercano a tu consulta:\n\n" + contextos[0]
        
        return {
            'respuesta': respuesta,
            'contextos': resultados,
            'confianza': confianza_promedio
        }


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

# Ruta del PDF (en la raíz del proyecto)
RUTA_PDF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "recomendaciones.pdf")

# Verificar si existe el archivo
if not os.path.exists(RUTA_PDF):
    st.warning(f"⚠️ No se encontró el archivo `recomendaciones.pdf` en la raíz del proyecto.")
    st.info(f"📁 Ruta esperada: `{RUTA_PDF}`")
    st.markdown("""
    ### 📋 Instrucciones:
    1. Coloca un archivo llamado `recomendaciones.pdf` en la carpeta raíz del proyecto
    2. Recarga la página
    """)
    st.stop()

# Cargar y procesar el PDF
with st.spinner("📄 Cargando documento..."):
    texto_pdf = cargar_pdf(RUTA_PDF)

if texto_pdf is None:
    st.stop()

# Dividir en chunks
chunks = dividir_en_chunks(texto_pdf, tamano_chunk=300, solapamiento=50)

if not chunks:
    st.error("❌ No se pudo extraer texto del PDF")
    st.stop()

# Crear sistema RAG
@st.cache_resource
def crear_rag(_chunks):
    return RAGSimple(_chunks)

rag = crear_rag(chunks)

# ============================================================================
# INTERFAZ
# ============================================================================

st.success(f"✅ Documento cargado: {len(chunks)} secciones indexadas")

# Información del documento
with st.expander("ℹ️ Información del documento"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Caracteres", f"{len(texto_pdf):,}")
    with col2:
        st.metric("📚 Secciones", len(chunks))
    with col3:
        st.metric("📝 Palabras aprox.", f"{len(texto_pdf.split()):,}")

st.divider()

# Inicializar historial de chat
if 'chat_history_rag' not in st.session_state:
    st.session_state.chat_history_rag = []

# Ejemplos de preguntas
st.subheader("💡 Ejemplos de preguntas:")
col1, col2 = st.columns(2)

with col1:
    if st.button("¿Cuáles son las principales recomendaciones?", use_container_width=True):
        st.session_state.pregunta_ejemplo = "¿Cuáles son las principales recomendaciones?"

with col2:
    if st.button("¿Qué metodología se utilizó?", use_container_width=True):
        st.session_state.pregunta_ejemplo = "¿Qué metodología se utilizó?"

st.divider()

# Campo de pregunta
st.subheader("❓ Haz tu pregunta sobre el documento")

# Usar formulario
with st.form(key="rag_form", clear_on_submit=True):
    # Verificar si hay pregunta de ejemplo
    valor_inicial = st.session_state.get('pregunta_ejemplo', '')
    if 'pregunta_ejemplo' in st.session_state:
        del st.session_state.pregunta_ejemplo
    
    pregunta = st.text_input(
        "Escribe tu pregunta:",
        value=valor_inicial,
        placeholder="Ej: ¿Qué recomendaciones hay para mejorar la calidad del suelo?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        enviar = st.form_submit_button("🔍 Buscar", type="primary")
    with col2:
        pass

# Botón limpiar historial
if st.button("🗑️ Limpiar historial"):
    st.session_state.chat_history_rag = []
    st.rerun()

# Procesar pregunta
if enviar and pregunta:
    with st.spinner("🔍 Buscando en el documento..."):
        resultado = rag.generar_respuesta(pregunta, top_k=3)
        
        # Guardar en historial
        st.session_state.chat_history_rag.append({
            'pregunta': pregunta,
            'respuesta': resultado['respuesta'],
            'confianza': resultado['confianza'],
            'contextos': resultado['contextos']
        })

# Mostrar historial
if st.session_state.chat_history_rag:
    st.divider()
    st.subheader("💬 Historial de consultas")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history_rag)):
        with st.expander(f"❓ {chat['pregunta'][:60]}..." if len(chat['pregunta']) > 60 else f"❓ {chat['pregunta']}", expanded=(i==0)):
            
            # Indicador de confianza
            confianza = chat['confianza']
            if confianza > 0.3:
                st.success(f"🎯 Relevancia: Alta ({confianza:.1%})")
            elif confianza > 0.1:
                st.warning(f"🎯 Relevancia: Media ({confianza:.1%})")
            else:
                st.error(f"🎯 Relevancia: Baja ({confianza:.1%})")
            
            st.markdown("**Respuesta:**")
            st.write(chat['respuesta'])
            
            # Mostrar contextos encontrados
            if chat['contextos']:
                with st.expander("📄 Ver secciones del documento utilizadas"):
                    for j, ctx in enumerate(chat['contextos'], 1):
                        st.markdown(f"**Sección {j}** (similitud: {ctx['similitud']:.1%})")
                        st.text(ctx['chunk'][:500] + "..." if len(ctx['chunk']) > 500 else ctx['chunk'])
                        st.divider()

# Información adicional
with st.expander("ℹ️ ¿Cómo funciona este sistema?"):
    st.markdown("""
    ### Sistema RAG con TF-IDF
    
    Este sistema utiliza **Recuperación Aumentada por Generación (RAG)** simplificado:
    
    1. **Indexación**: El documento PDF se divide en secciones pequeñas (chunks)
    2. **Vectorización**: Cada sección se convierte en un vector usando TF-IDF
    3. **Búsqueda**: Tu pregunta se compara con todas las secciones usando similitud coseno
    4. **Respuesta**: Se muestran las secciones más relevantes
    
    **Limitaciones:**
    - No genera texto nuevo, solo recupera secciones existentes
    - La calidad depende de cómo esté estructurado el PDF
    - Funciona mejor con preguntas que usen palabras del documento
    
    **Tips para mejores resultados:**
    - Usa palabras clave específicas del documento
    - Haz preguntas concretas
    - Si la relevancia es baja, intenta reformular la pregunta
    """)
