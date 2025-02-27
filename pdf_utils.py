from fpdf import FPDF
import os

def create_pdf_report(df, report_folder):
    pdf_filename = "analisis_ventas.pdf"
    pdf_path = os.path.join(report_folder, pdf_filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Analisis de Ventas", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Resumen del análisis:", ln=True)

    # ✅ Añadir resumen de los datos
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, f"Total de registros: {len(df)}", ln=True)
    pdf.cell(200, 10, f"Total de ventas: {df['total'].sum():,.2f}", ln=True)

    pdf.output(pdf_path)

    return pdf_filename