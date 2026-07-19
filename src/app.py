import streamlit as st
from src.retrieval import FinSecureAgent

# Configuración de la página (Cumpliendo enfoque funcional del Challenge)
st.set_page_config(page_title="FinSecure RAG Agent", page_icon="🛡️", layout="centered")

@st.cache_resource
def inicializar_agente():
    return FinSecureAgent()

# Instanciar el agente de IA
try:
    agent = inicializar_agente()
except Exception as e:
    st.error(f"Error al cargar el motor del agente: {e}")
    agent = None

st.title("🛡️ FinSecure AI Agent")
st.subheader("Asistente Virtual de Políticas Internas y Cumplimiento")
st.write("Realiza consultas sobre normativas de seguridad, transacciones y soporte.")

# Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    # Mostrar el mensaje del usuario en el contenedor
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta del agente usando el pipeline RAG
    with st.chat_message("assistant"):
        if agent:
            with st.spinner("Buscando en la base de conocimiento oficial..."):
                respuesta = agent.responder_consulta(prompt)
                st.markdown(respuesta)
        else:
            respuesta = "El sistema no está disponible en este momento por fallas en la base de conocimiento."
            st.markdown(respuesta)
            
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
