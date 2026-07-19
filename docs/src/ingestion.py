import os
import pandas as pd

# Definición de categorías oficiales aprobadas por los responsables (Ownership)
CATEGORIAS_APROBADAS = ["Seguridad", "Legal", "Soporte", "Financiero", "Operacional"]

def curar_y_procesar_politicas(ruta_csv="docs/politicas_fintech.csv"):
    """
    Implementa la Etapa 1 del Trello: Mapeo, definición de categorías,
    curaduría de calidad (filtrado de desactualizados/borradores) y estructuración.
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"Falta la base de conocimiento obligatoria en: {ruta_csv}")
    
    # 1. Mapeo e Ingesta Inicial
    df = pd.read_csv(ruta_csv)
    chunks_validos = []
    
    print("=== ETAPA 1: Iniciando Curaduría de Calidad e Ingesta ===")
    
    # Asegurar orden dinámico por fecha para mitigar versiones desactualizadas
    if 'fecha_actualizacion' in df.columns:
        df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])
        df = df.sort_values(by='fecha_actualizacion', ascending=False)
    
    # Llevar un registro para evitar procesar duplicados de una misma sección
    secciones_procesadas = set()
    
    for _, fila in df.iterrows():
        id_doc = fila.get('id')
        categoria = fila.get('categoria')
        seccion = fila.get('seccion')
        contenido = fila.get('contenido')
        estado = fila.get('estado', 'Vigente') # Por defecto vigente si no se aclara
        
        # 2. Curaduría de Calidad: Filtrar borradores o estados desactualizados
        if estado.lower() in ['borrador', 'desactualizado', 'prueba']:
            print(f" [DESCARTADO] Documento #{id_doc} omitido por estado: '{estado}' (Control de Calidad).")
            continue
            
        # 3. Curaduría de Calidad: Validar categorización estricta para metadatos
        if categoria not in CATEGORIAS_APROBADAS:
            print(f" [DESCARTADO] Categoría inválida '{categoria}' en Doc #{id_doc}.")
            continue
            
        # 4. Curaduría de Calidad: Evitar duplicados redundantes (Quedarse con el más reciente)
        if seccion in secciones_procesadas:
            print(f" [OMITIDO] Fragmento antiguo detectado para la sección '{seccion}'. Se mantiene el más reciente.")
            continue
            
        # Si pasa los filtros de calidad, estructuramos el chunk para el RAG
        texto_estructurado = f"Categoría Corporativa: {categoria}\nÁrea Responsable: {seccion}\nNormativa: {contenido}"
        
        metadatos = {
            "id": int(id_doc),
            "categoria": str(categoria),
            "seccion": str(seccion),
            "fecha_actualizacion": str(fila['fecha_actualizacion'].date())
        }
        
        chunks_validos.append({
            "chunk_text": texto_estructurado,
            "metadata": metadatos
        })
        secciones_procesadas.add(seccion)
        print(f" [APROBADO] Sección '{seccion}' indexada con metadatos de filtrado.")

    print(f"=== Proceso terminado: {len(chunks_validos)} documentos limpios cargados ===")
    return chunks_validos

if __name__ == "__main__":
    try:
        resultado = curar_y_procesar_politicas()
    except Exception as e:
        print(f"Error en el flujo: {e}")
