import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
import requests

class GS1ValitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GS1-Valitor")
        self.root.geometry("600x400")
        self.root.configure(bg="#2C2F33")

        # Estilo de fuente
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)

        # Títulos
        title_label = tk.Label(root, text="GS1-Valitor", font=self.title_font, bg="#2C2F33", fg="#FFFFFF")
        title_label.pack(pady=10)

        # Botón de cargar archivo
        load_button = tk.Button(root, text="Cargar Archivo", command=self.load_file, bg="#5E5E5E", fg="#FFFFFF", width=15)
        load_button.pack(pady=10)

        # Marco para listas
        list_frame = tk.Frame(root, bg="#2C2F33")
        list_frame.pack(pady=10)

        # Listas para códigos válidos e inválidos
        self.valid_codes_label = tk.Label(list_frame, text="Códigos Válidos", font=self.label_font, bg="#2C2F33", fg="#00FF00")
        self.valid_codes_label.grid(row=0, column=0, padx=20)

        self.valid_codes_list = tk.Listbox(list_frame, bg="#2C2F33", fg="#00FF00", selectbackground="#3C3F41", height=15, width=30)
        self.valid_codes_list.grid(row=1, column=0, padx=20)

        self.invalid_codes_label = tk.Label(list_frame, text="Códigos Inválidos", font=self.label_font, bg="#2C2F33", fg="#FF0000")
        self.invalid_codes_label.grid(row=0, column=1, padx=20)

        self.invalid_codes_list = tk.Listbox(list_frame, bg="#2C2F33", fg="#FF0000", selectbackground="#3C3F41", height=15, width=30)
        self.invalid_codes_list.grid(row=1, column=1, padx=20)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        try:
            with open(file_path, "rb") as file:
                response = requests.post("http://127.0.0.1:8000/GS1-128/", files={"file": file})
            
            if response.status_code == 200:
                results = response.json()
                # La respuesta ahora tiene el formato {"total_codes": X, "results": [...]}
                valid_codes = []
                invalid_codes = []
                
                for result in results["results"]:
                    if result["is_valid"]:
                        valid_codes.append(result["code"])
                    else:
                        invalid_codes.append(result["code"])
                
                self.display_results(valid_codes, invalid_codes)
            else:
                messagebox.showerror("Error", f"Error en la conexión con la API: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error procesando el archivo: {str(e)}")

    def display_results(self, valid_codes, invalid_codes):
        # Limpiar las listas primero
        self.valid_codes_list.delete(0, tk.END)
        self.invalid_codes_list.delete(0, tk.END)

        # Mostrar el total de códigos
        self.valid_codes_label.config(text=f"Códigos Válidos ({len(valid_codes)})")
        self.invalid_codes_label.config(text=f"Códigos Inválidos ({len(invalid_codes)})")

        # Insertar los códigos en las listas
        for code in valid_codes:
            self.valid_codes_list.insert(tk.END, code)

        for code in invalid_codes:
            self.invalid_codes_list.insert(tk.END, code)

if __name__ == "__main__":
    root = tk.Tk()
    app = GS1ValitorApp(root)
    root.mainloop()
