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
IMAGE_EXTENSION = '.png'  # Assumindo que as imagens são .png

# --- Lógica de Processamento de Imagem ---

class ImageProcessor:
    """Classe responsável por operações de imagem."""

    @staticmethod
    def get_average_hsv(image_path: str) -> np.ndarray | None:
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
                print(f"Classe '{class_name}' treinada com {len(hsv_values)} imagens.")
        
        if not self.color_patterns:
            raise RuntimeError("Treinamento falhou. Nenhuma imagem de treino foi encontrada ou processada.")
        
        print("Treinamento concluído.")
        return self.color_patterns


class EggClassifier:
    """Responsável por classificar uma nova imagem de ovo."""

    def __init__(self, color_patterns: dict):
        self.color_patterns = color_patterns

    def classify(self, image_path: str) -> str | None:
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
        with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, image_path, prediction])


# --- Interface Gráfica ---

class Application(tk.Tk):
    """Classe principal da aplicação com interface gráfica."""

    def __init__(self, trainer: EggTrainer, classifier: EggClassifier, logger: ResultLogger):
        super().__init__()
        self.trainer = trainer
        self.classifier = classifier
        self.logger = logger

        self.title("Analisador de Cozimento de Ovos")
        self.geometry("600x550")
        self.configure(bg="#f0f0f0")

        self._create_widgets()

    def _create_widgets(self):
        """Cria os componentes visuais da interface."""
        style = ttk.Style(self)
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
        style.configure("TButton", font=("Helvetica", 10), padding=5)

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # --- Seção de Informações do Treino ---
        train_info_frame = ttk.LabelFrame(main_frame, text="Informações do Treinamento", padding="15")
        train_info_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(train_info_frame, text=f"Imagens por classe: {IMAGE_COUNT_PER_CLASS}").pack(anchor="w")
        ttk.Label(train_info_frame, text="Padrões de Cor (HSV Médio):").pack(anchor="w", pady=(10, 5))

        for class_name, hsv in self.trainer.color_patterns.items():
            h, s, v = hsv
            info = f"- {class_name}: H={h:.1f}, S={s:.1f}, V={v:.1f}"
            ttk.Label(train_info_frame, text=info).pack(anchor="w")

        # --- Seção de Teste ---
        test_frame = ttk.LabelFrame(main_frame, text="Analisar Nova Imagem", padding="15")
        test_frame.pack(expand=True, fill="both")

        self.load_button = ttk.Button(test_frame, text="Carregar Imagem", command=self.load_and_classify_image)
        self.load_button.pack(pady=(0, 15))

        self.image_label = ttk.Label(test_frame, text="Nenhuma imagem carregada", anchor="center")
        self.image_label.pack(expand=True, fill="both", pady=5)

        self.result_label = ttk.Label(test_frame, text="Resultado: -", font=("Helvetica", 12, "bold"), anchor="center")
        self.result_label.pack(pady=(10, 0))

    def load_and_classify_image(self):
        """Abre um diálogo para o usuário selecionar uma imagem e a classifica."""
        filepath = filedialog.askopenfilename(
            title="Selecione uma imagem de ovo",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png"), ("Todos os arquivos", "*.*")]
        )
        if not filepath:
            return

        # Classifica a imagem
        prediction = self.classifier.classify(filepath)
        if prediction:
            self.result_label.config(text=f"Resultado: {prediction}")
            self.logger.log(filepath, prediction)
            messagebox.showinfo("Sucesso", f"A imagem foi classificada como: {prediction}")
        else:
            self.result_label.config(text="Resultado: Erro na análise")
            messagebox.showerror("Erro", "Não foi possível analisar a imagem.")

        # Exibe a imagem na interface
        self._display_image(filepath)

    def _display_image(self, filepath: str):
        """Redimensiona e exibe a imagem selecionada na GUI."""
        try:
            pil_image = Image.open(filepath)
            
            # Redimensiona a imagem para caber na label sem distorção
            w, h = pil_image.size
            max_size = 200
            if w > h:
                new_w = max_size
                new_h = int(h * (max_size / w))
            else:
                new_h = max_size
                new_w = int(w * (max_size / h))
            
            pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image, text="")
        except Exception as e:
            self.image_label.config(text="Erro ao exibir imagem", image="")
            print(f"Erro ao exibir imagem: {e}")


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
        messagebox.showerror("Erro Crítico", str(e))
        print(f"Erro: {e}")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado: {e}")
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
