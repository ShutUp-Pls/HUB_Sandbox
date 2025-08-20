import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class EncryptedTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Encriptado")
        self.text_area = tk.Text(root, wrap="word")
        self.text_area.pack(expand=1, fill="both")
        
        # Menú
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        root.config(menu=menu_bar)
        
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Genera una clave de encriptación basada en una contraseña y sal"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())
    
    def encrypt(self, plaintext: str, password: str) -> bytes:
        """Encripta el texto plano usando la contraseña proporcionada"""
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self.derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        # Concatenamos salt + iv + texto cifrado
        return base64.b64encode(salt + iv + ciphertext)
    
    def decrypt(self, encrypted_data: bytes, password: str) -> str:
        """Desencripta el texto cifrado usando la contraseña proporcionada"""
        encrypted_data = base64.b64decode(encrypted_data)
        salt, iv, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
        key = self.derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".eni", 
                                               filetypes=[("Encrypted information files", "*.eni")])
        if file_path:
            password = simpledialog.askstring("Contraseña", "Ingrese la contraseña de desencriptado:", show="*")
            try:
                with open(file_path, "rb") as file:
                    encrypted_data = file.read()
                    decrypted_data = self.decrypt(encrypted_data, password)
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, decrypted_data.decode())
                messagebox.showinfo("Abrir archivo", "Archivo desencriptado y cargado con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al desencriptar el archivo: {str(e)}")
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".eni", 
                                                 filetypes=[("Encrypted information files", "*.eni")])
        if file_path:
            password = simpledialog.askstring("Contraseña", "Ingrese la contraseña para encriptar:", show="*")
            try:
                plaintext = self.text_area.get(1.0, tk.END)
                encrypted_data = self.encrypt(plaintext, password)
                with open(file_path, "wb") as file:
                    file.write(encrypted_data)
                messagebox.showinfo("Guardar archivo", "Archivo encriptado y guardado con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al encriptar el archivo: {str(e)}")

# Configuración de la ventana principal
root = tk.Tk()
app = EncryptedTextEditor(root)
root.mainloop()
