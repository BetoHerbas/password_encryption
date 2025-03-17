import tkinter as tk
from tkinter import messagebox
from encrypt import generar_clave, cargar_contraseñas, guardar_contraseñas, encriptar, desencriptar
import os

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas")
        self.contraseñas = {}
        self.clave = None
        self.salt = None

        self.ventana_autenticacion()

    def ventana_autenticacion(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Ingrese su contraseña maestra:").pack()
        self.entrada_contraseña = tk.Entry(self.root, show="*")
        self.entrada_contraseña.pack()
        tk.Button(self.root, text="Acceder", command=self.autenticar).pack()

    def autenticar(self):
        contraseña = self.entrada_contraseña.get()
        self.salt, self.contraseñas = cargar_contraseñas()

        if not self.salt:
            self.salt = os.urandom(16)

        self.clave = generar_clave(contraseña, self.salt)
        self.ventana_principal()

    def ventana_principal(self):
        self.limpiar_ventana()
        tk.Button(self.root, text="Agregar Contraseña", command=self.ventana_agregar).pack()
        tk.Button(self.root, text="Ver Contraseñas", command=self.ventana_ver).pack()

    def ventana_agregar(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Servicio (ej. Gmail):").pack()
        self.servicio_entry = tk.Entry(self.root)
        self.servicio_entry.pack()

        tk.Label(self.root, text="Usuario:").pack()
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack()

        tk.Label(self.root, text="Contraseña:").pack()
        self.contraseña_entry = tk.Entry(self.root, show="*")
        self.contraseña_entry.pack()

        tk.Button(self.root, text="Guardar", command=self.guardar_contraseña).pack()
        tk.Button(self.root, text="Volver", command=self.ventana_principal).pack()

    def guardar_contraseña(self):
        servicio = self.servicio_entry.get()
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()

        if servicio and usuario and contraseña:
            contraseña_encriptada = encriptar(contraseña, self.clave)
            self.contraseñas[servicio] = {
                "usuario": usuario,
                "contraseña": contraseña_encriptada.decode()  
            }
            guardar_contraseñas(self.contraseñas, self.salt)
            messagebox.showinfo("Éxito", "Contraseña guardada correctamente.")
            self.ventana_principal()
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    def ventana_ver(self):
        self.limpiar_ventana()

        tk.Label(self.root, text="Ingrese su contraseña maestra para ver las contraseñas:").pack()
        self.verificacion_entry = tk.Entry(self.root, show="*")
        self.verificacion_entry.pack()
        tk.Button(self.root, text="Verificar", command=self.verificar_contraseña_ver).pack()

    def verificar_contraseña_ver(self):
        contraseña_ingresada = self.verificacion_entry.get()
        clave_verificacion = generar_clave(contraseña_ingresada, self.salt)

        if clave_verificacion == self.clave:
            self.mostrar_contraseñas()
        else:
            messagebox.showerror("Error", "Contraseña maestra incorrecta.")

    def mostrar_contraseñas(self):
        self.limpiar_ventana()

        for servicio, datos in self.contraseñas.items():
            contraseña_encriptada = datos["contraseña"].encode()

            contraseña_desencriptada = desencriptar(contraseña_encriptada, self.clave)

            tk.Label(self.root, text=f"Servicio: {servicio}").pack()
            tk.Label(self.root, text=f"Usuario: {datos['usuario']}").pack()
            tk.Label(self.root, text=f"Contraseña: {contraseña_desencriptada}").pack()

        tk.Button(self.root, text="Volver", command=self.ventana_principal).pack()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()