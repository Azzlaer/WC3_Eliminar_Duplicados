# -*- coding: utf-8 -*-
"""
Buscador y limpiador de archivos duplicados con GUI (Tkinter)
-----------------------------------------------------------------
Características principales:
- Selección de carpeta a analizar.
- Cálculo de hashes SHA-256 para detectar duplicados (idéntico contenido).
- Vista de resultados en un Listbox (todos los duplicados listados).
- Bitácora (LOG) embebida en la ventana para seguimiento de acciones.
- Botón para eliminar duplicados (mantiene 1 copia por hash).
- Generación de informe en archivo: REGISTRO_DD_MM_AAAA.log.
- Barra de progreso y contadores de archivos/duplicados.
- Manejo en hilo secundario para evitar congelar la interfaz.

Requisitos: Python 3.x estándar (sin dependencias externas).

Autor: Conversión desde BAT a Python con GUI.
"""

import os
import sys
import hashlib
import threading
from datetime import datetime
import traceback
from tkinter import Tk, StringVar, IntVar, END, BOTH, RIGHT, LEFT, X, Y, BOTTOM, TOP
from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter as tk

# ---------------------------- Utilidades ---------------------------- #

def calcular_sha256(ruta, chunk_size=1024 * 1024):
    """Devuelve el hash SHA256 de un archivo leyendo en bloques."""
    sha = hashlib.sha256()
    with open(ruta, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def formato_bytes(n):
    """Devuelve un tamaño legible (KB, MB, GB)."""
    for unidad in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0 or unidad == 'TB':
            return f"{n:3.1f} {unidad}"
        n /= 1024.0


# ---------------------------- Aplicación ---------------------------- #

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Buscador de duplicados (SHA-256)")
        master.minsize(900, 600)

        # Estado
        self.carpeta = StringVar(value="")
        self.incluir_subcarpetas = IntVar(value=1)
        self.modo_simulacion = IntVar(value=0)
        self.analizando = False

        # Datos de resultados
        self.total_archivos = 0
        self.duplicados_lista = []  # lista de rutas que son duplicados (excluye el original conservado)
        self.hash_map = {}  # hash -> [rutas]

        self._construir_ui()

    # ---------------------------- UI ---------------------------- #
    def _construir_ui(self):
        # Área superior: selección de carpeta y controles
        frm_top = ttk.Frame(self.master, padding=10)
        frm_top.pack(side=TOP, fill=X)

        lbl = ttk.Label(frm_top, text="Carpeta a analizar:")
        lbl.pack(side=LEFT)

        self.ent_carpeta = ttk.Entry(frm_top, textvariable=self.carpeta)
        self.ent_carpeta.pack(side=LEFT, fill=X, expand=True, padx=8)

        btn_browse = ttk.Button(frm_top, text="Seleccionar...", command=self.seleccionar_carpeta)
        btn_browse.pack(side=LEFT)

        self.chk_recursivo = ttk.Checkbutton(frm_top, text="Incluir subcarpetas", variable=self.incluir_subcarpetas)
        self.chk_recursivo.pack(side=LEFT, padx=8)

        self.chk_simulacion = ttk.Checkbutton(frm_top, text="Simular eliminación (no borra)", variable=self.modo_simulacion)
        self.chk_simulacion.pack(side=LEFT)

        # Área de botones de acciones
        frm_btns = ttk.Frame(self.master, padding=(10, 0))
        frm_btns.pack(side=TOP, fill=X)

        self.btn_analizar = ttk.Button(frm_btns, text="Analizar", command=self.iniciar_analisis)
        self.btn_analizar.pack(side=LEFT)

        self.btn_eliminar = ttk.Button(frm_btns, text="Eliminar duplicados", command=self.eliminar_duplicados, state='disabled')
        self.btn_eliminar.pack(side=LEFT, padx=6)

        self.btn_exportar = ttk.Button(frm_btns, text="Exportar informe (LOG)", command=self.exportar_log, state='disabled')
        self.btn_exportar.pack(side=LEFT)

        # Progreso y contadores
        frm_prog = ttk.Frame(self.master, padding=10)
        frm_prog.pack(side=TOP, fill=X)

        self.progreso = ttk.Progressbar(frm_prog, mode='determinate')
        self.progreso.pack(side=TOP, fill=X)

        self.lbl_stats = ttk.Label(frm_prog, text="Listo.")
        self.lbl_stats.pack(side=TOP, anchor='w', pady=5)

        # Split principal: Listbox de duplicados y consola LOG
        frm_split = ttk.Panedwindow(self.master, orient=tk.HORIZONTAL)
        frm_split.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo: Duplicados
        frm_left = ttk.Labelframe(frm_split, text="Duplicados encontrados (se eliminarán, se conserva 1 por hash)")
        frm_split.add(frm_left, weight=3)

        self.lb = tk.Listbox(frm_left, selectmode=tk.EXTENDED)
        self.lb_scroll_y = ttk.Scrollbar(frm_left, orient=tk.VERTICAL, command=self.lb.yview)
        self.lb.configure(yscrollcommand=self.lb_scroll_y.set)

        self.lb.pack(side=LEFT, fill=BOTH, expand=True)
        self.lb_scroll_y.pack(side=RIGHT, fill=Y)

        # Panel derecho: LOG
        frm_right = ttk.Labelframe(frm_split, text="LOG en vivo")
        frm_split.add(frm_right, weight=2)

        self.txt = tk.Text(frm_right, height=10, wrap='word')
        self.txt_scroll_y = ttk.Scrollbar(frm_right, orient=tk.VERTICAL, command=self.txt.yview)
        self.txt.configure(yscrollcommand=self.txt_scroll_y.set)
        self.txt.pack(side=LEFT, fill=BOTH, expand=True)
        self.txt_scroll_y.pack(side=RIGHT, fill=Y)

        self._log("Aplicación iniciada. Seleccione una carpeta y presione 'Analizar'.")

    # ---------------------------- Eventos UI ---------------------------- #
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccione una carpeta a analizar")
        if carpeta:
            self.carpeta.set(carpeta)

    def iniciar_analisis(self):
        if self.analizando:
            return
        ruta = self.carpeta.get().strip()
        if not ruta:
            messagebox.showwarning("Falta carpeta", "Seleccione una carpeta para analizar.")
            return
        if not os.path.isdir(ruta):
            messagebox.showerror("Carpeta inválida", "La carpeta especificada no existe.")
            return

        self.analizando = True
        self.btn_analizar.configure(state='disabled')
        self.btn_eliminar.configure(state='disabled')
        self.btn_exportar.configure(state='disabled')
        self.lb.delete(0, END)
        self.txt.delete('1.0', END)
        self._log(f"Iniciando análisis en: {ruta}")
        self.hash_map.clear()
        self.duplicados_lista.clear()
        self.total_archivos = 0
        self.progreso['value'] = 0

        hilo = threading.Thread(target=self._analizar_worker, daemon=True)
        hilo.start()

    def eliminar_duplicados(self):
        if self.analizando:
            return
        if not self.duplicados_lista:
            messagebox.showinfo("Sin duplicados", "No hay duplicados para eliminar.")
            return

        if not self.modo_simulacion.get():
            if not messagebox.askyesno("Confirmar eliminación", "Se eliminarán los archivos duplicados listados (se conserva 1 copia). ¿Desea continuar?"):
                self._log("Operación cancelada por el usuario.")
                return

        eliminados = 0
        errores = 0
        for ruta in list(self.duplicados_lista):
            try:
                if self.modo_simulacion.get():
                    self._log(f"[SIMULACIÓN] Eliminar: {ruta}")
                else:
                    os.remove(ruta)
                    self._log(f"Eliminado: {ruta}")
                eliminados += 1
                # quitar de la lista visual
                idxs = [i for i in range(self.lb.size()) if self.lb.get(i) == ruta]
                for idx in reversed(idxs):
                    self.lb.delete(idx)
                self.duplicados_lista.remove(ruta)
            except Exception as e:
                errores += 1
                self._log(f"ERROR eliminando {ruta}: {e}")

        self._log(f"Total de archivos eliminados: {eliminados}")
        if errores:
            self._log(f"Errores durante la eliminación: {errores}")
        self.btn_exportar.configure(state='normal')

    def exportar_log(self):
        ahora = datetime.now().strftime("REGISTRO_%d_%m_%Y.log")
        carpeta_dest = self.carpeta.get().strip() or os.getcwd()
        ruta_log = filedialog.asksaveasfilename(
            title="Guardar informe",
            defaultextension=".log",
            initialfile=ahora,
            initialdir=carpeta_dest,
            filetypes=[("Archivo LOG", ".log"), ("Todos", "*.*")]
        )
        if not ruta_log:
            return
        try:
            contenido = self.txt.get('1.0', END)
            with open(ruta_log, 'w', encoding='utf-8') as f:
                f.write(contenido)
            self._log(f"Informe guardado en: {ruta_log}")
            messagebox.showinfo("Informe", f"Informe guardado en:\n{ruta_log}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el informe:\n{e}")

    # ---------------------------- Lógica de análisis ---------------------------- #
    def _analizar_worker(self):
        try:
            ruta_base = self.carpeta.get().strip()
            incluir_sub = bool(self.incluir_subcarpetas.get())

            # 1) recolectar archivos
            archivos = []
            if incluir_sub:
                for root, _, files in os.walk(ruta_base):
                    for name in files:
                        archivos.append(os.path.join(root, name))
            else:
                try:
                    for name in os.listdir(ruta_base):
                        ruta = os.path.join(ruta_base, name)
                        if os.path.isfile(ruta):
                            archivos.append(ruta)
                except Exception:
                    pass

            self.total_archivos = len(archivos)
            self._ui(lambda: self.progreso.configure(maximum=max(1, self.total_archivos)))
            self._log(f"Total de archivos detectados: {self.total_archivos}")

            # 2) calcular hashes y detectar duplicados
            procesados = 0
            bytes_totales = 0
            for ruta in archivos:
                try:
                    tam = os.path.getsize(ruta)
                    bytes_totales += tam
                    h = calcular_sha256(ruta)
                    lista = self.hash_map.setdefault(h, [])
                    lista.append(ruta)
                    if len(lista) == 1:
                        self._log(f"Nuevo hash: {h[:12]}... -> {ruta}")
                    else:
                        # duplicado (dejar el primero, añadir el resto)
                        self.duplicados_lista.append(ruta)
                        self._ui(lambda r=ruta: self.lb.insert(END, r))
                        self._log(f"Duplicado encontrado (hash {h[:12]}...): {ruta}")
                except Exception as e:
                    self._log(f"ERROR leyendo {ruta}: {e}")
                finally:
                    procesados += 1
                    self._ui(lambda v=procesados: self.progreso.configure(value=v))

            # 3) resumen
            dup_count = len(self.duplicados_lista)
            resumen = (
                f"\nAnálisis finalizado.\n"
                f"Archivos analizados: {self.total_archivos}\n"
                f"Duplicados encontrados: {dup_count}\n"
                f"Tamaño total estimado analizado: {formato_bytes(bytes_totales)}\n"
            )
            self._log(resumen)

            self._ui(lambda: self.lbl_stats.configure(text=f"Analizados: {self.total_archivos} | Duplicados: {dup_count}"))
            self._ui(lambda: self.btn_eliminar.configure(state='normal' if dup_count > 0 else 'disabled'))
            self._ui(lambda: self.btn_exportar.configure(state='normal'))
        except Exception:
            self._log("\n*** Error inesperado durante el análisis ***\n" + traceback.format_exc())
        finally:
            self.analizando = False
            self._ui(lambda: self.btn_analizar.configure(state='normal'))

    # ---------------------------- Helpers ---------------------------- #
    def _log(self, texto):
        # Inserta texto en el cuadro LOG con timestamp
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        def _append():
            self.txt.insert(END, f"[{ts}] {texto}\n")
            self.txt.see(END)
        self._ui(_append)

    def _ui(self, func):
        # Ejecuta una función en el hilo de la UI de forma segura
        self.master.after(0, func)


# ---------------------------- Main ---------------------------- #

def main():
    root = Tk()
    # Estilos ttk
    try:
        style = ttk.Style(root)
        if sys.platform.startswith('win'):
            style.theme_use('vista')
        else:
            style.theme_use(style.theme_use())
    except Exception:
        pass

    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
