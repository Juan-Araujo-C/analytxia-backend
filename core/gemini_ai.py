import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analizar_campanas(datos_campanas):
    prompt = f"""
    Sos un Media Buyer Senior y Analista de Marketing Digital experto en Meta Ads. 
    Tu objetivo es analizar los siguientes datos de campañas publicitarias de una PyME y darle recomendaciones CLARAS, DIRECTAS y ACCIONABLES. 
    
    Reglas de tono: 
    - Hablále de vos de forma cercana, optimista pero muy profesional, ideal para el mercado argentino de PyMEs.
    
    REGLA DE ORO (EL OBJETIVO MANDA):
    - Prestá muchísima atención al "Objetivo Principal" de cada campaña. 
    - Si el objetivo es "Interacción (Mensajes)", el CTR o el CPC son métricas secundarias; lo que importa es la cantidad de mensajes y el Costo x Mensaje.
    - Si el objetivo es "Tráfico", ahí sí importa el CPC. 
    - No recomiendes optimizar clics en una campaña de mensajes.
    
    Analizá estos datos y devolveme un reporte estructurado con:
    1. Un diagnóstico breve (qué ves a simple vista en los números).
    2. Qué está funcionando bien.
    3. Qué alerta roja ves o qué se puede mejorar urgentemente.
    4. Tres (3) recomendaciones exactas de acción inmediata según el objetivo de la campaña.
    
    Datos de las campañas a analizar:
    {datos_campanas}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        print(f"❌ Error al contactar a Gemini: {e}")
        # En vez de None, devolvemos un escudo protector
        return "⚠️ La Inteligencia Artificial está saturada en este momento (Límite de cuota). Por favor, aguardá 1 minuto y volvé a auditar la cuenta."

def consultar_chat_ia(pregunta, contexto_previo):
    """Función exclusiva para el chat en vivo, sin el prompt gigante del reporte"""
    prompt = f"""
    Sos Analytxia, un asistente de Inteligencia Artificial experto en Meta Ads.
    Respondé la siguiente pregunta del usuario de forma directa, breve y profesional.
    
    Contexto de la cuenta que estás analizando: {contexto_previo[:1500]}
    
    Pregunta del usuario: {pregunta}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "Hubo un micro-corte de conexión con mi cerebro. ¿Me repetís la pregunta?"