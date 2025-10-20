# 🥚 Analisador de Cozimento de Ovos

Sistema inteligente de classificação de ovos (mole, ao ponto e passado) baseado em análise de cores usando visão computacional.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Funcionamento Técnico](#-funcionamento-técnico)
- [Dependências](#-dependências)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Sobre o Projeto

Este projeto implementa um classificador de ovos cozidos que:

1. **Treina** um modelo analisando 6 imagens de cada classe de ovo (mole, ao ponto, passado)
2. **Classifica** novas imagens baseando-se em padrões de cor no espaço HSV
3. **Registra** todos os resultados em um arquivo CSV com data e hora
4. **Exibe** uma interface gráfica minimalista para facilitar o uso

### Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação
- **OpenCV**: Processamento de imagens
- **Tkinter**: Interface gráfica nativa do Python
- **NumPy**: Operações matemáticas e arrays
- **Pillow (PIL)**: Manipulação de imagens para exibição

---

## 🔧 Pré-requisitos

### Sistema Operacional

- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 20.04+ ou similar)

### Python

Você precisa ter o **Python 3.8 ou superior** instalado. Verifique com:

```bash
python --version
```

ou

```bash
python3 --version
```

Se não tiver Python instalado, baixe em: [https://www.python.org/downloads/](https://www.python.org/downloads/)

**⚠️ Importante no Windows**: Durante a instalação, marque a opção "Add Python to PATH"

---

## 📁 Estrutura do Projeto

```
comp6cg02/
│
├── main.py                    # Código principal da aplicação
├── README.md                  # Este arquivo
├── resultados.csv             # Criado automaticamente ao classificar imagens
│
├── images/                    # Pasta de imagens
│   ├── base/                  # ⭐ Imagens de TREINAMENTO (coloque suas 18 imagens aqui)
│   │   ├── ovo-mole-01.png    # 6 imagens de ovos moles
│   │   ├── ovo-mole-02.png
│   │   ├── ... (até 06)
│   │   ├── ovo-ponto-01.png   # 6 imagens de ovos ao ponto
│   │   ├── ... (até 06)
│   │   ├── ovo-passado-01.png # 6 imagens de ovos passados
│   │   └── ... (até 06)
│   │
│   └── test/                  # 📂 Pasta para imagens de TESTE (criada automaticamente)
│                              #    Você pode colocar imagens aqui ou carregar de qualquer lugar
│
└── .venv/                     # Ambiente virtual (criado na instalação)
    └── ...
```

### 📌 Importante sobre as Pastas de Imagens

- **`images/base/`**: Esta pasta contém as **imagens de treinamento** que o sistema usa para aprender os padrões de cor de cada classe de ovo. Você **deve** colocar suas 18 imagens aqui antes de executar o programa pela primeira vez.

- **`images/test/`**: Esta pasta é criada automaticamente e serve como sugestão para você organizar as imagens que deseja testar. **Não é obrigatório** colocar imagens aqui - ao clicar em "Carregar Imagem", você pode selecionar arquivos de qualquer local do seu computador.

---

## 🚀 Instalação

### Passo 1: Clone ou Baixe o Projeto

Se você recebeu o projeto como ZIP, extraia-o. Se está no Git:

```bash
git clone <url-do-repositorio>
cd comp6cg02
```

### Passo 2: Prepare as Imagens de Treinamento

**⚠️ PASSO CRÍTICO**: Coloque suas **18 imagens de treino** (6 de cada classe) na pasta `images/base/` seguindo a nomenclatura exata:

- `ovo-mole-01.png` até `ovo-mole-06.png`
- `ovo-ponto-01.png` até `ovo-ponto-06.png`
- `ovo-passado-01.png` até `ovo-passado-06.png`

**Formatos aceitos**: `.jpg`, `.jpeg`, `.png`

**⚠️ Nota**: O código está configurado para usar extensão `.png`. Se suas imagens tiverem extensão diferente (ex: `.jpg`), edite a linha 24 do arquivo `main.py`:

```python
IMAGE_EXTENSION = '.jpg'  # Mude aqui se necessário
```

### Passo 3: Crie um Ambiente Virtual (Recomendado)

Um ambiente virtual isola as dependências do projeto, evitando conflitos com outros projetos Python.

#### No Windows:

```bash
python -m venv .venv
```

#### No macOS/Linux:

```bash
python3 -m venv .venv
```

### Passo 4: Ative o Ambiente Virtual

#### No Windows (CMD):

```bash
.venv\Scripts\activate
```

#### No Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

**⚠️ Erro no PowerShell?** Execute antes:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### No macOS/Linux:

```bash
source .venv/bin/activate
```

**✅ Como saber se está ativado?** Você verá `(.venv)` no início da linha do terminal.

### Passo 5: Instale as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install opencv-python-headless==4.8.1.78 numpy==1.24.3 Pillow==10.1.0
```

**Por que essas versões?**

- **opencv-python-headless 4.8.1.78**: Versão estável do OpenCV sem dependências GUI extras (mais leve)
- **numpy 1.24.3**: Compatível com OpenCV e estável para operações matemáticas
- **Pillow 10.1.0**: Versão recente com suporte a Python 3.8-3.12

**Alternativa**: Se preferir instalar as versões mais recentes:

```bash
pip install opencv-python-headless numpy Pillow
```

### Passo 6: Verifique a Instalação

```bash
pip list
```

Você deve ver algo como:

```
Package                 Version
----------------------- -----------
numpy                   1.24.3
opencv-python-headless  4.8.1.78
Pillow                  10.1.0
pip                     23.x.x
...
```

---

## 💻 Como Usar

### 1. Execute o Programa

Com o ambiente virtual ativado:

```bash
python main.py
```

### 2. Interface Principal

Ao executar, você verá:

- **Informações do Treinamento**: Quantas imagens foram processadas por classe
- **Lista de Classes**: As três classes de ovos reconhecidas pelo sistema
- **Área de Visualização**: Espaço para exibir a imagem carregada
- **Resultado**: Classificação da última imagem analisada
- **Botão "📁 Carregar Imagem"**: Para selecionar uma imagem de ovo para classificar
- **Botão "📊 Ver Resultados (CSV)"**: Para abrir uma janela com o histórico de todas as classificações

### 3. Classificar uma Nova Imagem

1. Clique em **"📁 Carregar Imagem"**
2. Selecione uma foto de ovo (pode estar em qualquer pasta do seu computador, não precisa estar em `images/test/`)
3. O sistema irá:
   - Analisar a imagem baseando-se nos padrões de cor aprendidos
   - Exibir a imagem redimensionada na interface
   - Mostrar o resultado da classificação
   - Salvar automaticamente o resultado no arquivo `resultados.csv` com:
     - Data e hora da análise
     - Caminho relativo da imagem (calculado a partir da pasta do projeto)
     - Classe prevista (Ovo Mole, Ovo ao Ponto ou Ovo Passado)

### 4. Visualizar Histórico de Resultados

1. Clique em **"📊 Ver Resultados (CSV)"**
2. Uma nova janela abrirá mostrando todos os resultados em formato de tabela
3. Você pode:
   - Visualizar todos os registros de classificações anteriores
   - Rolar a tabela verticalmente e horizontalmente
   - Fechar a janela quando terminar (clique no X ou no botão "Fechar")

### 5. Sair do Programa

Feche a janela principal ou pressione `Alt+F4` (Windows) / `Cmd+Q` (macOS).

### 6. Desativar o Ambiente Virtual

Quando terminar de usar o programa:

```bash
deactivate
```

---

## 🧠 Funcionamento Técnico

### Etapa 1: Treinamento

O sistema lê as 18 imagens da pasta `images/base/` e:

1. Converte cada imagem do espaço BGR (padrão do OpenCV) para **HSV** (Hue-Saturation-Value)
   - **Por quê HSV?** É mais robusto a variações de iluminação do que RGB
   - **H (Hue)**: Representa a cor pura (0-180 no OpenCV)
   - **S (Saturation)**: Representa a intensidade da cor (0-255)
   - **V (Value)**: Representa o brilho (0-255)
2. Calcula a média dos valores H, S e V de todos os pixels de cada imagem
3. Para cada classe, calcula a média das 6 médias individuais, resultando em um "padrão de cor" representativo da classe

**Exemplo de saída no console**:
```
Iniciando treinamento...
Classe 'Ovo Mole' treinada com 6 imagens.
Classe 'Ovo ao Ponto' treinada com 6 imagens.
Classe 'Ovo Passado' treinada com 6 imagens.
Treinamento concluído.
```

### Etapa 2: Classificação

Quando você carrega uma nova imagem:

1. O sistema extrai o padrão de cor HSV médio da nova imagem
2. Calcula a **distância euclidiana** entre esse padrão e os 3 padrões aprendidos no treinamento
3. Classifica a imagem como pertencente à classe com a **menor distância**

**Fórmula da distância euclidiana**:
```
distância = √((H₁-H₂)² + (S₁-S₂)² + (V₁-V₂)²)
```

Quanto menor a distância, mais similar é a cor média da imagem teste à cor média da classe.

### Etapa 3: Registro

Os resultados são salvos automaticamente em `resultados.csv` no formato:

| data_processamento | caminho_imagem | resultado_previsto |
|-------------------|----------------|-------------------|
| 2024-01-15 14:30:25 | images\test\ovo-teste.png | Ovo Mole |
| 2024-01-15 14:32:10 | C:\Users\...\Desktop\foto.jpg | Ovo ao Ponto |

- **data_processamento**: Timestamp no formato `YYYY-MM-DD HH:MM:SS`
- **caminho_imagem**: Caminho relativo quando possível, absoluto quando em drives diferentes
- **resultado_previsto**: Classe prevista pelo classificador

---

## 📦 Dependências

### Bibliotecas Python Externas

| Biblioteca | Versão Recomendada | Finalidade |
|------------|-------------------|------------|
| opencv-python-headless | 4.8.1.78 | Leitura de imagens, conversão BGR→HSV, processamento |
| numpy | 1.24.3 | Operações matemáticas (média, norma euclidiana) |
| Pillow (PIL) | 10.1.0 | Redimensionamento de imagens para exibição na GUI |

### Bibliotecas Padrão do Python (já inclusas)

- **tkinter**: Interface gráfica (vem com Python)
- **csv**: Leitura e escrita de arquivos CSV
- **os**: Operações com sistema de arquivos (paths, verificação de existência)
- **datetime**: Manipulação de datas e horas para timestamps

---

## 🐛 Troubleshooting

### Erro: "No module named 'cv2'"

**Solução**: O OpenCV não foi instalado corretamente.

```bash
pip install opencv-python-headless
```

### Erro: "No module named 'PIL'"

**Solução**: Pillow não está instalado.

```bash
pip install Pillow
```

### Erro: "Treinamento falhou. Nenhuma imagem de treino foi encontrada"

**Causas possíveis**:

1. **Pasta `images/base/` não existe**: Crie a pasta manualmente na raiz do projeto
2. **Nomenclatura incorreta**: Verifique se os arquivos seguem o padrão **exato**:
   - `ovo-mole-01.png` (não `ovo_mole_01.png`, `ovo-mole-1.png` ou `ovomole01.png`)
   - Use números com **dois dígitos**: `01`, `02`, ..., `06`
3. **Extensão diferente**: Se suas imagens são `.jpg`, altere a linha 24 do `main.py`:
   ```python
   IMAGE_EXTENSION = '.jpg'
   ```
4. **Imagens corrompidas**: Tente abrir as imagens em um visualizador de imagens para verificar se estão válidas

### Erro: "_tkinter.TclError" no Linux

**Solução**: Instale o Tkinter:

```bash
sudo apt-get install python3-tk
```

### Imagens não aparecem na interface

**Causas e soluções**:

1. **Pillow não instalado**:
   ```bash
   pip install Pillow --upgrade
   ```

2. **Formato de imagem não suportado**: Converta a imagem para JPG ou PNG

3. **Imagem muito grande**: O programa redimensiona automaticamente, mas arquivos extremamente grandes podem causar problemas

### Resultados inconsistentes na classificação

**Possíveis causas e soluções**:

1. **Iluminação muito diferente**: As imagens de treino e teste devem ter iluminação similar. Tire fotos sob as mesmas condições de luz.

2. **Poucas imagens de treino**: 6 imagens por classe é o mínimo funcional. Para melhor precisão, considere usar mais imagens (modifique `IMAGE_COUNT_PER_CLASS` no código).

3. **Variação dentro da mesma classe**: Certifique-se de que as 6 imagens de cada classe são realmente representativas e similares entre si.

4. **Fundo das imagens**: Tente usar um fundo neutro (branco ou cinza) para reduzir interferências na análise de cor.

### A interface trava ou não responde

**Solução**: Isso pode acontecer com imagens muito grandes. O programa processa toda a imagem para calcular a média de cores. Tente:

1. Redimensionar as imagens de teste para um tamanho menor (ex: 800x600)
2. Garantir que as imagens não estão corrompidas
3. Verificar se o ambiente virtual está ativado corretamente

---

## 🎨 Arquitetura do Código

O código segue os princípios **SOLID**:

- **S** (Single Responsibility): Cada classe tem uma única responsabilidade
  - `ImageProcessor`: Processamento de imagens e extração de características
  - `EggTrainer`: Treinamento do modelo (cálculo dos padrões de cor)
  - `EggClassifier`: Classificação de novas imagens
  - `ResultLogger`: Persistência de resultados em CSV
  - `ResultsViewer`: Janela de visualização de histórico
  - `Application`: Interface gráfica principal

- **O** (Open/Closed): Extensível sem modificar código existente
- **L** (Liskov Substitution): Classes seguem contratos bem definidos
- **I** (Interface Segregation): Métodos focados e específicos
- **D** (Dependency Inversion): Dependências passadas via construtor (Dependency Injection)

### Padrões de Código Aplicados

- **PEP 8**: Estilo de código Python oficial
- **Type hints**: Anotações de tipo para melhor documentação e detecção de erros
- **Docstrings**: Cada classe e método possui documentação
- **Comentários explicativos**: Focados no "porquê" das decisões técnicas

### Possíveis Melhorias Futuras

- Adicionar mais espaços de cor (LAB, YCrCb) para comparação
- Implementar validação cruzada no treinamento
- Adicionar suporte a múltiplos modelos (SVM, KNN)
- Criar visualização dos padrões de cor aprendidos
- Adicionar opção de retreinamento sem reiniciar o programa

---

## 📝 Licença

Este projeto é de uso educacional.

---

## 👨‍💻 Autor

Desenvolvido para o projeto `comp6cg02`.

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique a seção [Troubleshooting](#-troubleshooting)
2. Confirme que todas as dependências foram instaladas corretamente (`pip list`)
3. Verifique se o ambiente virtual está ativado (`(.venv)` aparece no terminal)
4. Revise a estrutura de pastas e nomenclatura dos arquivos de treino
5. Teste com imagens de diferentes formatos e tamanhos

**Bom uso! 🥚✨**
