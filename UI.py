import tkinter as tk
from tkinter import messagebox
from encrypt import generar_clave, cargar_contraseñas, guardar_contraseñas, encriptar, desencriptar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas")
        self.root.geometry("500x400")  # Tamaño inicial de la ventana
        self.contraseñas = {}
        self.clave = None
        self.salt = None

        # Estilos personalizados
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))

        # Ventana de autenticación
        self.ventana_autenticacion()

    def ventana_autenticacion(self):
        self.limpiar_ventana()
        ttk.Label(self.root, text="Ingrese su contraseña maestra:", bootstyle=PRIMARY).pack(pady=10)
        self.entrada_contraseña = ttk.Entry(self.root, show="*", bootstyle=PRIMARY)
        self.entrada_contraseña.pack(pady=10)
        ttk.Button(self.root, text="Acceder", command=self.autenticar, bootstyle=SUCCESS).pack(pady=10)

    def autenticar(self):
        contraseña = self.entrada_contraseña.get()
        self.salt, self.contraseñas = cargar_contraseñas()

        # Si no hay sal (primera ejecución), generar una nueva
        if not self.salt:
            self.salt = os.urandom(16)

        self.clave = generar_clave(contraseña, self.salt)
        self.ventana_principal()

    def ventana_principal(self):
        self.limpiar_ventana()
        ttk.Label(self.root, text="Gestor de Contraseñas", bootstyle=PRIMARY, font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(self.root, text="Agregar Contraseña", command=self.ventana_agregar, bootstyle=INFO).pack(pady=10)
        ttk.Button(self.root, text="Ver Contraseñas", command=self.ventana_ver, bootstyle=WARNING).pack(pady=10)

    def ventana_agregar(self):
        self.limpiar_ventana()
        ttk.Label(self.root, text="Agregar Nueva Contraseña", bootstyle=PRIMARY, font=("Helvetica", 14)).pack(pady=10)

        ttk.Label(self.root, text="Servicio (ej. Gmail):", bootstyle=PRIMARY).pack(pady=5)
        self.servicio_entry = ttk.Entry(self.root, bootstyle=PRIMARY)
        self.servicio_entry.pack(pady=5)

        ttk.Label(self.root, text="Usuario:", bootstyle=PRIMARY).pack(pady=5)
        self.usuario_entry = ttk.Entry(self.root, bootstyle=PRIMARY)
        self.usuario_entry.pack(pady=5)

        ttk.Label(self.root, text="Contraseña:", bootstyle=PRIMARY).pack(pady=5)
        self.contraseña_entry = ttk.Entry(self.root, show="*", bootstyle=PRIMARY)
        self.contraseña_entry.pack(pady=5)

        ttk.Button(self.root, text="Guardar", command=self.guardar_contraseña, bootstyle=SUCCESS).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.ventana_principal, bootstyle=DANGER).pack(pady=10)

    def guardar_contraseña(self):
        servicio = self.servicio_entry.get()
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()

        if servicio and usuario and contraseña:
            contraseña_encriptada = encriptar(contraseña, self.clave)
            self.contraseñas[servicio] = {
                "usuario": usuario,
                "contraseña": contraseña_encriptada.decode()  # Convertir bytes a str
            }
            guardar_contraseñas(self.contraseñas, self.salt)
            messagebox.showinfo("Éxito", "Contraseña guardada correctamente.")
            self.ventana_principal()
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    def ventana_ver(self):
        self.limpiar_ventana()
        ttk.Label(self.root, text="Ver Contraseñas", bootstyle=PRIMARY, font=("Helvetica", 14)).pack(pady=10)

        # Ventana de verificación de contraseña maestra
        ttk.Label(self.root, text="Ingrese su contraseña maestra para ver las contraseñas:", bootstyle=PRIMARY).pack(pady=5)
        self.verificacion_entry = ttk.Entry(self.root, show="*", bootstyle=PRIMARY)
        self.verificacion_entry.pack(pady=5)
        ttk.Button(self.root, text="Verificar", command=self.verificar_contraseña_ver, bootstyle=SUCCESS).pack(pady=10)

    def verificar_contraseña_ver(self):
        contraseña_ingresada = self.verificacion_entry.get()
        clave_verificacion = generar_clave(contraseña_ingresada, self.salt)

        # Verificar si la clave generada coincide con la clave maestra
        if clave_verificacion == self.clave:
            self.mostrar_contraseñas()
        else:
            messagebox.showerror("Error", "Contraseña maestra incorrecta.")

    def mostrar_contraseñas(self):
        self.limpiar_ventana()
        ttk.Label(self.root, text="Contraseñas Guardadas", bootstyle=PRIMARY, font=("Helvetica", 14)).pack(pady=10)

        for servicio, datos in self.contraseñas.items():
            # Convertir la contraseña encriptada de str a bytes
            contraseña_encriptada = datos["contraseña"].encode()

            # Desencriptar la contraseña
            contraseña_desencriptada = desencriptar(contraseña_encriptada, self.clave)

            # Mostrar los datos en la interfaz
            ttk.Label(self.root, text=f"Servicio: {servicio}", bootstyle=PRIMARY).pack(pady=5)
            ttk.Label(self.root, text=f"Usuario: {datos['usuario']}", bootstyle=PRIMARY).pack(pady=5)
            ttk.Label(self.root, text=f"Contraseña: {contraseña_desencriptada}", bootstyle=PRIMARY).pack(pady=5)

        # Botón para volver a la ventana principal
        ttk.Button(self.root, text="Volver", command=self.ventana_principal, bootstyle=DANGER).pack(pady=10)

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()