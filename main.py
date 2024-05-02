# -*- coding: utf-8 -*-
import Tkinter as tk
import tkFileDialog
import tkMessageBox
from PIL import Image, ImageTk
import subprocess
import os
from sintactico import analizar_y_traducir

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Analizador PL0 GUI")
        self.configure(bg='#333')

        self.title_label = tk.Label(self, text="Analizador JavaScript", font=("Helvetica", 16, "bold"), bg='#333', fg='white')
        self.title_label.pack(pady=(20, 10))

        self.instructions_label = tk.Label(self, text="Seleccione un archivo JS para analizar:", font=("Helvetica", 10), bg='#333', fg='white')
        self.instructions_label.pack(pady=(0, 20))

        self.boton_analizar = tk.Button(self, text="Seleccionar Archivo", command=self.seleccionar_archivo_y_analizar, bg='#5C85FB', fg='white', font=("Helvetica", 12), bd=0)
        self.boton_analizar.pack(pady=(0, 20), ipadx=10, ipady=5)

        self.minsize(400, 200)
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

    def seleccionar_archivo_y_analizar(self):
        filepath = tkFileDialog.askopenfilename(
            title="Seleccionar archivo PL/0",
            filetypes=(("Archivos JavaScript", "*.js"), ("Todos los archivos", "*.*")),
            parent=self
        )
        if filepath:
            try:
                # La función ahora devuelve la ruta del archivo .dot generado
                dot_file_path = analizar_y_traducir(filepath)
                print "Ruta al archivo DOT:", dot_file_path
                if os.path.exists(dot_file_path):
                    print "El archivo .dot fue encontrado."
                    self.display_graph(dot_file_path)
                else:
                    tkMessageBox.showerror("Error", "El archivo .dot no fue encontrado.", parent=self)
            except Exception as e:
                print "Ocurrio un error:", e
                tkMessageBox.showerror("Error", str(e), parent=self)

    def display_graph(self, dot_file):
        png_file = dot_file.replace('.dot', '.png')
        print("Ruta al archivo PNG:", png_file)
        try:
            subprocess.check_call(['dot', '-Tpng', dot_file, '-o', png_file])
            tkMessageBox.showinfo("Gráfico generado", "El gráfico ha sido generado con éxito.", parent=self)
            self.open_image_window(png_file)
        except subprocess.CalledProcessError as e:
            tkMessageBox.showerror("Error al generar gráfico", "Graphviz falló: " + str(e), parent=self)
        except Exception as e:
            tkMessageBox.showerror("Error", "Ocurrió un error: " + str(e), parent=self)

    def open_image_window(self, image_path):
        new_window = tk.Toplevel(self)
        new_window.title("Visualización del Gráfico")
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(new_window, image=photo)
        label.image = photo  # Mantén una referencia
        label.pack()

if __name__ == '__main__':
    app = Application()
    app.mainloop()
