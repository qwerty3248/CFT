import tkinter as tk
from tkinter import messagebox, scrolledtext,ttk
import platform
import subprocess
import os
import shutil
from fpdf import FPDF
from datetime import datetime

# Instalacion de dependecias del script
try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, ttk
    import platform
    import subprocess
    import os
    import shutil
    from fpdf import FPDF
    from datetime import datetime
except Exception as e:
    print(f"Error al instalar dependencias: {e}")

# Función para detectar información básica del sistema
def detectar_sistema():
    sistema = platform.system()
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
        info = {}
        for line in lines:
            key, _, value = line.partition("=")
            info[key.strip()] = value.strip().strip('"')
        distro = info.get("NAME", "Desconocido")
        version = info.get("VERSION", "")
    except Exception:
        distro, version = ("Desconocido", "")
    kernel = platform.release()

    return f"Sistema operativo: {sistema}\nDistribución: {distro} {version}\nVersión del kernel: {kernel}", distro, version

# Función para comprobar si hay actualizaciones pendientes
def comprobar_actualizaciones(distro):
    try:
        if shutil.which("apt"):
            resultado = subprocess.run(['apt', 'list', '--upgradable'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            salida = resultado.stdout.strip()
            if "Listing..." in salida:
                salida = '\n'.join(salida.split('\n')[1:])
            return salida if salida else "No hay actualizaciones pendientes."
        elif shutil.which("dnf"):
            resultado = subprocess.run(['dnf', 'check-update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return resultado.stdout.strip() or "No hay actualizaciones pendientes."
        elif shutil.which("pacman"):
            resultado = subprocess.run(['checkupdates'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return resultado.stdout.strip() or "No hay actualizaciones pendientes."
        else:
            return "Gestor de paquetes no compatible detectado."
    except Exception as e:
        return f"Error al comprobar actualizaciones: {e}"

# Función para comprobar si ufw (firewall) está activo
def comprobar_firewall():
    try:
        resultado = subprocess.run(['ufw', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Status: active" in resultado.stdout:
            return "✅ Firewall (ufw) está ACTIVADO."
        else:
            return "⚠️ Firewall (ufw) NO está activado."
    except Exception as e:
        return f"No se pudo comprobar el firewall: {e}"

# Función para buscar vulnerabilidades conocidas usando osv-scanner
def buscar_vulnerabilidades():
    if not shutil.which("osv-scanner"):
        return "osv-scanner no está instalado. Puede instalarlo desde https://github.com/google/osv-scanner"

    try:
        resultado = subprocess.run(["osv-scanner", "--lockfile=", "/dev/null"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return resultado.stdout.strip() or "✅ No se encontraron vulnerabilidades."
    except Exception as e:
        return f"Error al ejecutar osv-scanner: {e}"

# Función para ejecutar auditoría con Lynis
def ejecutar_lynis():
    if not shutil.which("lynis"):
        return "Lynis no está instalado. Puede instalarlo con 'sudo apt install lynis' o desde https://cisofy.com/lynis/"

    try:
        resultado = subprocess.run(["sudo", "lynis", "audit", "system"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return resultado.stdout.strip()[-2000:]
    except Exception as e:
        return f"Error al ejecutar Lynis: {e}"

# Función para escanear con ClamAV
def escanear_clamav():
    if not shutil.which("clamscan"):
        return "ClamAV no está instalado. Puede instalarlo con 'sudo apt install clamav' o desde https://www.clamav.net"

    try:
        resultado = subprocess.run(["clamscan", "-r", "--bell", "/home/jesus/Imágenes"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return resultado.stdout.strip()[-2000:]
    except Exception as e:
        return f"Error al ejecutar ClamAV: {e}"

# Función para comprobar puertos abiertos y detectar si están expuestos al exterior
def comprobar_puertos_abiertos():
    try:
        resultado = subprocess.run(['ss', '-tuln'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lineas = resultado.stdout.strip().split('\n')[1:]  # Omitir encabezado
        puertos_abiertos = []
        for linea in lineas:
            columnas = linea.split()
            if len(columnas) >= 5:
                direccion = columnas[4]
                if '0.0.0.0' in direccion or '[::]' in direccion:
                    expuesto = "⚠️ EXPUESTO al exterior"
                else:
                    expuesto = "✅ Sólo accesible localmente"
                puertos_abiertos.append(f"{linea} -> {expuesto}")
        return "\n".join(puertos_abiertos) if puertos_abiertos else "No hay puertos abiertos detectados."
    except Exception as e:
        return f"Error al comprobar puertos: {e}"

# Exportar a PDF
def exportar_pdf(contenido):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for linea in contenido.split('\n'):
        pdf.multi_cell(0, 10, linea)
    nombre = f"informe_seguridad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(nombre)
    messagebox.showinfo("PDF generado", f"Informe exportado como {nombre}")

def analizar_sistema():
    salida_texto.delete(1.0, tk.END)

    estado_label.config(text="🔍 Detectando información del sistema...")
    ventana.update_idletasks()
    info, distro, version = detectar_sistema()
    contenido = f"[INFO DEL SISTEMA]\n{info}\n\n"
    salida_texto.insert(tk.END, contenido)

    estado_label.config(text="📦 Comprobando actualizaciones disponibles...")
    ventana.update_idletasks()
    salida_texto.insert(tk.END, "[ACTUALIZACIONES DISPONIBLES]\n")
    actualizaciones = comprobar_actualizaciones(distro)
    salida_texto.insert(tk.END, f"{actualizaciones}\n")
    contenido += f"[ACTUALIZACIONES DISPONIBLES]\n{actualizaciones}\n"

    if "No hay actualizaciones" not in actualizaciones and "no hay actualizaciones" not in actualizaciones.lower():
        recomendacion = "⚠️ Su sistema NO está completamente actualizado. Se recomienda actualizarlo cuanto antes.\n\n"
    else:
        recomendacion = "✅ El sistema está completamente actualizado.\n\n"
    salida_texto.insert(tk.END, recomendacion)
    contenido += recomendacion

    estado_label.config(text="🔒 Comprobando firewall...")
    ventana.update_idletasks()
    salida_texto.insert(tk.END, "[FIREWALL]\n")
    firewall = comprobar_firewall()
    salida_texto.insert(tk.END, f"{firewall}\n\n")
    contenido += f"[FIREWALL]\n{firewall}\n\n"

    estado_label.config(text="🌐 Comprobando puertos abiertos...")
    ventana.update_idletasks()
    salida_texto.insert(tk.END, "[PUERTOS ABIERTOS]\n")
    puertos = comprobar_puertos_abiertos()
    salida_texto.insert(tk.END, f"{puertos}\n\n")
    contenido += f"[PUERTOS ABIERTOS]\n{puertos}\n\n"

    estado_label.config(text="🔎 Buscando vulnerabilidades conocidas...")
    ventana.update_idletasks()
    salida_texto.insert(tk.END, "[VULNERABILIDADES CONOCIDAS]\n")
    vulnerabilidades = buscar_vulnerabilidades()
    salida_texto.insert(tk.END, f"{vulnerabilidades}\n\n")
    contenido += f"[VULNERABILIDADES CONOCIDAS]\n{vulnerabilidades}\n\n"

    estado_label.config(text="📋 Ejecutando auditoría de seguridad (Lynis)...")
    ventana.update_idletasks()
    salida_texto.insert(tk.END, "[AUDITORÍA DE SEGURIDAD - LYNIS]\n")
    lynis = ejecutar_lynis()
    salida_texto.insert(tk.END, f"{lynis}\n\n")
    contenido += f"[AUDITORÍA DE SEGURIDAD - LYNIS]\n{lynis}\n\n"

    estado_label.config(text="🧪 Escaneando con ClamAV...")
    ventana.update_idletasks()
    salida_texto.insert(tk.END, "[ESCANEO ANTIVIRUS - CLAMAV]\n")
    clamav = escanear_clamav()
    salida_texto.insert(tk.END, f"{clamav}\n")
    contenido += f"[ESCANEO ANTIVIRUS - CLAMAV]\n{clamav}\n"

    estado_label.config(text="✅ Análisis completado.")
    ventana.update_idletasks()

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("Estimador de Seguridad - Sistema Linux")
ventana.geometry("1000x600")

boton_analizar = tk.Button(ventana, text="Analizar Sistema", command=analizar_sistema, font=('Arial', 12), bg='lightblue')
boton_analizar.pack(pady=10)

salida_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=('Courier', 10))
salida_texto.pack(expand=True, fill='both', padx=10, pady=10)

estado_label = tk.Label(ventana, text="", font=('Arial', 10), fg="green")
estado_label.pack(pady=5)


ventana.mainloop()
