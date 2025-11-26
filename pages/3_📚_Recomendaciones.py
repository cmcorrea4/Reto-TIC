"""
RAG Optimizado con TF-IDF (Preciso, conciso, sin expanders anidados)
"""
import streamlit as st
import os
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ================================================================
# CONFIGURACIÓN
# ================================================================

st.set_page_config(page_title="Recomendaciones", page_icon="📘", layout="wide")
st.title("📘 Consulta Inteligente (RAG Optimizado)")
st.markdown("Haz preguntas y obtén **conceptos clave + frase relevante** del documento.")


# ================================================================
# UTILIDADES
# ================================================================

@st.cache_resource
def cargar_pdf(ruta):
    """Carga texto desde un PDF con pypdf."""
    import pypdf

    try:
        reader = pypdf.PdfReader(open(ruta, "rb"))
        texto = "\n".join([p.extract_text() or "" for p in reader.pages])
        return texto
    except Exception as e:
        st.error(f"Error cargando PDF: {e}")
        return ""


def dividir_en_chunks(texto, tam=80, sol=20):
    """Divide en chunks pequeños para mayor precisión."""
    texto = re.sub(r"\s+", " ", texto)
    palabras = texto.split()

    chunks = []
    i = 0
    while i < len(palabras):
        chunk = " ".join(palabras[i:i+tam])
        chunks.append(chunk)
        i += tam - sol
    
    return chunks


# ================================================================
# RAG Optimizado
# ================================================================

class RAG_TFIDF:
    def __init__(self, chunks):
        self.chunks = chunks

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1,1),      # Mejor precisión en documentos cortos
            stop_words="spanish",   # Elimina ruido
            max_features=2000       # Compacto y eficiente
        )

        self.matrix = self.vectorizer.fit_transform(chunks)
        self.vocab = np.array(self.vectorizer.get_feature_names_out())

    def _conceptos_clave(self, texto, top=6):
        """Extrae conceptos clave del chunk."""
        tfidf_vals = self.vectorizer.transform([texto]).toarray()[0]
        idx = tfidf_vals.argsort()[::-1][:top]
        palabras = self.vocab[idx]
        return ", ".join(palabras)

    def _frase_relevante(self, chunk, conceptos):
        """Obtiene solo la frase más relevante en lugar de todo el chunk."""
        frases = re.split(r"[.!?]", chunk)
        conceptos_lista = [c.strip().lower() for c in conceptos.split(",")]

        for palabra in conceptos_lista:
            for f in frases:
                if palabra in f.lower():
                    return f.strip()

        return chunk[:180]  # fallback mínimo

    def buscar(self, query, k=3):
        """Recupera chunk relevante."""
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).flatten()

        idx = sims.argsort()[-k:][::-1]
        resultados = [(i, sims[i]) for i in idx if sims[i] > 0]
        return resultados

    def responder(self, query):
        encontrados = self.buscar(query)

        if not encontrados:
            return {
                "respuesta": "No encontré información relevante en el documento.",
                "conceptos": [],
                "confianza": 0,
                "chunks": []
            }

        # Tomar el chunk más relevante
        idx, sim = encontrados[0]
        chunk = self.chunks[idx]

        conceptos = self._conceptos_clave(chunk)
        frase = self._frase_relevante(chunk, conceptos)

        return {
            "respuesta": frase,
            "conceptos": conceptos,
            "confianza": float(sim),
            "chunks": encontrados
        }


# ================================================================
# CARGAR PDF
# ================================================================

RUTA_PDF = "recomendaciones.pdf"

if not os.path.exists(RUTA_PDF):
    st.error("No se encontró recomendaciones.pdf")
    st.stop()

texto = cargar_pdf(RUTA_PDF)
chunks = dividir_en_chunks(texto, tam=80, sol=20)

rag = RAG_TFIDF(chunks)

st.success(f"Documento listo: {len(chunks)} secciones indexadas")


# ================================================================
# UI DE CONSULTA
# ================================================================

if "historial" not in st.session_state:
    st.session_state.historial = []

st.divider()
st.subheader("🔍 Haz tu consulta")

query = st.text_input("Pregunta:")

if st.button("Buscar", type="primary"):
    if query.strip():
        resultado = rag.responder(query)

        st.session_state.historial.append({
            "pregunta": query,
            "respuesta": resultado["respuesta"],
            "conceptos": resultado["conceptos"],
            "confianza": resultado["confianza"],
            "chunks": resultado["chunks"]
        })

if st.session_state.historial:
    st.divider()
    st.subheader("📝 Historial")

    for h in reversed(st.session_state.historial):
        with st.expander(f"❓ {h['pregunta']}", expanded=False):
            st.markdown(f"**🎯 Relevancia:** {h['confianza']:.1%}")
            st.markdown(f"**🔑 Conceptos clave:** {h['conceptos']}")
            st.markdown("**💬 Respuesta:**")
            st.write(h["respuesta"])

            st.markdown("---")
            st.markdown("**📄 Secciones relevantes:**")
            for idx, sim in h["chunks"]:
                st.markdown(f"- Chunk {idx} — similitud {sim:.1%}")

