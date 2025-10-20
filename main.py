import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

# --- Constantes e Configurações ---

# Diretórios para imagens de treino e teste
BASE_IMAGE_PATH = 'images/base'
TEST_IMAGE_PATH = 'images/test'
RESULTS_FILE = 'resultados.csv'

# Classes de ovos e seus prefixos de arquivo
EGG_CLASSES = {
    'Ovo Mole': 'ovo-mole',
    'Ovo ao Ponto': 'ovo-ponto',
    'Ovo Passado': 'ovo-passado'
}
IMAGE_COUNT_PER_CLASS = 6
IMAGE_EXTENSION = '.png'

# --- Lógica de Processamento de Imagem ---

class ImageProcessor:
    """Classe responsável por operações de imagem."""

    @staticmethod
    def get_average_hsv(image_path: str):
        """
        Lê uma imagem e calcula a cor média no espaço de cores HSV.

        Args:
            image_path: O caminho para o arquivo de imagem.

        Returns:
            Um array numpy com os valores médios de H, S, V ou None se a
            imagem não puder ser lida.
        """
        if not os.path.exists(image_path):
            print(f"Aviso: Imagem não encontrada em {image_path}")
            return None
        
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Converte a imagem de BGR (padrão do OpenCV) para HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Calcula a média dos canais H, S e V
        avg_hsv = np.mean(hsv_image, axis=(0, 1))
        return avg_hsv


class EggTrainer:
    """Responsável por treinar o modelo a partir das imagens base."""

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.color_patterns = {}
        self.images_per_class = {}

    def train(self):
        """
        Processa as imagens de treino para extrair os padrões de cor médios
        para cada classe de ovo.
        """
        print("Iniciando treinamento...")
        for class_name, file_prefix in EGG_CLASSES.items():
            hsv_values = []
            for i in range(1, IMAGE_COUNT_PER_CLASS + 1):
                filename = f"{file_prefix}-{i:02d}{IMAGE_EXTENSION}"
                image_path = os.path.join(self.base_path, filename)
                
                avg_hsv = ImageProcessor.get_average_hsv(image_path)
                if avg_hsv is not None:
                    hsv_values.append(avg_hsv)
            
            if hsv_values:
                # Calcula a média dos valores HSV para a classe
                self.color_patterns[class_name] = np.mean(hsv_values, axis=0)
                self.images_per_class[class_name] = len(hsv_values)
                print(f"Classe '{class_name}' treinada com {len(hsv_values)} imagens.")
            else:
                self.images_per_class[class_name] = 0
        
        if not self.color_patterns:
            raise RuntimeError(
                "Treinamento falhou. Nenhuma imagem de treino foi encontrada ou processada.\n"
                f"Verifique se as imagens estão em: {os.path.abspath(self.base_path)}"
            )
        
        print("Treinamento concluído.")
        return self.color_patterns


class EggClassifier:
    """Responsável por classificar uma nova imagem de ovo."""

    def __init__(self, color_patterns: dict):
        self.color_patterns = color_patterns

    def classify(self, image_path: str):
        """
        Classifica uma imagem com base na proximidade com os padrões de cor.

        Args:
            image_path: O caminho para a imagem de teste.

        Returns:
            O nome da classe prevista ou None se a classificação falhar.
        """
        avg_hsv = ImageProcessor.get_average_hsv(image_path)
        if avg_hsv is None:
            return None

        min_distance = float('inf')
        predicted_class = None

        for class_name, pattern_hsv in self.color_patterns.items():
            # Calcula a distância euclidiana no espaço de cores HSV
            distance = np.linalg.norm(avg_hsv - pattern_hsv)
            if distance < min_distance:
                min_distance = distance
                predicted_class = class_name
        
        return predicted_class


class ResultLogger:
    """Responsável por registrar os resultados da classificação em um CSV."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._initialize_file()

    def _initialize_file(self):
        """Cria o arquivo CSV com cabeçalho se ele não existir."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['data_processamento', 'caminho_imagem', 'resultado_previsto'])

    def log(self, image_path: str, prediction: str):
        """
        Adiciona uma nova entrada de log ao arquivo CSV.
        
        Args:
            image_path: Caminho da imagem de teste.
            prediction: A classe prevista pelo classificador.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Converte para caminho relativo a partir da raiz do projeto
        try:
            project_root = os.path.dirname(os.path.abspath(__file__))
            rel_path = os.path.relpath(image_path, project_root)
        except ValueError:
            # Em Windows, se estiver em drives diferentes, usa caminho absoluto
            rel_path = image_path
        
        with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, rel_path, prediction])
    
    def read_all(self):
        """
        Lê todos os registros do arquivo CSV.
        
        Returns:
            Uma lista de listas contendo os dados do CSV.
        """
        if not os.path.exists(self.filepath):
            return []
        
        with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)


# --- Interface Gráfica ---

class ResultsViewer(tk.Toplevel):
    """Janela separada para visualizar os resultados do CSV."""
    
    def __init__(self, parent, logger: ResultLogger):
        super().__init__(parent)
        self.logger = logger
        
        self.title("Histórico de Resultados")
        self.geometry("900x450")
        self.configure(bg="#ffffff")
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        """Cria os componentes visuais da janela de resultados."""
        # Estilo minimalista
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Treeview", 
                       background="#ffffff",
                       foreground="#333333",
                       rowheight=28,
                       fieldbackground="#ffffff",
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       background="#f5f5f5",
                       foreground="#333333",
                       relief="flat",
                       font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#e3f2fd")])
        
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="Histórico de Classificações",
            font=("Segoe UI", 16, "bold"),
            foreground="#1976D2",
            background="#ffffff"
        )
        title_label.pack(pady=(0, 15))
        
        # Frame para a tabela com scrollbar
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(expand=True, fill="both")
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        
        # Treeview (tabela)
        self.tree = ttk.Treeview(
            table_frame,
            columns=("Data", "Caminho", "Resultado"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="browse"
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configuração das colunas
        self.tree.heading("Data", text="Data/Hora")
        self.tree.heading("Caminho", text="Caminho da Imagem")
        self.tree.heading("Resultado", text="Resultado")
        
        self.tree.column("Data", width=180, anchor="center")
        self.tree.column("Caminho", width=500, anchor="w")
        self.tree.column("Resultado", width=180, anchor="center")
        
        # Posicionamento
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Botão fechar
        close_btn = ttk.Button(
            main_frame,
            text="Fechar",
            command=self.destroy
        )
        close_btn.pack(pady=(15, 0))
    
    def _load_data(self):
        """Carrega os dados do CSV na tabela."""
        data = self.logger.read_all()
        
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adiciona os dados (pula o cabeçalho)
        if len(data) > 1:
            for row in data[1:]:
                if len(row) == 3:
                    self.tree.insert("", "end", values=row)
        else:
            # Adiciona mensagem se não houver dados
            self.tree.insert("", "end", values=("—", "Nenhum resultado ainda", "—"))


class Application(tk.Tk):
    """Classe principal da aplicação com interface gráfica."""

    def __init__(self, trainer: EggTrainer, classifier: EggClassifier, logger: ResultLogger):
        super().__init__()
        self.trainer = trainer
        self.classifier = classifier
        self.logger = logger
        self.current_image_ref = None  # Mantém referência da imagem

        self.title("Analisador de Ovos")
        self.geometry("520x500")
        self.configure(bg="#ffffff")
        self.resizable(False, False)

        self._create_widgets()

    def _create_widgets(self):
        """Cria os componentes visuais da interface."""
        # Configuração de estilo minimalista
        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 9), foreground="#555555")
        style.configure("Info.TLabel", background="#ffffff", font=("Segoe UI", 9), foreground="#777777")
        style.configure("Result.TLabel", font=("Segoe UI", 16, "bold"), foreground="#2196F3", background="#ffffff")
        style.configure("TButton", font=("Segoe UI", 10), padding=12)
        
        # Container principal
        main_frame = ttk.Frame(self, padding="25")
        main_frame.pack(expand=True, fill="both")

        # Título
        title = ttk.Label(
            main_frame,
            text="🥚 Analisador de Ovos",
            font=("Segoe UI", 20, "bold"),
            foreground="#1976D2",
            background="#ffffff"
        )
        title.pack(pady=(0, 25))

        # --- Informações do Treino (compacto) ---
        info_text = f"Modelo treinado com {IMAGE_COUNT_PER_CLASS} imagens por classe"
        info_label = ttk.Label(main_frame, text=info_text, style="Info.TLabel")
        info_label.pack(pady=(0, 5))
        
        classes_text = f"Classes: {', '.join(EGG_CLASSES.keys())}"
        classes_label = ttk.Label(main_frame, text=classes_text, style="Info.TLabel")
        classes_label.pack(pady=(0, 25))

        # --- Área de Imagem (com tamanho fixo) ---
        self.image_frame = tk.Frame(
            main_frame,
            bg="#f9f9f9",
            highlightbackground="#e0e0e0",
            highlightthickness=1,
            width=220,
            height=220
        )
        self.image_frame.pack(pady=(0, 20))
        self.image_frame.pack_propagate(False)  # Mantém tamanho fixo
        
        self.image_label = tk.Label(
            self.image_frame,
            text="Nenhuma imagem\ncarregada",
            font=("Segoe UI", 10),
            fg="#999999",
            bg="#f9f9f9"
        )
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Resultado ---
        self.result_label = ttk.Label(
            main_frame,
            text="",
            style="Result.TLabel"
        )
        self.result_label.pack(pady=(0, 25))

        # --- Botões ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        self.load_button = ttk.Button(
            button_frame,
            text="📁 Carregar Imagem",
            command=self.load_and_classify_image
        )
        self.load_button.pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        self.results_button = ttk.Button(
            button_frame,
            text="📊 Ver Resultados",
            command=self.show_results
        )
        self.results_button.pack(side="right", expand=True, fill="x")

    def load_and_classify_image(self):
        """Abre um diálogo para o usuário selecionar uma imagem e a classifica."""
        filepath = filedialog.askopenfilename(
            title="Selecione uma imagem de ovo",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if not filepath:
            return

        # Exibe a imagem primeiro
        success = self._display_image(filepath)
        if not success:
            self.result_label.config(text="✗ Erro ao carregar")
            messagebox.showerror("Erro", "Não foi possível carregar a imagem.")
            return

        # Classifica a imagem
        prediction = self.classifier.classify(filepath)
        if prediction:
            self.result_label.config(text=f"✓ {prediction}")
            self.logger.log(filepath, prediction)
        else:
            self.result_label.config(text="✗ Erro na análise")
            messagebox.showerror("Erro", "Não foi possível analisar a imagem.")

    def _display_image(self, filepath: str):
        """
        Redimensiona e exibe a imagem selecionada na GUI.
        
        Returns:
            True se a imagem foi carregada com sucesso, False caso contrário.
        """
        try:
            # Abre a imagem
            pil_image = Image.open(filepath)
            
            # Converte para RGB se necessário (ex: imagens RGBA)
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Redimensiona mantendo proporção
            w, h = pil_image.size
            max_size = 200
            
            if w > h:
                new_w = max_size
                new_h = int(h * (max_size / w))
            else:
                new_h = max_size
                new_w = int(w * (max_size / h))
            
            pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Converte para PhotoImage e mantém referência
            self.current_image_ref = ImageTk.PhotoImage(pil_image)
            
            # Atualiza o label
            self.image_label.config(image=self.current_image_ref, text="", bg="#f9f9f9")
            
            return True
            
        except Exception as e:
            print(f"Erro ao exibir imagem: {e}")
            self.image_label.config(
                image="",
                text="Erro ao\nexibir imagem",
                fg="#d32f2f"
            )
            self.current_image_ref = None
            return False
    
    def show_results(self):
        """Abre uma janela separada para visualizar os resultados do CSV."""
        ResultsViewer(self, self.logger)


# --- Ponto de Entrada Principal ---

def main():
    """Função principal que inicializa e executa a aplicação."""
    # Garante que o diretório de teste exista
    os.makedirs(TEST_IMAGE_PATH, exist_ok=True)

    try:
        # 1. Treinar o modelo
        trainer = EggTrainer(BASE_IMAGE_PATH)
        trainer.train()

        # 2. Inicializar o classificador com os padrões treinados
        classifier = EggClassifier(trainer.color_patterns)

        # 3. Inicializar o logger de resultados
        logger = ResultLogger(RESULTS_FILE)

        # 4. Iniciar a aplicação GUI
        app = Application(trainer, classifier, logger)
        app.mainloop()

    except RuntimeError as e:
        # Cria uma janela temporária para mostrar o erro
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro Crítico", str(e))
        root.destroy()
        print(f"Erro: {e}")
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado:\n\n{e}")
        root.destroy()
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
