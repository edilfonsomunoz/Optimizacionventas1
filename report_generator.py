from fpdf import FPDF
import os
import shutil

def create_pdf_report(df, report_folder, img_paths, resumen):
    """ Genera un informe en PDF con gráficos, resumen y una breve interpretación """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Informe de Ventas", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    # 📌 Resumen
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Resumen de Ventas", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    for key, value in resumen.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)
    
    # 📌 Asegurar que las imágenes están en la carpeta de reports
    img_report_paths = []
    for img_path in img_paths:
        source_path = os.path.join("static", img_path)  # Ruta donde se guardan los gráficos en pantalla
        dest_path = os.path.join(report_folder, img_path)  # Mover a reports/
        if os.path.exists(source_path):
            shutil.copy(source_path, dest_path)
            img_report_paths.append(dest_path)
    
    # 📌 Agregar gráficos con interpretación
    for img_path in img_report_paths:
        if os.path.exists(img_path):
            pdf.image(img_path, x=10, w=180)
            pdf.ln(5)
            if "series_tiempo" in img_path:
                pdf.set_font("Arial", "I", 12)
                pdf.multi_cell(0, 10, "Este gráfico muestra la evolución de las ventas a lo largo del tiempo, permitiendo identificar tendencias generales en el comportamiento de las ventas.")
            elif "descomposicion_tiempo" in img_path:
                pdf.set_font("Arial", "I", 12)
                pdf.multi_cell(0, 10, "Aquí se descompone la serie en sus componentes principales: tendencia, estacionalidad y residuales. Esto ayuda a comprender mejor los factores que afectan las ventas.")
            elif "pronostico" in img_path:
                pdf.set_font("Arial", "I", 12)
                pdf.multi_cell(0, 10, "Este gráfico presenta el pronóstico de ventas basado en un modelo optimizado con ARIMA, permitiendo prever el comportamiento futuro de las ventas.")
            pdf.ln(10)
    
    # 📌 Guardar el PDF
    pdf_filename = "informe_ventas.pdf"
    pdf_path = os.path.join(report_folder, pdf_filename)
    pdf.output(pdf_path)
    
    return pdf_filename