import os
import requests
from dotenv import load_dotenv

load_dotenv()

def obtener_metricas_campanas(ad_account_id, estado='ACTIVE', limit=50):
    access_token = os.getenv('META_ACCESS_TOKEN')
    if not access_token:
        print("❌ Error: No se encontró META_ACCESS_TOKEN en el archivo .env")
        return []

    # --- EL TRUCO DE JUAN (Control de Pulso de los últimos 3 días) ---
    campanas_vivas_ids = set()
    
    if estado == 'ACTIVE':
        # Consultamos qué campañas gastaron plata recientemente (las verdaderamente vivas)
        url_pulse = f"https://graph.facebook.com/v19.0/{ad_account_id}/insights"
        params_pulse = {
            'access_token': access_token,
            'level': 'campaign',
            'fields': 'campaign_id',
            'date_preset': 'last_3d',
            'limit': 1000
        }
        try:
            resp_pulse = requests.get(url_pulse, params=params_pulse).json()
            for item in resp_pulse.get('data', []):
                campanas_vivas_ids.add(item.get('campaign_id'))
        except Exception as e:
            print(f"Error en el pulso: {e}")

    # --- AHORA SÍ, TRAEMOS LA HISTORIA COMPLETA (Maximum) ---
    url = f"https://graph.facebook.com/v19.0/{ad_account_id}/campaigns"
    
    # NUEVO: Le pedimos el 'objective' (Objetivo de la campaña) a Meta
    fields = "id,name,objective,effective_status,insights.date_preset(maximum){spend,clicks,impressions,reach,ctr,actions,cost_per_action_type}"
    
    params = {
        'access_token': access_token,
        'fields': fields,
        'limit': limit
    }

    if estado != 'ALL':
        params['effective_status'] = f'["{estado}"]'
    else:
        params['effective_status'] = '["ACTIVE","PAUSED","ARCHIVED"]'

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'error' in data:
            print(f"❌ Error de Meta API: {data['error']}")
            return []

        campanas_procesadas = []

        for camp in data.get('data', []):
            camp_id = camp.get('id')
            camp_name = camp.get('name')
            camp_status = camp.get('effective_status')
            
            # --- NUEVO: Extraemos el objetivo y lo traducimos al español ---
            camp_objective_raw = camp.get('objective', 'Desconocido')
            
            # Diccionario para que la IA y la tabla entiendan de qué trata la campaña
            diccionario_objetivos = {
                'OUTCOME_ENGAGEMENT': 'Interacción (Mensajes)',
                'OUTCOME_SALES': 'Ventas / Conversiones',
                'OUTCOME_LEADS': 'Clientes Potenciales (Leads)',
                'OUTCOME_TRAFFIC': 'Tráfico al Sitio Web',
                'OUTCOME_AWARENESS': 'Reconocimiento de Marca',
                'MESSAGES': 'Mensajes (WhatsApp/Instagram)'
            }
            objetivo_traducido = diccionario_objetivos.get(camp_objective_raw, camp_objective_raw)

            # Filtro Inteligente: Si pidieron Activas y no tiene pulso, la ignoramos.
            if estado == 'ACTIVE' and camp_id not in campanas_vivas_ids:
                continue

            # Filtro normal de estado
            if estado != 'ALL' and camp_status != estado:
                continue

            insights_data = camp.get('insights', {}).get('data', [])
            
            if not insights_data:
                continue 
                
            item = insights_data[0]
            
            spend = float(item.get('spend', 0))
            if spend <= 0:
                continue

            clicks = int(item.get('clicks', 0))
            impressions = int(item.get('impressions', 0))
            reach = int(item.get('reach', 0))
            ctr = float(item.get('ctr', 0))

            actions = item.get('actions', [])
            
            mensajes = 0
            leads = 0
            clics_enlace = 0
            
            for action in actions:
                action_type = action.get('action_type', '')
                value = int(action.get('value', 0))
                
                if 'messaging_conversation_started' in action_type or 'messages_conversation_started' in action_type:
                    mensajes += value
                elif 'lead' in action_type:
                    leads += value
                elif action_type == 'link_click':
                    clics_enlace += value

            if mensajes > 0:
                tipo_resultado = "Mensajes"
                cantidad_resultados = mensajes
            elif leads > 0:
                tipo_resultado = "Leads"
                cantidad_resultados = leads
            elif clics_enlace > 0:
                tipo_resultado = "Clics en Enlace"
                cantidad_resultados = clics_enlace
            else:
                tipo_resultado = "Clics Totales"
                cantidad_resultados = clicks

            costo_resultado = spend / cantidad_resultados if cantidad_resultados > 0 else 0

            campanas_procesadas.append({
                'campaign_name': camp_name,
                'objetivo': objetivo_traducido, # <-- ¡Acá mandamos el objetivo traducido!
                'spend': spend,
                'clicks': clicks,
                'impressions': impressions,
                'reach': reach,
                'ctr': ctr,
                'tipo_resultado': tipo_resultado,
                'cantidad_resultados': cantidad_resultados,
                'costo_resultado': costo_resultado,
                'currency': 'ARS',
                'status': camp_status
            })

        return campanas_procesadas

    except Exception as e:
        print(f"❌ Error interno al consultar Meta: {e}")
        return []