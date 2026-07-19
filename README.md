# finsecure-rag-agent
# 🛡️ FinSecure RAG Agent - Fintech Compliance

Este repositorio contiene el desarrollo del agente de Inteligencia Artificial basado en Arquitectura RAG (Retrieval-Augmented Generation) para el desafío **Alura Agente**. El sistema está diseñado para auditar, procesar y responder consultas internas sobre políticas de cumplimiento, seguridad y transacciones dentro de un ecosistema Fintech.

## 🚀 Características del Proyecto
*   **Etapa 1 (Ingesta de Datos):** Carga y curación automatizada de políticas corporativas eliminando registros obsoletos o borradores.
*   **Etapa 2 (Agente RAG):** Lógica de recuperación de contextos semánticos y mitigación estricta de alucinaciones mediante un protocolo de *Fallback* (flujo alternativo).
*   **Etapa 3 (Interfaz de Usuario):** Chat interactivo minimalista desarrollado con Streamlit enfocado en la funcionalidad operativa.

## 📁 Estructura del Repositorio
*   `docs/`: Repositorio de la base de conocimiento oficial (`politicas_fintech.csv`).
*   `src/ingestion.py`: Pipeline de limpieza, validación y control de versiones de datos.
*   `src/retrieval.py`: Configuración del agente y algoritmos de recuperación contextual.
*   `src/app.py`: Interfaz de usuario para la interacción con el agente en producción.

## 🛠️ Tecnologías Utilizadas
*   Python 3.10+
*   Streamlit
*   Pandas (Gestión y estructuración de datos)
