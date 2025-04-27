# RAG Study Project with SmolaGents and BM25

Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) utilizando SmolaGents y BM25Retriever para procesamiento y consulta de documentos locales. Es una implementación educativa que demuestra cómo construir un sistema RAG utilizando búsqueda basada en términos.

## Características

- Procesamiento de múltiples formatos de documentos (PDF, TXT, DOCX, MD)
- Búsqueda eficiente con BM25Retriever
- Integración con modelos de OpenAI mediante SmolaGents
- Chat interactivo con documentos
- Manejo robusto de errores

## Configuración

1. Crear y activar el entorno virtual:

```bash
python -m venv .venv

# En Windows:
.venv\Scripts\activate
# En Unix o MacOS:
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
   Crear un archivo `.env` con:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-0125-preview  # o el modelo que prefieras
```

## Uso

1. Ejecutar el script principal:

```python
python rag_agent.py
```

2. Seguir las instrucciones en consola para interactuar con los documentos.

### Formatos de Archivo Soportados

El sistema soporta los siguientes formatos:

- Archivos PDF (`.pdf`)
- Archivos de texto (`.txt`)
- Documentos Word (`.doc`, `.docx`)
- Archivos Markdown (`.md`)

## Características Técnicas

- Utiliza SmolaGents para interacciones basadas en agentes
- BM25Retriever para búsqueda eficiente de términos
- División de documentos en chunks para mejor recuperación
- Configurable para despliegues locales
- Utiliza modelos de OpenAI (configurable via variables de entorno)
- Soporta múltiples formatos de documentos

## Notas

- Los documentos se dividen automáticamente en chunks para mejor recuperación
- El tamaño predeterminado de chunk es 500 tokens con 50 tokens de superposición
- El sistema recupera los 10 chunks más relevantes para cada consulta
- El modelo de OpenAI se puede configurar mediante la variable OPENAI_MODEL

## Próximos Pasos

- Implementar caché de resultados
- Añadir soporte para más formatos de documentos
- Mejorar la interfaz de usuario
- Implementar evaluación de calidad de respuestas
