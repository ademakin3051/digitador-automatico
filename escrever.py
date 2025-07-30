import tkinter as tk
from tkinter import messagebox, ttk
from pynput.keyboard import Controller
import time
import threading

class DigitadorAutomatico:
    def __init__(self, root):
        self.root = root
        self.root.title("Digitador Automático - VS Code")
        self.root.geometry("600x500")
        
        # Configuração do teclado virtual
        self.keyboard = Controller()
        
        # Variável para controle da thread
        self.digitando = False
        
        # Criar interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto
        ttk.Label(main_frame, text="Digite seu texto abaixo:").pack(pady=5)
        
        self.texto_entrada = tk.Text(
            main_frame,
            height=15,
            width=70,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.texto_entrada.pack(fill=tk.BOTH, expand=True)
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        # Velocidade de digitação
        ttk.Label(control_frame, text="Velocidade (ms):").grid(row=0, column=0, padx=5)
        self.velocidade = tk.IntVar(value=50)
        ttk.Spinbox(
            control_frame,
            from_=10,
            to=500,
            increment=10,
            textvariable=self.velocidade,
            width=5
        ).grid(row=0, column=1, padx=5)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Iniciar Digitação",
            command=self.iniciar_digitacao
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Parar",
            command=self.parar_digitacao
        ).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status = ttk.Label(main_frame, text="Pronto")
        self.status.pack(pady=5)
    
    def iniciar_digitacao(self):
        if self.digitando:
            return
            
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite algo antes de iniciar")
            return
        
        messagebox.showinfo(
            "Preparar",
            "Posicione o cursor no local de digitação em 5 segundos...\n\n"
            "Mantenha o mouse sobre a janela de destino."
        )
        
        # Usar thread para não travar a interface
        self.digitando = True
        threading.Thread(
            target=self._digitar_texto,
            args=(texto,),
            daemon=True
        ).start()
    
    def _digitar_texto(self, texto):
        time.sleep(5)  # Tempo para posicionar o cursor
        
        try:
            self.status.config(text="Digitando...")
            self.root.update()
            
            velocidade = self.velocidade.get() / 1000  # Converter para segundos
            
            for char in texto:
                if not self.digitando:
                    break
                
                if char == '\n':
                    self.keyboard.press('\n')
                    self.keyboard.release('\n')
                else:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
                
                time.sleep(velocidade)
            
            self.status.config(text="Concluído" if self.digitando else "Interrompido")
            self.digitando = False
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
            self.status.config(text="Erro")
            self.digitando = False
    
    def parar_digitacao(self):
        self.digitando = False
        self.status.config(text="Interrompido pelo usuário")

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitadorAutomatico(root)
    
    # Centralizar janela
    window_width = 600
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    root.mainloop()