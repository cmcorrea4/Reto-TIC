# 🌱 SueloGuIA - Agente de Datos de Suelos Agrosavia

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-yellow.svg)](https://langchain.com)

Herramienta integral para el análisis de calidad de datos de suelos agrícolas, cálculo del **Índice de Calidad de Datos (ICD)** y consultas mediante asistentes conversacionales con IA.

---

## 📋 Descripción

SueloGuIA es una aplicación web desarrollada con Streamlit que permite:

- **Cargar y procesar** datos de análisis de suelos desde archivos CSV/Excel o APIs Socrata
- **Calcular el Índice de Calidad de Datos (ICD)** con 6 dimensiones de evaluación
- **Visualizar estadísticas** descriptivas y detectar outliers con múltiples métodos
- **Consultar datos** mediante lenguaje natural con un agente IA (GPT + Pandas)
- **Obtener recomendaciones** agronómicas mediante RAG (Retrieval-Augmented Generation)

---

## 🏗️ Estructura del Proyecto

```
sueloguia/
│
├── Inicio.py                    # Página principal - Carga de datos
├── utils.py                  # Utilidades: limpieza, normalización, tipos
├── calidad_datos.py          # Cálculo del Índice de Calidad de Datos (ICD)
├── visualizaciones.py        # Estadísticos descriptivos y gráficos
├── recomendaciones.pdf       # Documento base para RAG (recomendaciones agronómicas)
│
├── pages/
│   ├── 2_📊_Análisis e IDC.py  # Análisis estadístico y cálculo de ICD
│   ├── 3_🤖🔬_Asistente de datos.py   # Agente conversacional con Pandas
│   └── 4_🤖📚_Asistente de información.py.py       # Asistente RAG con documento de recomendaciones
│
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

---

## 🎯 Funcionalidades

### 1. Carga de Datos (`app.py`)

- **Archivos locales**: Soporte para CSV y Excel (.xlsx, .xls)
- **API Socrata**: Conexión directa a datos.gov.co y otros portales de datos abiertos
- **Limpieza automática**: Eliminación de filas/columnas vacías, duplicados y conversión de tipos
- **Normalización**: Estandarización de nombres de columnas (tildes, espacios, mayúsculas)

### 2. Índice de Calidad de Datos - ICD (`calidad_datos.py`)

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

### 5. Agente IA para Consultas (`pages/2_🤖_Analisis_IA.py`)

Utiliza LangChain + OpenAI GPT para responder preguntas en lenguaje natural:

```
Ejemplos de consultas:
- "¿Cuál es la media de pH en los cultivos de café?"
- "Muestra un resumen estadístico de materia orgánica"
- "¿Cuántos datos nulos tiene la conductividad eléctrica?"
- "¿Qué cultivos se dan en el municipio de Pasca?"
```

### 6. RAG con Recomendaciones (`pages/3_📄_RAG_PDF.py`)

Sistema de Retrieval-Augmented Generation que consulta el documento `recomendaciones.pdf`:

```
Ejemplos de consultas:
- "¿Qué significa un alto valor de Aluminio?"
- "¿Qué hacer si tengo un pH de agua bajo?"
- "¿Cómo interpretar la asimetría en los datos?"
```

---

## 🛠️ Instalación

### Prerrequisitos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- API Key de OpenAI (para funcionalidades de IA)

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

4. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

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
```

---

## 🚀 Uso

### 1. Cargar datos

Desde la página principal, puedes:

- **Subir un archivo** CSV o Excel con datos de suelos
- **Conectar a API Socrata** (ej: datos.gov.co, dataset `ch4u-f3i5`)

### 2. Analizar calidad de datos

En la página **📊 Estadísticos**:

1. Selecciona las variables a analizar
2. Elige el método de detección de outliers
3. Haz clic en "Generar Análisis"
4. Revisa el ICD, estadísticos y visualizaciones

### 3. Consultas con IA

En la página **🤖 Análisis IA**:

1. Ingresa tu API Key de OpenAI en la barra lateral
2. Escribe tu pregunta en lenguaje natural
3. El agente analizará los datos y responderá

### 4. Consultas sobre recomendaciones

En la página **📄 RAG PDF**:

1. Ingresa tu API Key de OpenAI
2. Haz preguntas sobre interpretación de resultados o recomendaciones agronómicas

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

## ⚙️ Configuración

### Variables de entorno

Puedes configurar la API Key de OpenAI como variable de entorno:

```bash
export OPENAI_API_KEY="tu-api-key-aqui"
```

### Configuración de Socrata

Para conectar a datos.gov.co:
- **Dominio**: `www.datos.gov.co`
- **Dataset ID**: `ch4u-f3i5` (datos de suelos Agrosavia)
- **App Token**: Opcional, pero recomendado para mayor límite de requests

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
- [OpenAI](https://openai.com/) - Modelos de lenguaje GPT

---

## 📞 Soporte

Si tienes preguntas o problemas, por favor abre un issue en el repositorio.
