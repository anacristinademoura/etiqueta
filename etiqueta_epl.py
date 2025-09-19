import socket
import os
import sys
import re
from PIL import Image, ImageDraw, ImageFont
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

# Adicione esta importação para Windows
if platform.system() == "Windows":
    import win32print
    import traceback

COUNTER_FILE = "contador_volume.txt"


def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, funcionando tanto no .py quanto no .exe"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


from PIL import Image, ImageDraw, ImageFont

from PIL import Image, ImageDraw, ImageFont

def visualizar_epl(epl, largura_pontos=640, altura_pontos=920):
    """
    Gera uma imagem de visualização prévia a partir de um código EPL.
    Aumenta o tamanho da fonte do título (identificado por h_mult=3, v_mult=2) na visualização.
    
    Args:
        epl (str): Código EPL a ser renderizado.
        largura_pontos (int): Largura da etiqueta em pontos (8 pontos/mm).
        altura_pontos (int): Altura da etiqueta em pontos (ajustado para 920).
    
    Returns:
        PIL.Image: Imagem renderizada da etiqueta.
    """
    # Cria uma imagem em branco (fundo branco, modo RGB para compatibilidade com ImageTk)
    img = Image.new("RGB", (largura_pontos, altura_pontos), "white")
    draw = ImageDraw.Draw(img)

    # Tenta carregar uma fonte TrueType para melhor renderização
    try:
        font_path = "arial.ttf"  # Substitua pelo caminho de uma fonte TrueType no seu sistema
        font_default = ImageFont.truetype(font_path, 18)  # Tamanho padrão para textos
        font_title = ImageFont.truetype(font_path, 45)    # Tamanho maior para o título
    except:
        font_default = ImageFont.load_default()  # Fallback para fonte padrão
        font_title = ImageFont.load_default()    # Fallback para título

    # Offsets para ajuste fino do alinhamento
    offset_x = -190  # Ajuste para mover textos para a direita
    offset_y = 200   # Ajuste para mover textos para baixo

    # Padding para permitir coordenadas negativas
    padding = 200  # Ajuste para cobrir offsets negativos

    # Divide o EPL em linhas e processa cada comando
    lines = epl.strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";") or line.startswith("P") or line.startswith("N") or line.startswith("q") or line.startswith("Q") or line.startswith("D") or line.startswith("S"):
            continue  # Ignora comentários, comandos de impressão e configurações

        # Comando LO (Line Or Box)
        if line.startswith("LO"):
            try:
                parts = line[2:].split(",")
                if len(parts) == 4:
                    x, y, width, height = map(int, parts)
                    # Desenha um retângulo preenchido
                    draw.rectangle(
                        [(x, y), (x + width - 1, y + height - 1)],
                        fill="black"
                    )
            except Exception as e:
                print(f"Erro ao processar comando LO: {line} ({e})")

        # Comando X (Box Draw)
        elif line.startswith("X"):
            try:
                parts = line[1:].split(",")
                if len(parts) == 5:
                    x1, y1, thickness, x2, y2 = map(int, parts)
                    # Desenha um retângulo com bordas
                    draw.rectangle(
                        [(x1, y1), (x2, y2)],
                        outline="black",
                        width=thickness
                    )
            except Exception as e:
                print(f"Erro ao processar comando X: {line} ({e})")

        # Comando A (Text)
        elif line.startswith("A"):
            try:
                parts = line[1:].split(",")
                if len(parts) >= 8:
                    x, y = int(parts[0]), int(parts[1])
                    rotation = int(parts[2])
                    font_id = int(parts[3])  # Não usado
                    h_mult = int(parts[4])   # Usado para identificar o título
                    v_mult = int(parts[5])   # Usado para identificar o título
                    reverse = parts[6]
                    text = parts[7].strip('"')

                    # Escolher fonte com base nos parâmetros (título tem h_mult=3, v_mult=2)
                    font = font_title if h_mult == 3 and v_mult == 2 else font_default

                    # Ajustar coordenadas e rotação
                    if rotation == 1:  # 90° horário
                        new_x = y + offset_x
                        new_y = largura_pontos - x + offset_y
                        angle = 270  # Rotação anti-horária para PIL
                    else:  # Sem rotação (ou outras rotações não implementadas)
                        new_x = x + offset_x
                        new_y = y + offset_y
                        angle = 0

                    # Criar imagem temporária para o texto com padding para coordenadas negativas
                    text_img = Image.new("RGBA", (largura_pontos + 2*padding, altura_pontos + 2*padding), (255, 255, 255, 0))
                    text_draw = ImageDraw.Draw(text_img)
                    fill_color = "black" if reverse == "N" else "white"
                    text_draw.text((new_x + padding, new_y + padding), text, fill=fill_color, font=font)

                    # Rotacionar o texto se necessário
                    if angle != 0:
                        text_img = text_img.rotate(angle, expand=False)

                    # Colar o texto na imagem principal com offset para padding
                    img.paste(text_img, (-padding, -padding), text_img)

            except Exception as e:
                print(f"Erro ao processar comando A: {line} ({e})")

    # Aplicar rotação global de 90° para manter a orientação das linhas
    img = img.rotate(90, expand=True)

    return img


def ler_ultimo_volume():
    """Lê o último número de volume do arquivo, retornando 0 se inválido ou não existente."""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return int(content)
                return 0
        except (ValueError, IOError) as e:
            print(f"Erro ao ler {COUNTER_FILE}: {e}")
            return 0
    return 0


def salvar_volume(volume):
    """Salva o volume com backup e retorna o próximo volume, atualizando GUI."""
    try:
        if os.path.exists(COUNTER_FILE):
            if os.path.exists(COUNTER_FILE + ".bak"):
                os.remove(COUNTER_FILE + ".bak")
            os.rename(COUNTER_FILE, COUNTER_FILE + ".bak")
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            f.write(str(volume))
        return volume + 1
    except Exception as e:
        print(f"Erro ao salvar volume: {e}")
        return volume + 1


def enviar_para_zebra(printer_name, epl, retries=3):
    if platform.system() != "Windows":
        raise NotImplementedError("Envio para impressora local apenas no Windows.")

    printers = [p[2] for p in win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
    if printer_name not in printers:
        raise ValueError(f"Impressora '{printer_name}' não encontrada. Impressoras disponíveis: {printers}")

    # Tentar encoding compatível com Windows / impressoras térmicas
    try_encodings = ["mbcs", "cp1252", "latin-1", "utf-8"]
    data = None
    for enc in try_encodings:
        try:
            data = epl.encode(enc)
            break
        except Exception:
            data = None
    if data is None:
        # fallback rígido
        data = epl.encode("utf-8", errors="replace")

    for attempt in range(retries):
        try:
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
                win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta EPL", None, "RAW"))
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, data)
                win32print.EndPagePrinter(hPrinter)
                win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            return True
        except Exception:
            print(f"Tentativa {attempt + 1}/{retries} falhou:")
            traceback.print_exc()
            if attempt == retries - 1:
                return False


def montar_epl(d, largura_pontos=640, altura_pontos=920, grade="10/12/14/16"):
    # Deslocamentos para mover um pouco para a direita e para baixo
    offset_x = 70  # Move pontos para a direita
    offset_y = 0   # Move pontos para baixo

    # Definir os tamanhos com base na grade selecionada
    if grade == "1/2/3":
        tamanhos = ["1", "2", "3"]
        num_colunas = 3
    elif grade == "4/5/6":
        tamanhos = ["4", "5", "6"]
        num_colunas = 3
    elif grade == "P/M/G":
        tamanhos = ["P", "M", "G"]
        num_colunas = 3
    else:  # "10/12/14/16"
        tamanhos = ["10", "12", "14", "16"]
        num_colunas = 4

    # Base do EPL
    epl = f"""
N
q{largura_pontos}
Q{altura_pontos},24
D10
S2

; --- Moldura externa com 4 LO ---
LO{0 + offset_x},{80 + offset_y},540,3
LO{0 + offset_x},{890 + offset_y},540,3
LO{0 + offset_x},{80 + offset_y},3,810
LO{538 + offset_x},{80 + offset_y},3,810
X{0 + offset_x},{80 + offset_y},3,{540 + offset_x},{890 + offset_y}
"""

    # Linhas horizontais internas
    if num_colunas == 4:
        epl += f"""
; ===== Linhas horizontais internas =====
LO{0 + offset_x},{300 + offset_y},540,3
LO{0 + offset_x},{500 + offset_y},400,3
LO{450 + offset_x},{500 + offset_y},90,3
LO{0 + offset_x},{650 + offset_y},400,3
LO{450 + offset_x},{650 + offset_y},90,3
LO{0 + offset_x},{710 + offset_y},400,3
LO{0 + offset_x},{770 + offset_y},400,3
LO{0 + offset_x},{830 + offset_y},400,3
"""
    else:  # 3 colunas
        epl += f"""
; ===== Linhas horizontais internas =====
LO{0 + offset_x},{300 + offset_y},540,3
LO{0 + offset_x},{500 + offset_y},400,3
LO{450 + offset_x},{500 + offset_y},90,3
LO{0 + offset_x},{650 + offset_y},400,3
LO{450 + offset_x},{650 + offset_y},90,3
LO{0 + offset_x},{725 + offset_y},400,3
LO{0 + offset_x},{805 + offset_y},400,3
# LO{0 + offset_x},{830 + offset_y},400,3
"""

    # Linhas verticais internas
    if num_colunas == 4:
        epl += f"""
; ===== Linhas verticais internas =====
LO{50 + offset_x},{300 + offset_y},3,350
LO{100 + offset_x},{300 + offset_y},3,350
LO{150 + offset_x},{80 + offset_y},3,810
LO{200 + offset_x},{80 + offset_y},3,810
LO{250 + offset_x},{80 + offset_y},3,810
LO{300 + offset_x},{80 + offset_y},3,810
LO{350 + offset_x},{80 + offset_y},3,810
LO{400 + offset_x},{80 + offset_y},3,810
LO{450 + offset_x},{80 + offset_y},3,810
LO{500 + offset_x},{80 + offset_y},3,810
"""
    else:  # 3 colunas
        epl += f"""
; ===== Linhas verticais internas =====
LO{50 + offset_x},{300 + offset_y},3,350
LO{100 + offset_x},{300 + offset_y},3,350
LO{150 + offset_x},{80 + offset_y},3,810
LO{200 + offset_x},{80 + offset_y},3,810
LO{250 + offset_x},{80 + offset_y},3,810
LO{300 + offset_x},{80 + offset_y},3,810
LO{350 + offset_x},{80 + offset_y},3,810
LO{400 + offset_x},{80 + offset_y},3,810
LO{450 + offset_x},{80 + offset_y},3,810
LO{500 + offset_x},{80 + offset_y},3,810
"""

    # Título e conteúdo da tabela
    epl += f"""
; ===== Título (maior) =====
A{600 + offset_x},{190 + offset_y},1,2,3,2,N,"{d['titulo']}"

; ===== Conteúdo da tabela =====
; Coluna 1
A{530 + offset_x},{100 + offset_y},1,2,1,1,N,"N do Volume"
A{480 + offset_x},{100 + offset_y},1,2,1,1,N,"N do Pedido"
A{430 + offset_x},{100 + offset_y},1,2,1,1,N,"Descricao"
A{380 + offset_x},{100 + offset_y},1,2,1,1,N,"Ref. Cod."
A{110 + offset_x},{100 + offset_y},1,2,1,1,N,"Total de"
A{80 + offset_x},{100 + offset_y},1,2,1,1,N,"pecas caixa"

; Coluna 2
A{530 + offset_x},{310 + offset_y},1,2,1,1,N,"{d['volume']}"
A{530 + offset_x},{510 + offset_y},1,2,1,1,N,"{d['vezes1']}"
A{480 + offset_x},{310 + offset_y},1,2,1,1,N,"{d['pedido']}"
A{430 + offset_x},{310 + offset_y},1,2,1,1,N,"{d['descricao']}"
A{380 + offset_x},{310 + offset_y},1,2,1,1,N,"{d['cod_torra']}"
A{35 + offset_x},{350 + offset_y},1,2,1,1,N,"{d['total']}"

; Coluna 3
A{480 + offset_x},{510 + offset_y},1,2,1,1,N,"N.F."
A{380 + offset_x},{510 + offset_y},1,2,1,1,N,"Cor"
A{230 + offset_x},{510 + offset_y},1,2,1,1,N,"{d['cor']}"
A{480 + offset_x},{665 + offset_y},1,2,1,1,N,"{d['nf']}"
"""

    # Tamanhos dinâmicos com base na grade
    if num_colunas == 4:
        epl += f"""
; Coluna 4
A{380 + offset_x},{660 + offset_y},1,2,1,1,N,"{tamanhos[0]}"
A{380 + offset_x},{720 + offset_y},1,2,1,1,N,"{tamanhos[1]}"
A{380 + offset_x},{780 + offset_y},1,2,1,1,N,"{tamanhos[2]}"
A{380 + offset_x},{840 + offset_y},1,2,1,1,N,"{tamanhos[3]}"
A{230 + offset_x},{665 + offset_y},1,2,1,1,N,"{d['q10']}"
A{230 + offset_x},{725 + offset_y},1,2,1,1,N,"{d['q12']}"
A{230 + offset_x},{785 + offset_y},1,2,1,1,N,"{d['q14']}"
A{230 + offset_x},{845 + offset_y},1,2,1,1,N,"{d['q16']}"
A{100 + offset_x},{665 + offset_y},1,2,1,1,N,"{d['q10']}"
A{100 + offset_x},{725 + offset_y},1,2,1,1,N,"{d['q12']}"
A{100 + offset_x},{785 + offset_y},1,2,1,1,N,"{d['q14']}"
A{100 + offset_x},{845 + offset_y},1,2,1,1,N,"{d['q16']}"
"""
    else:  # 3 colunas
        epl += f"""
A{380 + offset_x},{670 + offset_y},1,2,1,1,N,"{tamanhos[0]}"
A{380 + offset_x},{750 + offset_y},1,2,1,1,N,"{tamanhos[1]}"
A{380 + offset_x},{830 + offset_y},1,2,1,1,N,"{tamanhos[2]}"

A{230 + offset_x},{670 + offset_y},1,2,1,1,N,"{d['q10']}"
A{230 + offset_x},{750 + offset_y},1,2,1,1,N,"{d['q12']}"
A{230 + offset_x},{830 + offset_y},1,2,1,1,N,"{d['q14']}"

A{100 + offset_x},{670 + offset_y},1,2,1,1,N,"{d['q10']}"
A{100 + offset_x},{750 + offset_y},1,2,1,1,N,"{d['q12']}"
A{100 + offset_x},{830 + offset_y},1,2,1,1,N,"{d['q14']}"
"""

    epl += "P1\n"
    return epl


def create_gui():
    root = tk.Tk()
    root.title("Editor de Etiquetas EPL")
    root.geometry("1000x600")

    # Ícones
    system = platform.system()
    try:
        if system == "Windows":
            icon_path = resource_path("icon_win.ico")
            root.iconbitmap(icon_path)
        else:
            icon_path = resource_path("icon_lux.png")
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
    except Exception as e:
        print(f"Aviso: não foi possível carregar ícone. {e}")

    # Tema e estilo
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0",
                    foreground="#333333", font=("Arial", 10))
    style.configure("Update.TButton", background="#0078D7", foreground="white", font=(
        "Arial", 8, "bold"), padding=5, width=20)
    style.map("Update.TButton", background=[("active", "#005BB5")])
    style.configure("Print.TButton", background="#4C75AF", foreground="white", font=(
        "Arial", 8, "bold"), padding=5, width=20)
    style.map("Print.TButton", background=[
              ("active", "#4C50AF")], foreground=[("active", "white")])
    root.configure(bg="#f0f0f0")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.rowconfigure(0, weight=1)

    # Frames
    input_frame = ttk.Frame(root, padding=(20, 50, 15, 50))
    input_frame.grid(row=0, column=0, sticky="nsew")
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=3)
    preview_frame = ttk.Frame(root, padding=(0, 50, 0, 0))
    preview_frame.grid(row=0, column=1, sticky="nsew")

    # Variáveis (corrigidos: largura=10cm, altura=15cm conforme pedido)
    largura_var = tk.StringVar(value="10")
    altura_var = tk.StringVar(value="15")
    printer_var = tk.StringVar(value="ELGIN L42Pro") # ELGIN L42Pro | ZDesigner TLP 2844
    titulo_var = tk.StringVar(value="Magazine Torra Torra Ltda")
    volume_var = tk.StringVar(value=str(ler_ultimo_volume() + 1))
    pedido_var = tk.StringVar(value="0")
    nf_var = tk.StringVar(value="0")
    descricao_var = tk.StringVar(value="")
    cor_var = tk.StringVar(value="")
    cod_torra_var = tk.StringVar(value="0")
    grade_var = tk.StringVar(value="10/12/14/16")  # Valor padrão
    q10_var = tk.StringVar(value="0")
    q12_var = tk.StringVar(value="0")
    q14_var = tk.StringVar(value="0")
    q16_var = tk.StringVar(value="0")
    vezes_var = tk.StringVar(value="1")

    # Dicionário para armazenar os widgets de rótulo e entrada
    label_widgets = {}
    entry_widgets = {}

    # Função para atualizar os rótulos dos campos de quantidade
    def atualizar_rotulos_grade():
        grade = grade_var.get()
        if grade == "1/2/3":
            tamanhos = ["1", "2", "3"]
        elif grade == "4/5/6":
            tamanhos = ["4", "5", "6"]
        elif grade == "P/M/G":
            tamanhos = ["P", "M", "G"]
        else:  # "10/12/14/16"
            tamanhos = ["10", "12", "14", "16"]
        
        # Limpar os widgets existentes no input_frame
        for widget in input_frame.winfo_children():
            widget.destroy()
            
        # Definir os campos fixos
        entries = [
            ("Nome da impressora:", printer_var),
            ("Título:", titulo_var),
            ("Número do volume:", volume_var),
            ("Número do pedido:", pedido_var),
            ("Número da nota fiscal:", nf_var),
            ("Descrição do produto:", descricao_var),
            ("Cor do produto:", cor_var),
            ("Código Torra:", cod_torra_var),
            ("Grade:", grade_var),
        ]

        # Adicionar campos de quantidade dinamicamente
        if grade == "10/12/14/16":
            entries.extend([
                (f"Quantidade tamanho {tamanhos[0]}:", q10_var),
                (f"Quantidade tamanho {tamanhos[1]}:", q12_var),
                (f"Quantidade tamanho {tamanhos[2]}:", q14_var),
                (f"Quantidade tamanho {tamanhos[3]}:", q16_var),
            ])
        else:  # Grades de 3 colunas
            entries.extend([
                (f"Quantidade tamanho {tamanhos[0]}:", q10_var),
                (f"Quantidade tamanho {tamanhos[1]}:", q12_var),
                (f"Quantidade tamanho {tamanhos[2]}:", q14_var),
            ])
            q16_var.set("0")  # Zerar q16 para grades de 3 colunas

        # Adicionar campo de quantidade de etiquetas
        entries.append(("Quantas etiquetas:", vezes_var))

        # Criar os widgets
        for i, (label, var) in enumerate(entries):
            label_widget = ttk.Label(input_frame, text=label)
            label_widget.grid(row=i, column=0, sticky="w", padx=(5, 10), pady=5)
            if label == "Grade:":
                grade_combo = ttk.Combobox(
                    input_frame,
                    textvariable=var,
                    values=["10/12/14/16", "1/2/3", "4/5/6", "P/M/G"],
                    state="readonly"
                )
                grade_combo.grid(row=i, column=1, sticky="ew", pady=3)
                grade_combo.bind("<<ComboboxSelected>>", lambda event: atualizar_rotulos_grade())
            else:
                entry_widget = ttk.Entry(input_frame, textvariable=var)
                entry_widget.grid(row=i, column=1, sticky="ew", pady=3)
            
            # Armazenar widgets para referência futura
            label_widgets[label] = label_widget
            if label != "Grade:":
                entry_widgets[label] = entry_widget

        # Adicionar botões
        ttk.Button(input_frame, text="Atualizar Visualização", style="Update.TButton",
                   command=atualizar_visualizacao).grid(row=len(entries), column=0, pady=10)
        ttk.Button(input_frame, text="Imprimir Etiqueta", style="Print.TButton",
                   command=enviar_etiqueta).grid(row=len(entries), column=1, pady=10)

    # Funções auxiliares
    def get_float(value, field_name):
        if not value:
            return None
        val = float(value)
        if val <= 0:
            raise ValueError(f"{field_name} deve ser maior que zero.")
        return val

    def get_int(value, field_name, allow_empty=True):
        if not value and allow_empty:
            return 0
        val = int(value)
        if val < 0:
            raise ValueError(f"{field_name} não pode ser negativo.")
        if field_name == "Número do volume" and val > 999999:
            raise ValueError(f"{field_name} não pode exceder 999999.")
        return val

    def get_string(value, field_name, max_length=50, allow_empty=True):
        if not value and allow_empty:
            return "Sem Título"
        if not value:
            raise ValueError(f"{field_name} não pode ser vazio.")
        if len(value) > max_length:
            raise ValueError(
                f"{field_name} não pode exceder {max_length} caracteres.")
        return value

    def atualizar_visualizacao():
        try:
            largura_cm = get_float(largura_var.get(), "Largura da folha")
            altura_cm = get_float(altura_var.get(), "Altura da folha")
            largura_mm = largura_cm * 10
            altura_mm = altura_cm * 10
            largura_pontos = int(largura_mm * 8)
            altura_pontos = int(altura_mm * 8)

            # Definir tamanhos com base na grade
            grade = grade_var.get()
            if grade == "1/2/3":
                tamanhos = ["1", "2", "3"]
            elif grade == "4/5/6":
                tamanhos = ["4", "5", "6"]
            elif grade == "P/M/G":
                tamanhos = ["P", "M", "G"]
            else:  # "10/12/14/16"
                tamanhos = ["10", "12", "14", "16"]

            # Validar quantidades com base nos tamanhos disponíveis
            q10 = get_int(q10_var.get(), f"Quantidade tamanho {tamanhos[0]}")
            q12 = get_int(q12_var.get(), f"Quantidade tamanho {tamanhos[1]}")
            q14 = get_int(q14_var.get(), f"Quantidade tamanho {tamanhos[2]}")
            q16 = get_int(q16_var.get(), f"Quantidade tamanho {tamanhos[3]}") if grade == "10/12/14/16" else 0
            total = q10 + q12 + q14 + q16

            volume = get_int(volume_var.get(), "Número do volume", allow_empty=False)
            titulo = get_string(titulo_var.get(), "Título", allow_empty=False)

            d = {
                "titulo": titulo,
                "volume": volume,
                "pedido": pedido_var.get() or "Sem Pedido",
                "nf": nf_var.get() or "Sem NF",
                "descricao": descricao_var.get() or "Sem Descricao",
                "cor": cor_var.get() or "Sem Cor",
                "cod_torra": cod_torra_var.get() or "Sem Código",
                "q10": q10,
                "q12": q12,
                "q14": q14,
                "q16": q16,
                "total": total,
                "vezes1": vezes_var.get() or "1",
            }

            epl = montar_epl(d, largura_pontos, altura_pontos, grade_var.get())
            img = visualizar_epl(epl, largura_pontos, altura_pontos)

            # scale para caber no canvas mantendo proporção
            canvas_width = canvas.winfo_width() or 800
            canvas_height = canvas.winfo_height() or 1200

            scale = min(canvas_width / largura_pontos, canvas_height / altura_pontos) * canvas.scale_factor
            scale = max(0.01, scale)
            new_size = (max(1, int(largura_pontos * scale)), max(1, int(altura_pontos * scale)))

            img_copy = img.copy()
            img_copy.thumbnail(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_copy)

            canvas.img = photo
            canvas.delete("all")
            canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo, anchor="center")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            canvas.delete("all")
            canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                            text="Erro na visualização. Verifique os dados.", anchor="center")

    def zoom(event):
        # event.delta no Windows, event.num no X11
        try:
            if hasattr(event, "delta"):
                zoom_factor = 1.1 if event.delta > 0 else 0.9
            else:
                zoom_factor = 1.1 if event.num == 4 else 0.9
        except Exception:
            zoom_factor = 1.1
        canvas.scale_factor *= zoom_factor
        canvas.scale_factor = max(0.1, min(canvas.scale_factor, 5.0))
        atualizar_visualizacao()

    def start_pan(event):
        canvas.scan_mark(event.x, event.y)

    def do_pan(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    def enviar_etiqueta():
        try:
            largura_cm = get_float(largura_var.get(), "Largura da folha")
            altura_cm = get_float(altura_var.get(), "Altura da folha")
            largura_mm = largura_cm * 10
            altura_mm = altura_cm * 10
            largura_pontos = int(largura_mm * 8)
            altura_pontos = int(altura_mm * 8)

            # Definir tamanhos com base na grade
            grade = grade_var.get()
            if grade == "1/2/3":
                tamanhos = ["1", "2", "3"]
            elif grade == "4/5/6":
                tamanhos = ["4", "5", "6"]
            elif grade == "P/M/G":
                tamanhos = ["P", "M", "G"]
            else:  # "10/12/14/16"
                tamanhos = ["10", "12", "14", "16"]

            # Validar quantidades com base nos tamanhos disponíveis
            q10 = get_int(q10_var.get(), f"Quantidade tamanho {tamanhos[0]}")
            q12 = get_int(q12_var.get(), f"Quantidade tamanho {tamanhos[1]}")
            q14 = get_int(q14_var.get(), f"Quantidade tamanho {tamanhos[2]}")
            q16 = get_int(q16_var.get(), f"Quantidade tamanho {tamanhos[3]}") if grade == "10/12/14/16" else 0
            total = q10 + q12 + q14 + q16

            vezes = get_int(vezes_var.get(), "Quantidade de etiquetas", allow_empty=False)
            volume = get_int(volume_var.get(), "Número do volume", allow_empty=False)
            titulo = get_string(titulo_var.get(), "Título", allow_empty=False)
            printer_name = printer_var.get()
            if not printer_name.strip():
                raise ValueError("Nome da impressora não pode ser vazio.")
            ultimo_volume = ler_ultimo_volume()

            if volume <= ultimo_volume:
                resposta = messagebox.askyesno(
                    "Aviso", f"O volume {volume} é menor ou igual ao último salvo ({ultimo_volume}). Continuar?")
                if not resposta:
                    return

            for _ in range(vezes):
                volume_atual = volume
                d = {
                    "titulo": titulo,
                    "volume": str(volume_atual),
                    "pedido": pedido_var.get() or "Sem Pedido",
                    "nf": nf_var.get() or "Sem NF",
                    "descricao": descricao_var.get() or "Sem Descricao",
                    "cor": cor_var.get() or "Sem Cor",
                    "cod_torra": cod_torra_var.get() or "Sem Código",
                    "q10": q10,
                    "q12": q12,
                    "q14": q14,
                    "q16": q16,
                    "total": total,
                    "vezes1": vezes,
                }
                epl = montar_epl(d, largura_pontos, altura_pontos, grade_var.get())

                if enviar_para_zebra(printer_name, epl):
                    print(f"Etiqueta enviada. Volume #{volume_atual}")
                    volume = salvar_volume(volume_atual)  # salva e incrementa
                    volume_var.set(str(volume))
                else:
                    messagebox.showerror(
                        "Erro", f"Falha ao enviar etiqueta para {printer_name}.")
                    return

            messagebox.showinfo(
                "Sucesso", f"{vezes} etiqueta(s) enviada(s) com sucesso!")
            atualizar_visualizacao()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Canvas de visualização
    canvas = tk.Canvas(preview_frame, bg="white", width=500, height=400)
    canvas.pack(expand=True, fill="both")
    canvas.scale_factor = 1.0

    # Adiciona a mensagem inicial no canvas
    canvas.create_text(300, 300, text="Preencha os campos e clique em 'Atualizar Visualização'",
                       anchor="center", font=("Arial", 12))

    # Eventos do canvas
    canvas.bind("<ButtonPress-1>", start_pan)
    canvas.bind("<B1-Motion>", do_pan)
    canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<Button-4>", zoom)
    canvas.bind("<Button-5>", zoom)
  
    # Inicializar rótulos com base na grade padrão
    atualizar_rotulos_grade()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
