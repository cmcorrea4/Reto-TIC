# 🌱 SueloGuIA - Agente de Datos de Suelos Agrosavia

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-yellow.svg)](https://langchain.com)
[![Accesibilidad](https://img.shields.io/badge/Accesibilidad-Voz-orange.svg)](#-accesibilidad-por-voz)

Herramienta integral para el análisis de calidad de datos de suelos agrícolas, cálculo del **Índice de Calidad de Datos (ICD)** y consultas mediante asistentes conversacionales con IA. **Diseñada con funciones de voz para facilitar el acceso a población rural y campesina.**

---

## 🎯 Accesibilidad para el Campo Colombiano

> *"La tecnología debe estar al servicio de todos, especialmente de quienes alimentan a Colombia"*

SueloGuIA incorpora **funcionalidades de voz** pensadas especialmente para la **población campesina** que puede tener dificultades con la lectura o escritura:

### 🎤 Habla tu pregunta
No necesitas escribir. Simplemente **graba tu voz** y el sistema transcribirá automáticamente tu consulta.

### 🔊 Escucha las respuestas
Las respuestas del asistente pueden ser **reproducidas en audio**, facilitando la comprensión sin necesidad de leer textos extensos.

### 💡 ¿Por qué es importante?

- **Inclusión digital**: Democratiza el acceso a información técnica agrícola
- **Analfabetismo funcional**: Según el DANE, aproximadamente el 5.2% de la población rural colombiana tiene dificultades de lectoescritura
- **Comodidad**: Los agricultores pueden consultar mientras trabajan en campo
- **Idioma natural**: Permite hacer preguntas como se habla cotidianamente

---

## 🌐 Demo en Vivo

La aplicación está desplegada en **Streamlit Cloud**:

🔗 **[Acceder a SueloGuIA](https://agrosaviaidc.streamlit.app/)**

---

## 📋 Descripción

SueloGuIA es una aplicación web desarrollada con Streamlit que permite:

- **Cargar y procesar** datos de análisis de suelos desde archivos CSV/Excel o APIs Socrata
- **Calcular el Índice de Calidad de Datos (ICD)** con 6 dimensiones de evaluación
- **Visualizar estadísticas** descriptivas y detectar outliers con múltiples métodos
- **Consultar datos** mediante lenguaje natural con un agente IA (GPT + Pandas)
- **Obtener recomendaciones** agronómicas mediante RAG (Retrieval-Augmented Generation)
- **Interactuar por voz** 🎤 para hacer preguntas y 🔊 escuchar respuestas

---

## 🗣️ Funcionalidades de Voz

### Speech-to-Text (Voz a Texto) 🎤

Convierte tu voz en texto usando **OpenAI Whisper**:

| Característica | Descripción |
|----------------|-------------|
| **Grabación directa** | Graba desde el micrófono del dispositivo |
| **Subir audio** | Soporta archivos WAV, MP3, M4A, OGG |
| **Idioma** | Optimizado para español colombiano |
| **Costo** | $0.006 USD por minuto de audio |

**Ejemplo de uso:**
1. Haz clic en el ícono del micrófono 🎤
2. Habla tu pregunta: *"¿Qué significa que el pH del suelo esté bajo?"*
3. El sistema transcribe y procesa automáticamente

### Text-to-Speech (Texto a Voz) 🔊

Escucha las respuestas en voz natural usando **OpenAI TTS**:

| Característica | Descripción |
|----------------|-------------|
| **6 voces disponibles** | alloy, echo, fable, onyx, nova, shimmer |
| **Velocidad ajustable** | De 0.5x a 2.0x |
| **Idioma** | Pronunciación clara en español |
| **Costo** | $0.015 USD por cada 1,000 caracteres |

**Voces recomendadas para español:**
- **Nova**: Voz femenina clara y amigable ⭐ Recomendada
- **Onyx**: Voz masculina profunda
- **Alloy**: Voz neutral y versátil

---

## 🏗️ Estructura del Proyecto

```
sueloguia/
│
├── Inicio.py                 # Página principal - Carga de datos
├── utils.py                  # Utilidades: limpieza, normalización, tipos
├── calidad_datos.py          # Cálculo del Índice de Calidad de Datos (ICD)
├── visualizaciones.py        # Estadísticos descriptivos y gráficos
├── recomendaciones.pdf       # Documento base para RAG (recomendaciones agronómicas)
│
├── pages/
│   ├── 2_📊_Análisis e IDC.py              # Análisis estadístico y cálculo de ICD
│   ├── 3_🤖🔬_Asistente de datos.py        # Agente conversacional con Pandas
│   └── 4_🤖📚_Asistente de información.py  # Asistente RAG con voz habilitada
│
├── .streamlit/
│   └── secrets.toml          # Configuración de secrets (solo local)
│
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

---

## 🎯 Funcionalidades

### 1. Carga de Datos (`Inicio.py`)

- **Archivos locales**: Soporte para CSV y Excel (.xlsx, .xls)
- **API Socrata**: Conexión directa a datos.gov.co y otros portales de datos abiertos
- **Limpieza automática**: Eliminación de filas/columnas vacías, duplicados y conversión de tipos
- **Normalización**: Estandarización de nombres de columnas (tildes, espacios, mayúsculas)

### 2. Índice de Calidad de Datos - ICD (`📊_Análisis e IDC.py`)

El ICD evalúa la calidad de los datos en **6 dimensiones** con un puntaje total de 0-100:

| Dimensión | Puntos | Descripción |
|-----------|--------|-------------|
| **Completitud** | 25 | Porcentaje de valores no nulos |
| **Precisión** | 20 | Detección de outliers (IQR, K-means, SVM) |
| **Unicidad** | 15 | Identificación de registros duplicados |
| **Consistencia** | 15 | Valores con tipos de datos mixtos |
| **Variabilidad** | 15 | Coeficiente de variación por columna |
| **Integridad** | 10 | Columnas esperadas vs. disponibles |

**Niveles de calidad:**
- 🟢 **Excelente** (≥90): Datos listos para análisis avanzados
- 🟡 **Buena** (75-89): Utilizables con limpieza menor
- 🟠 **Aceptable** (60-74): Requiere limpieza antes de análisis
- 🟠 **Baja** (40-59): Limpieza profunda requerida
- 🔴 **Crítica** (<40): Revisar proceso de captura

### 3. Detección de Outliers

Tres métodos disponibles para la dimensión de Precisión:

- **IQR (Cuartiles)**: Método tradicional basado en rango intercuartílico
- **K-means**: Clustering para identificar puntos distantes de centroides
- **SVM (One-Class)**: Aprendizaje automático para detección de anomalías
- **Combinado**: Unión de los tres métodos

### 4. Visualizaciones (`visualizaciones.py`)

- Histogramas de distribución
- Boxplots para detección visual de outliers
- Matriz de correlación con heatmap
- Tabla de estadísticos descriptivos completa

### 5. Agente IA para Consultas (`pages/3_🤖🔬_Asistente de datos.py`)

Utiliza LangChain + OpenAI GPT para responder preguntas en lenguaje natural:

```
Ejemplos de consultas:
- "¿Cuál es la media de pH en los cultivos de café?"
- "Muestra un resumen estadístico de materia orgánica"
- "¿Cuál es la correlación mayor entre las variables numéricas?"
- "¿Qué cultivos se dan en el municipio de Pasca?"
```

### 6. RAG con Recomendaciones y Voz (`pages/4_🤖📚_Asistente de información.py`)

Sistema de Retrieval-Augmented Generation que consulta el documento `recomendaciones.pdf`, **ahora con soporte completo de voz**:

```
Ejemplos de consultas (escritas o habladas):
- 🎤 "¿Qué hago si mi tierra tiene mucho aluminio?"
- 🎤 "¿Por qué el pH de mi suelo está bajito?"
- 🎤 "¿Cómo mejoro la materia orgánica de mi finca?"
```

**Características de voz:**
- ⌨️ **Tab Escribir**: Entrada tradicional por texto
- 🎤 **Tab Grabar voz**: Grabación directa desde micrófono
- 🔊 **Respuesta en audio**: Activa desde la barra lateral
- 📁 **Subir audio**: Alternativa para archivos grabados

---

## 🛠️ Instalación Local

### Prerrequisitos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- API Key de OpenAI (para funcionalidades de IA)
- Micrófono (opcional, para funciones de voz)

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/sueloguia.git
   cd sueloguia
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar secrets** (ver sección de configuración)

5. **Ejecutar la aplicación**
   ```bash
   streamlit run Inicio.py
   ```

---

## ⚙️ Configuración

### Configuración de API Key (Secrets)

La aplicación utiliza `st.secrets` para manejar las credenciales de forma segura.

#### Desarrollo Local

Crea el archivo `.streamlit/secrets.toml` en la raíz del proyecto:

```toml
[settings]
key = "sk-proj-tu-api-key-de-openai"
```

> ⚠️ **Importante**: Agrega `.streamlit/secrets.toml` a tu `.gitignore` para no exponer tu API Key.

#### Streamlit Cloud

1. Ve a tu aplicación en [share.streamlit.io](https://share.streamlit.io)
2. Haz clic en **Settings** (⚙️) → **Secrets**
3. Agrega la configuración:

```toml
[settings]
key = "sk-proj-tu-api-key-de-openai"
```

4. Guarda los cambios y reinicia la aplicación

### Configuración de Socrata

Para conectar a datos.gov.co:
- **Dominio**: `www.datos.gov.co`
- **Dataset ID**: `ch4u-f3i5` (datos de suelos Agrosavia)
- **App Token**: Opcional, pero recomendado para mayor límite de requests

---

## 📦 Dependencias

```txt
# Core
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0

# Visualización
plotly>=5.18.0

# Machine Learning (detección de outliers)
scikit-learn>=1.3.0

# API Socrata
sodapy>=2.2.0

# IA y LangChain
langchain>=0.2.0
langchain-openai>=0.1.0
langchain-experimental>=0.0.50
langchain-community>=0.2.0
openai>=1.0.0

# RAG / Procesamiento de PDF
pypdf>=3.0.0
faiss-cpu>=1.7.0

# Funcionalidades de Voz
audio-recorder-streamlit==0.0.10
```

---

## 💰 Costos de las Funcionalidades de Voz

Las funcionalidades de voz utilizan la API de OpenAI y tienen los siguientes costos:

| Servicio | Modelo | Costo | Ejemplo |
|----------|--------|-------|---------|
| **Speech-to-Text** | Whisper | $0.006/minuto | 10 min de audio = $0.06 |
| **Text-to-Speech** | TTS-1 | $0.015/1K caracteres | Respuesta de 500 chars = $0.0075 |

**Nota**: El TTS está **deshabilitado por defecto** para evitar costos innecesarios. El usuario puede activarlo desde la barra lateral cuando lo necesite.

---

## 🚀 Uso

### 1. Cargar datos

Desde la página principal, puedes:

- **Subir un archivo** CSV o Excel con datos de suelos
- **Conectar a API Socrata** (ej: datos.gov.co, dataset `ch4u-f3i5`)

### 2. Analizar calidad de datos

En la página **📊 Análisis e IDC**:

1. Selecciona las variables a analizar
2. Elige el método de detección de outliers
3. Haz clic en "Generar Análisis"
4. Revisa el ICD, estadísticos, algoritmos de clasificación IA "Clásica" y visualizaciones

### 3. Consultas con IA

En la página **🤖🔬 Asistente de datos**:

1. Las credenciales se cargan automáticamente desde secrets
2. Escribe tu pregunta en lenguaje natural
3. El agente analizará y responderá sobre los datos consultados

### 4. Consultas sobre recomendaciones (con voz) 🎤🔊

En la página **🤖📚 Asistente de información**:

1. Las credenciales se cargan automáticamente desde secrets
2. **Opción A - Escribir**: Escribe tu pregunta en el formulario
3. **Opción B - Hablar**: 
   - Ve a la pestaña "🎤 Grabar voz"
   - Haz clic en el micrófono y habla tu pregunta
   - Presiona "Transcribir y preguntar"
4. **Escuchar respuesta**: Activa "🔊 Habilitar respuesta por voz" en la barra lateral

---

## 📊 Variables de Suelos Soportadas

La aplicación está optimizada para las siguientes variables de análisis de suelos:

| Variable | Descripción |
|----------|-------------|
| `ph_agua_suelo` | pH del suelo en agua |
| `materia_organica` | Contenido de materia orgánica (%) |
| `fosforo_bray_ii` | Fósforo disponible (ppm) |
| `azufre_fosfato_monocalcico` | Azufre disponible (ppm) |
| `acidez_kcl` | Acidez intercambiable |
| `aluminio_intercambiable` | Aluminio intercambiable (cmol/kg) |
| `calcio_intercambiable` | Calcio intercambiable (cmol/kg) |
| `magnesio_intercambiable` | Magnesio intercambiable (cmol/kg) |
| `potasio_intercambiable` | Potasio intercambiable (cmol/kg) |
| `sodio_intercambiable` | Sodio intercambiable (cmol/kg) |
| `capacidad_de_intercambio_cationico` | CIC (cmol/kg) |
| `conductividad_electrica` | CE (dS/m) |
| `hierro_disponible_olsen` | Hierro disponible - Olsen (ppm) |
| `cobre_disponible` | Cobre disponible (ppm) |
| `manganeso_disponible_olsen` | Manganeso disponible - Olsen (ppm) |
| `zinc_disponible_olsen` | Zinc disponible - Olsen (ppm) |
| `boro_disponible` | Boro disponible (ppm) |

---

## 🌾 Impacto Social

SueloGuIA busca contribuir a:

- **Democratización del conocimiento agrícola**: Información técnica accesible para todos
- **Inclusión digital rural**: Tecnología adaptada a las necesidades del campo
- **Mejora de la productividad**: Decisiones informadas basadas en datos de calidad
- **Sostenibilidad agrícola**: Mejor manejo de suelos basado en evidencia

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **SUME** - Desarrollo inicial

---

## 🙏 Agradecimientos

- [Agrosavia](https://www.agrosavia.co/) - Datos de análisis de suelos
- [Datos Abiertos Colombia](https://datos.gov.co/) - Plataforma de datos abiertos
- [Streamlit](https://streamlit.io/) - Framework de aplicaciones web
- [LangChain](https://langchain.com/) - Framework para aplicaciones con LLMs
- [OpenAI](https://openai.com/) - Modelos de lenguaje GPT, Whisper y TTS

---

## 📞 Soporte

Si tienes preguntas o problemas, por favor abre un issue en el repositorio.

---

<p align="center">
  <i>Hecho con ❤️ para el campo colombiano</i>
</p>
