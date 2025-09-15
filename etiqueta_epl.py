# ====== Site para visualizar EPl --> https://eplprinter.azurewebsites.net/

# import socket
# import os
# import sys
# from PIL import Image, ImageDraw, ImageFont
# import platform
# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import ImageTk

# COUNTER_FILE = "contador_volume.txt"

# def resource_path(relative_path):
#     """Retorna o caminho absoluto para o recurso, funcionando tanto no .py quanto no .exe"""
#     try:
#         base_path = sys._MEIPASS
#     except AttributeError:
#         base_path = os.path.dirname(__file__)
#     return os.path.join(base_path, relative_path)

# def visualizar_epl(epl_code, largura_pontos, altura_pontos):
#     img = Image.new("RGB", (largura_pontos, altura_pontos), "white")
#     draw = ImageDraw.Draw(img)

#     try:
#         font_large = ImageFont.truetype("arial.ttf", 52)
#         font_small = ImageFont.truetype("arial.ttf", 16)
#         font_bold = ImageFont.truetype("arialbd.ttf", 16)
#     except:
#         font_large = ImageFont.load_default()
#         font_small = ImageFont.load_default()
#         font_bold = ImageFont.load_default()

#     for linha in epl_code.split("\n"):
#         linha = linha.strip()
#         if not linha:
#             continue
#         if linha.startswith("A"):
#             partes = linha.split(",")
#             if len(partes) < 8:
#                 continue
#             x, y = int(partes[0][1:]), int(partes[1])
#             fonte = int(partes[3])
#             escala_x, escala_y = int(partes[4]), int(partes[5])
#             texto = partes[-1].strip('"')
#             font = font_large if fonte == 5 and escala_x >= 7 else font_bold if escala_x >= 2 else font_small
#             draw.text((x, y), texto, fill="black", font=font)
#         elif linha.startswith("LO"):
#             partes = linha[2:].split(",")
#             if len(partes) != 4:
#                 continue
#             x, y, comprimento, espessura = map(int, partes)
#             draw.line((x, y, x + comprimento, y), fill="black", width=espessura * 2)
#         elif linha.startswith("LE"):
#             partes = linha[2:].split(",")
#             if len(partes) != 5:
#                 continue
#             x, y, _, altura, espessura = map(int, partes)
#             draw.line((x, y, x, y + altura), fill="black", width=espessura * 2)

#     return img

# def ler_ultimo_volume():
#     """Lê o último número de volume do arquivo, retornando 0 se inválido ou não existente."""
#     if os.path.exists(COUNTER_FILE):
#         try:
#             with open(COUNTER_FILE, "r", encoding="utf-8") as f:
#                 content = f.read().strip()
#                 if content:
#                     return int(content)
#                 return 0
#         except (ValueError, IOError) as e:
#             print(f"Erro ao ler {COUNTER_FILE}: {e}")
#             return 0
#     return 0

# def salvar_volume(volume):
#     """
#     Salva o número do volume no arquivo com backup e retorna o próximo número.
#     Args:
#         volume (int): Volume a ser salvo.
#     Returns:
#         int: Próximo volume (volume + 1).
#     """
#     try:
#         if os.path.exists(COUNTER_FILE):
#             # Remove backup antigo, se existir
#             if os.path.exists(COUNTER_FILE + ".bak"):
#                 os.remove(COUNTER_FILE + ".bak")
#             os.rename(COUNTER_FILE, COUNTER_FILE + ".bak") # Cria novo backup
#         with open(COUNTER_FILE, "w", encoding="utf-8") as f:
#             f.write(str(volume))
#         return volume + 1
#     except Exception as e:
#         print(f"Erro ao salvar volume: {e}")
#         return volume + 1

# def enviar_para_zebra(ip, epl, porta=9100, timeout=5, retries=3):
#     for attempt in range(retries):
#         try:
#             with socket.create_connection((ip, porta), timeout=timeout) as s:
#                 s.sendall(epl.encode("utf-8"))
#             return True
#         except Exception as e:
#             print(f"Tentativa {attempt + 1}/{retries} falhou: {e}")
#             if attempt == retries - 1:
#                 print(f"Erro ao enviar etiqueta após {retries} tentativas.")
#                 return False
#     return False

# def montar_epl(d, largura_pontos, altura_pontos):
#     return f"""
# N
# q{largura_pontos}
# Q{altura_pontos},24

# ; Título
# A280,30,0,5,10,10,N,"{d['titulo']}"

# ; Linhas horizontais da tabela
# LO54,120,1100,1
# LO54,160,1100,1
# LO54,200,1100,1
# LO54,240,1100,1
# LO54,280,1100,1
# LO54,320,1100,1
# LO54,360,1100,1
# LO54,400,1100,1
# LO54,440,1100,1
# LO54,480,1100,1
# LO190,520,312,1
# LO735,520,222,1
# LO54,560,1100,1

# ; Linhas verticais da tabela
# LE54,120,0,440,1
# LE190,120,0,440,1
# LE390,240,0,320,1
# LE390,120,0,80,1
# LE502,120,0,80,1
# LE502,240,0,320,1
# LE734,120,0,40,1
# LE734,240,0,320,1
# LE558,240,0,320,1
# LE618,240,0,320,1
# LE678,240,0,320,1
# LE958,120,0,440,1
# LE1152,120,0,440,1

# ; Conteúdo da tabela
# ; Linha 1
# A62,132,0,3,2,2,N,"Nº do Volume"
# A198,132,0,3,1,1,N,"{d['volume']}"
# A510,132,0,3,2,2,N,"Ref.Cod.Torra"
# A742,132,0,3,1,1,N,"{d['cod_torra']}"

# ; Linha 2
# A62,172,0,3,2,2,N,"Nº do Pedido"
# A198,172,0,3,1,1,N,"{d['pedido']}"
# A398,172,0,3,2,2,N,"N.F."
# A510,172,0,3,1,1,N,"{d['nf']}"

# ; Linha 3
# A62,212,0,3,2,2,N,"Descrição"
# A198,212,0,3,1,1,N,"{d['descricao']}"

# ; Linha 4
# A398,252,0,3,2,2,N,"Cor"
# A518,252,0,3,2,2,N,"10"
# A574,252,0,3,2,2,N,"12"
# A630,252,0,3,2,2,N,"14"
# A694,252,0,3,2,2,N,"16"

# ; Linha 7
# A398,372,0,3,1,1,N,"{d['cor']}"
# A518,372,0,3,1,1,N,"{d['q10']}"
# A574,372,0,3,1,1,N,"{d['q12']}"
# A630,372,0,3,1,1,N,"{d['q14']}"
# A694,372,0,3,1,1,N,"{d['q16']}"

# ; Linha 10
# A66,500,0,3,2,2,N,"Total de"
# A66,520,0,3,2,2,N,"peças caixa"
# A198,528,0,3,1,1,N,"{d['total']}"
# A518,504,0,3,1,1,N,"{d['q10']}"
# A574,504,0,3,1,1,N,"{d['q12']}"
# A630,504,0,3,1,1,N,"{d['q14']}"
# A694,504,0,3,1,1,N,"{d['q16']}"

# P1
# """.strip() + "\n"

# def create_gui():
#     root = tk.Tk()
#     root.title("Editor de Etiquetas EPL")
#     root.geometry("1000x600")

#     # Configurar o ícone da janela e da barra de tarefas
#     system = platform.system()
#     if system == "Windows":
#         try:
#             icon_path = resource_path("icon_win.ico")
#             if not os.path.exists(icon_path):
#                 raise FileNotFoundError(f"Arquivo 'icon_win.ico' não encontrado em: {icon_path}")
#             root.iconbitmap(icon_path)
#         except (tk.TclError, FileNotFoundError) as e:
#             print(f"Erro ao carregar o ícone 'icon_win.ico': {e}")
#             print(f"Verifique se o arquivo 'icon_win.ico' está na pasta do executável ou do script e é um ICO válido (ex.: contém resoluções 16x16 e 32x32 pixels).")
#             try:
#                 icon_path_png = resource_path("icon_lux.png")
#                 if not os.path.exists(icon_path_png):
#                     raise FileNotFoundError(f"Arquivo 'icon_lux.png' não encontrado em: {icon_path_png}")
#                 icon = tk.PhotoImage(file=icon_path_png)
#                 root.iconphoto(True, icon)
#             except (tk.TclError, FileNotFoundError) as e:
#                 print(f"Fallback para 'icon_lux.png' falhou: {e}")
#                 print(f"Verifique se o arquivo 'icon_lux.png' está na pasta do executável ou do script e é um PNG válido (ex.: 32x32 pixels).")
#     else:
#         try:
#             icon_path = resource_path("icon_lux.png")
#             if not os.path.exists(icon_path):
#                 raise FileNotFoundError(f"Arquivo 'icon_lux.png' não encontrado em: {icon_path}")
#             icon = tk.PhotoImage(file=icon_path)
#             root.iconphoto(True, icon)
#         except (tk.TclError, FileNotFoundError) as e:
#             print(f"Erro ao carregar o ícone 'icon_lux.png': {e}")
#             print(f"Verifique se o arquivo 'icon_lux.png' está na pasta do executável ou do script e é um PNG válido (ex.: 32x32 pixels).")

#     # Configurar o tema e estilo
#     style = ttk.Style()
#     style.theme_use("clam")
#     style.configure("TFrame", background="#f0f0f0")
#     style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Arial", 10))
#     style.configure("Update.TButton", background="#0078D7", foreground="white", font=("Arial", 8, "bold"), padding=5, width=20)
#     style.map("Update.TButton", background=[("active", "#005BB5")])
#     style.configure("Print.TButton", background="#4C75AF", foreground="white", font=("Arial", 8, "bold"), padding=5, width=20)
#     style.map("Print.TButton", background=[("active", "#4C50AF")], foreground=[("active", "white")])
#     root.configure(bg="#f0f0f0")

#     root.columnconfigure(0, weight=1)
#     root.columnconfigure(1, weight=3)
#     root.rowconfigure(0, weight=1)

#     input_frame = ttk.Frame(root, padding=(10, 50, 10, 0))
#     input_frame.grid(row=0, column=0, sticky="nsew")
#     preview_frame = ttk.Frame(root, padding=(0, 50, 0, 0))
#     preview_frame.grid(row=0, column=1, sticky="nsew")

#     # Variáveis para entradas
#     largura_var = tk.StringVar(value="15")
#     altura_var = tk.StringVar(value="10")
#     ip_var = tk.StringVar(value="127.0.0.1")
#     titulo_var = tk.StringVar(value="Magazine Torra Torra Ltda")
#     volume_var = tk.StringVar(value=str(ler_ultimo_volume() + 1))  # Inicializa com o próximo volume
#     pedido_var = tk.StringVar(value="0")
#     nf_var = tk.StringVar(value="0")
#     descricao_var = tk.StringVar(value="")
#     cor_var = tk.StringVar(value="")
#     cod_torra_var = tk.StringVar(value="0")
#     q10_var = tk.StringVar(value="0")
#     q12_var = tk.StringVar(value="0")
#     q14_var = tk.StringVar(value="0")
#     q16_var = tk.StringVar(value="0")
#     vezes_var = tk.StringVar(value="1")

#     def get_float(value, field_name):
#         """Converte uma string para float, validando se é positiva."""
#         if not value:
#             return None
#         try:
#             val = float(value)
#             if val <= 0:
#                 raise ValueError(f"{field_name} deve ser maior que zero.")
#             return val
#         except ValueError:
#             raise ValueError(f"{field_name} deve ser um número válido.")

#     def get_int(value, field_name, allow_empty=True):
#         """Converte uma string para inteiro, validando se é não-negativo e dentro do limite."""
#         if not value and allow_empty:
#             return "0"
#         try:
#             val = int(value)
#             if val < 0:
#                 raise ValueError(f"{field_name} não pode ser negativo.")
#             if field_name == "Número do volume" and val > 999999:
#                 raise ValueError(f"{field_name} não pode exceder 999999.")
#             return str(val)
#         except ValueError:
#             raise ValueError(f"{field_name} deve ser um número inteiro válido.")

#     def get_string(value, field_name, max_length=50, allow_empty=True):
#         """Valida uma string, garantindo que não exceda o comprimento máximo."""
#         if not value and allow_empty:
#             return "Sem Título"
#         if not value:
#             raise ValueError(f"{field_name} não pode ser vazio.")
#         if len(value) > max_length:
#             raise ValueError(f"{field_name} não pode exceder {max_length} caracteres.")
#         return value

#     def atualizar_visualizacao():
#         """Atualiza a pré-visualização da etiqueta"""
#         try:
#             largura_cm = get_float(largura_var.get(), "Largura da folha")
#             altura_cm = get_float(altura_var.get(), "Altura da folha")
#             if not largura_cm or not altura_cm:
#                 raise ValueError("Largura e altura são obrigatórios.")

#             largura_mm = largura_cm * 10
#             altura_mm = altura_cm * 10
#             largura_pontos = int(largura_mm * 8)
#             altura_pontos = int(altura_mm * 8)

#             q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
#             q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
#             q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
#             q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
#             total = str(int(q10 or 0) + int(q12 or 0) + int(q14 or 0) + int(q16 or 0))

#             volume = get_int(volume_var.get(), "Número do volume", allow_empty=False)
#             titulo = get_string(titulo_var.get(), "Título", allow_empty=False)

#             d = {
#                 "titulo": titulo,
#                 "volume": volume,
#                 "pedido": pedido_var.get() or "Sem Pedido",
#                 "nf": nf_var.get() or "Sem NF",
#                 "descricao": descricao_var.get() or "Sem Descrição",
#                 "cor": cor_var.get() or "Sem Cor",
#                 "cod_torra": cod_torra_var.get() or "Sem Código",
#                 "q10": q10,
#                 "q12": q12,
#                 "q14": q14,
#                 "q16": q16,
#                 "total": total,
#             }

#             epl = montar_epl(d, largura_pontos, altura_pontos)
#             img = visualizar_epl(epl, largura_pontos, altura_pontos)

#             base_size = 500
#             new_size = (int(base_size * canvas.scale_factor), int(base_size * canvas.scale_factor))
#             img.thumbnail(new_size, Image.Resampling.LANCZOS)
#             photo = ImageTk.PhotoImage(img)

#             canvas.img = photo
#             canvas_width = canvas.winfo_width() or 500
#             canvas_height = canvas.winfo_height() or 500
#             canvas.delete("all")
#             canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo, anchor="center")
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))
#             canvas.delete("all")
#             canvas.create_text(canvas.winfo_width() / 2 or 250, canvas.winfo_height() / 2 or 250,
#                            text="Erro na visualização. Verifique os dados.", anchor="center")

#     def zoom(event):
#         """Ajusta o zoom da visualização com a roda do mouse."""
#         zoom_factor = 1.1 if event.delta > 0 or event.num == 4 else 0.9
#         canvas.scale_factor *= zoom_factor
#         canvas.scale_factor = max(0.5, min(canvas.scale_factor, 5.0))
#         atualizar_visualizacao()

#     def start_pan(event):
#         """Inicia o arraste da visualização."""
#         canvas.scan_mark(event.x, event.y)

#     def do_pan(event):
#         """Executa o arraste da visualização."""
#         canvas.scan_dragto(event.x, event.y, gain=1)

#     def proximo_volume():
#         """Atualiza o campo 'Número do volume' com o próximo volume do contador."""
#         volume_var.set(str(ler_ultimo_volume() + 1))

#     def enviar_etiqueta():
#         """Envia a etiqueta para a impressora, usando o volume digitado e atualizando o contador."""
#         try:
#             largura_cm = get_float(largura_var.get(), "Largura da folha")
#             altura_cm = get_float(altura_var.get(), "Altura da folha")
#             if not largura_cm or not altura_cm:
#                 raise ValueError("Largura e altura são obrigatórios.")
#             ip = ip_var.get()
#             if not ip:
#                 raise ValueError("IP da impressora é obrigatório.")

#             largura_mm = largura_cm * 10
#             altura_mm = altura_cm * 10
#             largura_pontos = int(largura_mm * 8)
#             altura_pontos = int(altura_mm * 8)

#             q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
#             q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
#             q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
#             q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
#             total = str(int(q10 or 0) + int(q12 or 0) + int(q14 or 0) + int(q16 or 0))

#             vezes = get_int(vezes_var.get(), "Quantidade de etiquetas", allow_empty=False)
#             volume = int(get_int(volume_var.get(), "Número do volume", allow_empty=False))
#             titulo = get_string(titulo_var.get(), "Título", allow_empty=False)
#             ultimo_volume = ler_ultimo_volume()

#             # Alerta para volumes potencialmente duplicados
#             if volume <= ultimo_volume:
#                 resposta = messagebox.askyesno("Aviso", f"O volume {volume} é menor ou igual ao último salvo ({ultimo_volume}). Isso pode causar duplicatas. Continuar?")
#                 if not resposta:
#                     return

#             for _ in range(int(vezes)):
#                 volume_atual = volume
#                 d = {
#                     "titulo": titulo,
#                     "volume": str(volume_atual),
#                     "pedido": pedido_var.get() or "Sem Pedido",
#                     "nf": nf_var.get() or "Sem NF",
#                     "descricao": descricao_var.get() or "Sem Descrição",
#                     "cor": cor_var.get() or "Sem Cor",
#                     "cod_torra": cod_torra_var.get() or "Sem Código",
#                     "q10": q10,
#                     "q12": q12,
#                     "q14": q14,
#                     "q16": q16,
#                     "total": total,
#                 }
#                 epl = montar_epl(d, largura_pontos, altura_pontos)
#                 if enviar_para_zebra(ip, epl):
#                     print(f"Etiqueta enviada. Volume #{volume_atual}")
#                     salvar_volume(volume_atual)
#                     volume += 1
#                 else:
#                     messagebox.showerror("Erro", "Falha ao enviar para a impressora.")
#                     return
#             messagebox.showinfo("Sucesso", f"{vezes} etiqueta(s) enviada(s) com sucesso!")
#         except Exception as e:
#             messagebox.showerror("Erro", str(e))

#     canvas = tk.Canvas(preview_frame, bg="white", width=500, height=400)
#     canvas.pack(expand=True, fill="both")
#     canvas.scale_factor = 1.0

#     canvas.bind("<MouseWheel>", zoom)
#     canvas.bind("<Button-4>", zoom)
#     canvas.bind("<Button-5>", zoom)
#     canvas.bind("<Button-1>", start_pan)
#     canvas.bind("<B1-Motion>", do_pan)

#     canvas.create_text(300, 300, text="Preencha os campos e clique em 'Atualizar Visualização'", anchor="center", font=("Arial", 12))

#     entries = [
#         ("Largura da folha (cm):", largura_var),
#         ("Altura da folha (cm):", altura_var),
#         ("IP da impressora:", ip_var),
#         ("Título:", titulo_var),
#         ("Número do volume:", volume_var),
#         ("Número do pedido:", pedido_var),
#         ("Número da nota fiscal:", nf_var),
#         ("Descrição do produto:", descricao_var),
#         ("Cor do produto:", cor_var),
#         ("Código Torra:", cod_torra_var),
#         ("Quantidade tamanho 10:", q10_var),
#         ("Quantidade tamanho 12:", q12_var),
#         ("Quantidade tamanho 14:", q14_var),
#         ("Quantidade tamanho 16:", q16_var),
#         ("Quantas etiquetas:", vezes_var),
#     ]

#     # Configurar o input_frame para expandir
#     input_frame = ttk.Frame(root, padding=(20, 50, 15, 50))
#     input_frame.grid(row=0, column=0, sticky="nsew")  # Expande em todas as direções
#     input_frame.columnconfigure(0, weight=1)  # Labels têm peso menor
#     input_frame.columnconfigure(1, weight=3)  # Entradas expandem mais

#     # Configurar pesos na janela principal
#     root.columnconfigure(0, weight=1)  # input_frame expande
#     root.columnconfigure(1, weight=3)  # preview_frame expande mais
#     root.rowconfigure(0, weight=1)

#     for i, (label, var) in enumerate(entries):
#         ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w", padx=(5, 10), pady=5)
#         ttk.Entry(input_frame, textvariable=var).grid(row=i, column=1, sticky="ew", pady=3)

#     ttk.Button(input_frame, text="Atualizar Visualização", command=atualizar_visualizacao, style="Update.TButton").grid(
#         row=len(entries), column=0, sticky="ew", padx=5, pady=10)
#     ttk.Button(input_frame, text="Enviar para Impressora", command=enviar_etiqueta, style="Print.TButton").grid(
#         row=len(entries), column=1, sticky="ew", padx=5, pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     create_gui()


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


def montar_epl(d, largura_pontos=640, altura_pontos=920):
    # Deslocamentos para mover um pouco para a direita e para baixo
    offset_x = 70  # Move pontos para a direita
    offset_y = 0  # Move pontos para baixo

    return f"""
N
q{largura_pontos}
Q{altura_pontos},24
D10
S2

; --- Moldura externa com 4 LO ---
; topo: de X=20 até X=560 (largura 540), esp. 2
LO{0 + offset_x},{80 + offset_y},540,2

; base: mesma largura, Y=910
LO{0 + offset_x},{890 + offset_y},540,2

; esquerda: X=20, altura 810 (de 100 até 910)
LO{0 + offset_x},{80 + offset_y},2,810

; direita: começa em X=558, largura 2 (vai até 560)
LO{538 + offset_x},{80 + offset_y},2,810
X{0 + offset_x},{80 + offset_y},2,{530 + offset_x},{890 + offset_y}     ; moldura de (20,100) até (550,910)

; ===== Linhas horizontais internas =====
LO{0 + offset_x},{300 + offset_y},540,3
LO{0 + offset_x},{500 + offset_y},400,3
LO{450 + offset_x},{500 + offset_y},90,3
LO{0 + offset_x},{650 + offset_y},400,3
LO{450 + offset_x},{650 + offset_y},90,3
LO{0 + offset_x},{710 + offset_y},400,3
LO{0 + offset_x},{770 + offset_y},400,3
LO{0 + offset_x},{830 + offset_y},400,3

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

; ===== Título (maior) =====
A{590 + offset_x},{190 + offset_y},1,2,3,2,N,"{d['titulo']}"

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
A{30 + offset_x},{350 + offset_y},1,2,1,1,N,"{d['total']}"

; Coluna 3
A{480 + offset_x},{510 + offset_y},1,2,1,1,N,"N.F."
A{380 + offset_x},{510 + offset_y},1,2,1,1,N,"Cor"
A{230 + offset_x},{510 + offset_y},1,2,1,1,N,"{d['cor']}"

; Coluna 4
A{480 + offset_x},{665 + offset_y},1,2,1,1,N,"{d['nf']}"
A{380 + offset_x},{660 + offset_y},1,2,1,1,N,"10"
A{380 + offset_x},{720 + offset_y},1,2,1,1,N,"12"
A{380 + offset_x},{780 + offset_y},1,2,1,1,N,"14"
A{380 + offset_x},{840 + offset_y},1,2,1,1,N,"16"
A{230 + offset_x},{665 + offset_y},1,2,1,1,N,"{d['q10']}"
A{230 + offset_x},{725 + offset_y},1,2,1,1,N,"{d['q12']}"
A{230 + offset_x},{785 + offset_y},1,2,1,1,N,"{d['q14']}"
A{230 + offset_x},{845 + offset_y},1,2,1,1,N,"{d['q16']}"
A{100 + offset_x},{665 + offset_y},1,2,1,1,N,"{d['q10']}"
A{100 + offset_x},{725 + offset_y},1,2,1,1,N,"{d['q12']}"
A{100 + offset_x},{785 + offset_y},1,2,1,1,N,"{d['q14']}"
A{100 + offset_x},{845 + offset_y},1,2,1,1,N,"{d['q16']}"

P1
"""


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
    printer_var = tk.StringVar(value="ELGIN L42Pro") # ELGIN L42Pro ZDesigner TLP 2844
    titulo_var = tk.StringVar(value="Magazine Torra Torra Ltda")
    volume_var = tk.StringVar(value=str(ler_ultimo_volume() + 1))
    pedido_var = tk.StringVar(value="0")
    nf_var = tk.StringVar(value="0")
    descricao_var = tk.StringVar(value="")
    cor_var = tk.StringVar(value="")
    cod_torra_var = tk.StringVar(value="0")
    q10_var = tk.StringVar(value="0")
    q12_var = tk.StringVar(value="0")
    q14_var = tk.StringVar(value="0")
    q16_var = tk.StringVar(value="0")
    vezes_var = tk.StringVar(value="1")

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

            q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
            q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
            q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
            q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
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

            epl = montar_epl(d, largura_pontos, altura_pontos)
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

            q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
            q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
            q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
            q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
            total = q10 + q12 + q14 + q16

            vezes = get_int(vezes_var.get(),
                            "Quantidade de etiquetas", allow_empty=False)
            volume = get_int(volume_var.get(),
                             "Número do volume", allow_empty=False)
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
                epl = montar_epl(d, largura_pontos, altura_pontos)

                if enviar_para_zebra(printer_name, epl):
                    print(f"Etiqueta enviada. Volume #{volume_atual}")
                    volume = salvar_volume(volume_atual) # salva e incrementa
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

    # Campos de entrada
    entries = [
        ("Nome da impressora:", printer_var),
        ("Título:", titulo_var),
        ("Número do volume:", volume_var),
        ("Número do pedido:", pedido_var),
        ("Número da nota fiscal:", nf_var),
        ("Descrição do produto:", descricao_var),
        ("Cor do produto:", cor_var),
        ("Código Torra:", cod_torra_var),
        ("Quantidade tamanho 10:", q10_var),
        ("Quantidade tamanho 12:", q12_var),
        ("Quantidade tamanho 14:", q14_var),
        ("Quantidade tamanho 16:", q16_var),
        ("Quantas etiquetas:", vezes_var),
    ]

    for i, (label, var) in enumerate(entries):
        ttk.Label(input_frame, text=label).grid(
            row=i, column=0, sticky="w", padx=(5, 10), pady=5)
        ttk.Entry(input_frame, textvariable=var).grid(
            row=i, column=1, sticky="ew", pady=3)

    # Botões
    ttk.Button(input_frame, text="Atualizar Visualização", style="Update.TButton",
               command=atualizar_visualizacao).grid(row=len(entries), column=0, pady=10)
    ttk.Button(input_frame, text="Imprimir Etiqueta", style="Print.TButton",
               command=enviar_etiqueta).grid(row=len(entries), column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
