import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

from core.meta_api import obtener_metricas_campanas
from core.gemini_ai import analizar_campanas, consultar_chat_ia # <-- Importamos la nueva función
from core.pdf_generator import generar_reporte_pdf
from database import guardar_auditoria, crear_tablas, obtener_todas_las_auditorias

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
crear_tablas()

@app.route('/', methods=['GET', 'POST'])
def home():
    reporte_ia, raw_data_for_web, pdf_link = None, [], None
    nombre_cuenta, buscado = "No seleccionada", False
    
    if request.method == 'POST':
        id_cuenta = request.form.get('account_id')
        estado_filtro = request.form.get('estado_filtro', 'ACTIVE')
        
        if id_cuenta and not id_cuenta.startswith('act_'):
            id_cuenta = f"act_{id_cuenta}"
        
        buscado = True
        nombre_cuenta = f"Cuenta ID: {id_cuenta}"
        
        campanas_meta = obtener_metricas_campanas(id_cuenta, estado_filtro)
        
        if campanas_meta:
            moneda = campanas_meta[0].get('currency', 'ARS')
            total_gasto, total_clics = 0, 0
            
            if estado_filtro == 'ACTIVE':
                instruccion_ia = "Sos un Media Buyer Senior. Optimizá estas campañas ACTIVAS para mejorar el ROI hoy mismo. Sé directo."
            elif estado_filtro == 'PAUSED':
                instruccion_ia = "Sos un Auditor Forense de Marketing. Analizá este histórico de campañas PAUSADAS. Identificá qué falló y qué lecciones sacar para el futuro."
            else:
                instruccion_ia = "Sos un Analista de Datos. Hacé un análisis general del rendimiento de toda la cuenta (activas e inactivas)."

            texto_contexto = f"{instruccion_ia}\nCONTEXTO: Moneda {moneda}. Analizá el embudo (Impresiones -> Resultados).\n\n"
            
            for c in campanas_meta:
                gasto = c.get('spend', 0)
                clics = c.get('clicks', 0)
                # Extraemos el objetivo de Meta (o decimos Desconocido si falla)
                objetivo_camp = c.get('objetivo', 'Desconocido') 
                
                total_gasto += gasto
                total_clics += clics
                
                # LA MAGIA ESTÁ ACÁ: Le mandamos el Objetivo a Gemini
                texto_contexto += f"Campaña: {c['campaign_name']} ({c['status']}) | Objetivo Principal: {objetivo_camp} | Gasto: {moneda} {gasto:,.2f} | Impresiones: {c['impressions']} | Alcance: {c['reach']} | CTR: {c['ctr']}% | Resultados: {c['cantidad_resultados']} {c['tipo_resultado']} | Costo x Resultado: {moneda} {c['costo_resultado']:,.2f}\n"
                
                raw_data_for_web.append({
                    'name': c['campaign_name'],
                    'spend': f"{moneda} {gasto:,.2f}",
                    'impressions': f"{c['impressions']:,}",
                    'reach': f"{c['reach']:,}",
                    'ctr': f"{c['ctr']:.2f}%",
                    'resultado_tipo': c['tipo_resultado'],
                    'resultado_cant': c['cantidad_resultados'],
                    'costo_resultado': f"{moneda} {c['costo_resultado']:,.2f}",
                    'clicks': clics,
                    'objetivo': objetivo_camp # Por si lo querés mostrar en la tabla HTML en el futuro
                })
            
            reporte_ia = analizar_campanas(texto_contexto)
            
            resumen_ejecutivo = {
                'total_gasto': f"{moneda} {total_gasto:,.2f}",
                'total_clics': total_clics,
                'cpc_promedio': f"{moneda} {(total_gasto/total_clics):,.2f}" if total_clics > 0 else "0.00"
            }
            
            guardar_auditoria(id_cuenta, "Cliente Meta", campanas_meta, reporte_ia)
            pdf_filename = f"reporte_{id_cuenta}.pdf"
            generar_reporte_pdf(id_cuenta, resumen_ejecutivo, reporte_ia, pdf_filename)
            pdf_link = pdf_filename
            
            session['ultimo_reporte'] = reporte_ia
            session['contexto_data'] = texto_contexto
        else:
            reporte_ia = f"No se encontraron campañas o el Token de Meta expiró. Revisá la terminal para más detalles."

    return render_template('index.html', reporte=reporte_ia, data=raw_data_for_web, 
                           nombre_cuenta=nombre_cuenta, pdf_link=pdf_link, buscado=buscado)

@app.route('/historial')
def historial():
    auditorias_db = obtener_todas_las_auditorias()
    lista_auditorias = []
    for row in auditorias_db:
        reporte_entero = row[4] if row[4] else "Sin reporte"
        lista_auditorias.append({
            'id': row[0],
            'fecha': row[1],
            'account_id': row[2],
            'nombre': row[3],
            'reporte_corto': reporte_entero[:100] + "..." if len(reporte_entero) > 100 else reporte_entero,
            'reporte_completo': reporte_entero # Acá agregamos el reporte entero
        })
    return render_template('historial.html', auditorias=lista_auditorias)

@app.route('/chat', methods=['POST'])
def chat():
    pregunta = request.json.get('msg')
    # Para el chat, le pasamos los números crudos, no el reporte anterior, así puede calcular cosas
    contexto_previo = session.get('contexto_data', '') 
    
    if not contexto_previo: 
        return jsonify({'response': "Error: Necesitás hacer una auditoría primero para que tenga contexto de tu cuenta."})
    
    # Ahora usamos la función nueva que armamos
    respuesta_ia = consultar_chat_ia(pregunta, contexto_previo)
    return jsonify({'response': respuesta_ia})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
