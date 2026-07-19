import os
from src.ingestion import curar_y_procesar_politicas

class FinSecureAgent:
    def __init__(self):
        print("=== ETAPA 2: Inicializando Agente Inteligente FinSecure ===")
        # Cargamos los chunks curados y limpios de la base de conocimiento
        try:
            self.knowledge_base = curar_y_procesar_politicas()
        except Exception as e:
            print(f"Error al cargar la base de conocimiento: {e}")
            self.knowledge_base = []

    def buscar_contexto(self, query, categoria_filtro=None):
        """
        Simula la recuperación semántica (Retrieval) filtrando por metadatos relevantes.
        """
        contextos_encontrados = []
        query_palabras = query.lower().split()
        
        for doc in self.knowledge_base:
            texto = doc["chunk_text"].lower()
            metadatos = doc["metadata"]
            
            # Filtrado por categoría si el usuario lo especifica (Control de acceso/Metadatos)
            if categoria_filtro and metadatos["categoria"] != categoria_filtro:
                continue
                
            # Búsqueda de coincidencia por palabras clave básicas
            coincidencias = sum(1 for palabra in query_palabras if palabra in texto)
            if coincidencias > 0:
                contextos_encontrados.append((coincidencias, doc["chunk_text"]))
                
        # Ordenar por el número de coincidencias encontradas
        contextos_encontrados.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in contextos_encontrados[:2]] # Retorna los 2 fragmentos más relevantes

    def responder_consulta(self, query, categoria_filtro=None):
        """
        Genera la respuesta final emulando el comportamiento de un LLM con RAG (Anti-alucinaciones).
        """
        contextos = self.buscar_contexto(query, categoria_filtro)
        
        if not contextos:
            # FLUJO ALTERNATIVO (Fallback obligatorio): Mitiga alucinaciones si no hay datos oficiales
            return (
                "Lo siento, no encontré información oficial vigente sobre esa consulta en la "
                "base de conocimiento corporativa. Por favor, comunícate con el área responsable."
            )
            
        # Simulación de la respuesta estructurada del agente combinando el contexto
        contexto_unido = "\n\n".join(contextos)
        respuesta = (
            f"Basado en las políticas internas de la compañía, te informo:\n\n"
            f"[Información de Respaldo Recuperada]:\n{contexto_unido}\n\n"
            f"Espero que esta información resuelva tu duda regulatoria."
        )
        return respuesta

if __name__ == "__main__":
    # Prueba rápida del comportamiento del agente
    agente = FinSecureAgent()
    print("\n--- Simulando Consulta de Usuario ---")
    pregunta = "¿Cuáles son los límites de transacciones?"
    print(f"Pregunta: {pregunta}")
    print(agente.responder_consulta(pregunta))
