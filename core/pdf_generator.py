from fpdf import FPDF
import os

class AnalytixaPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42) 
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.set_y(10)
        self.cell(0, 10, '  ANALYTXIA', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, '   Reporte de Performance Publicitaria Profesional', 0, 1, 'L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'AnalytxIA - Pagina {self.page_no()}', 0, 0, 'C')

def generar_reporte_pdf(id_cuenta, resumen, reporte_texto, filename):
    pdf = AnalytixaPDF()
    pdf.add_page()
    
    pdf.set_y(40)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, f"Cuenta ID: {id_cuenta}", 0, 1, 'L')
    pdf.ln(2)
    
    # Tabla Resumen
    pdf.set_fill_color(241, 245, 249)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(63, 10, 'Inversion', 1, 0, 'C', True)
    pdf.cell(63, 10, 'Clics', 1, 0, 'C', True)
    pdf.cell(63, 10, 'CPC Promedio', 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(63, 12, str(resumen['total_gasto']), 1, 0, 'C')
    pdf.cell(63, 12, str(resumen['total_clics']), 1, 0, 'C')
    pdf.cell(63, 12, str(resumen['cpc_promedio']), 1, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 10, "ANALISIS Y RECOMENDACIONES", 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_font('Arial', '', 10.5)
    pdf.set_text_color(50, 50, 50)
    
    # --- ESCUDO PROTECTOR ---
    # Si la IA falla o no manda nada, le asignamos un texto por defecto
    if reporte_texto is None:
        reporte_texto = "No se pudo generar el análisis de IA en este momento debido a un micro-corte. Por favor, vuelva a auditar la cuenta."
    
    # Limpiamos Markdown asegurándonos de que sea un string (str) para que el PDF no se rompa
    clean_text = str(reporte_texto).replace('**', '').replace('###', '').replace('---', '').replace('¡', '').replace('¿', '')
    pdf.multi_cell(0, 7, clean_text.encode('latin-1', 'ignore').decode('latin-1'))

    path = os.path.join('static', 'reports', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pdf.output(path)
    return filename