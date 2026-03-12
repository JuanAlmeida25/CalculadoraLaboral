import os
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("800x320")

styles = getSampleStyleSheet()


def operaciones():
    try:
        nombre = txtNombre.get().strip()
        documento = txtNumeroId.get().strip()
        profesion = txtProfesion.get().strip()

        dias_trabajados = float(txt_dias_trabajados.get())
        horas_por_dia = float(txt_numero_horas_trabajadas_por_dia.get())
        valor_hora = float(txt_valor_horas.get())

        salario_dia = valor_hora * horas_por_dia
        salario_mes = salario_dia * dias_trabajados

        # Guardar para exportar
        ventana.ultimo_nombre = nombre
        ventana.ultimo_id = documento
        ventana.ultimo_profesion = profesion
        ventana.ultimo_salario_dia = salario_dia
        ventana.ultimo_salario_mes = salario_mes

        texto = (
            f"{nombre}, Salario por día: ${salario_dia:,.0f}, "
            f"Salario por mes: ${salario_mes:,.0f}"
        ).replace(",", ".")
        resultLabel.config(text=texto)

    except ValueError:
        messagebox.showerror("Error", "Debes ingresar números válidos en días, horas y valor hora.")


def exportPDF(nombreArchivo, nombre, documento, profesion, salario_dia, salario_mes):
    doc = SimpleDocTemplate(nombreArchivo, pagesize=letter)

    # Estilos
    titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        leading=20
    )
    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=14
    )
    normal = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=12,
        leading=18
    )

    contenido = []

    logo_path = r"/Users/juanalmeida/Documents/Proyectos/CalculadoraDavid/Logo.jpeg"
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=90, height=90)
            img.hAlign = "LEFT"
            contenido.append(img)
            contenido.append(Spacer(1, 10))
        except Exception as e:
            print("Error cargando logo:", e)

    # Encabezado
    contenido.append(Paragraph("Nombre de empresa chingona", titulo))
    contenido.append(Paragraph("NIT: 192939942", subtitulo))
    contenido.append(Spacer(1, 14))

    # Título
    contenido.append(Paragraph("<b>Reporte de ganancias por día y mes</b>", subtitulo))
    contenido.append(Spacer(1, 12))

    linea = f"""
        Debe a: <b>{nombre}</b>, con número de identificación: {documento}<br/>
        Un salario por día de: ${salario_dia:,.0f} y un salario por mes de: ${salario_mes:,.0f}<br/><br/>
        Por concepto de prestación de servicios profesionales como <b>{profesion}</b><br/>
        en el HomeCare de los siguientes pacientes:
    """.replace(",", ".")

    contenido.append(Paragraph(linea, normal))

    # Generar
    doc.build(contenido)


def exportar_desde_gui():
    try:
        nombre = getattr(ventana, "ultimo_nombre", None)
        documento = getattr(ventana, "ultimo_id", None)
        profesion = getattr(ventana, "ultimo_profesion", None)
        salario_dia = getattr(ventana, "ultimo_salario_dia", None)
        salario_mes = getattr(ventana, "ultimo_salario_mes", None)

        if None in (nombre, documento, profesion, salario_dia, salario_mes):
            messagebox.showwarning("Atención", "Primero debes calcular el salario antes de exportar el PDF.")
            return

        exportPDF("reporte.pdf", nombre, documento, profesion, salario_dia, salario_mes)

        ruta = os.path.abspath("reporte.pdf")
        messagebox.showinfo("Éxito", f"Reporte generado.\nSe guardó en:\n{ruta}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar el PDF:\n{e}")
        print("Error exportando PDF:", e)


tk.Label(ventana, text="Ingresar nombre").place(x=0, y=40)
txtNombre = tk.Entry(ventana, width=18)
txtNombre.place(x=120, y=40)

tk.Label(ventana, text="Ingresar número de documento").place(x=320, y=40)
txtNumeroId = tk.Entry(ventana, width=18)
txtNumeroId.place(x=520, y=40)

tk.Label(ventana, text="Ingresar profesión").place(x=0, y=80)
txtProfesion = tk.Entry(ventana, width=30)
txtProfesion.place(x=240, y=80)

tk.Label(ventana, text="Ingresar número de días trabajados: ").place(x=0, y=120)
txt_dias_trabajados = tk.Entry(ventana, width=30)
txt_dias_trabajados.place(x=240, y=120)

tk.Label(ventana, text="Ingresar horas trabajadas por día: ").place(x=0, y=160)
txt_numero_horas_trabajadas_por_dia = tk.Entry(ventana, width=30)
txt_numero_horas_trabajadas_por_dia.place(x=220, y=160)

tk.Label(ventana, text="Ingresar valor de las horas trabajadas: ").place(x=0, y=200)
txt_valor_horas = tk.Entry(ventana, width=30)
txt_valor_horas.place(x=260, y=200)

btn_calcular = tk.Button(ventana, text="Calcular", command=operaciones)
btn_calcular.place(x=120, y=240)

btn_export = tk.Button(ventana, text="Exportar", command=exportar_desde_gui)
btn_export.place(x=0, y=240)

resultLabel = tk.Label(ventana, text="")
resultLabel.place(x=240, y=240)

ventana.mainloop()
