import socket
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

COUNTER_FILE = "contador_volume.txt"

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, funcionando tanto no .py quanto no .exe"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def visualizar_epl(epl_code, largura_pontos, altura_pontos):
    img = Image.new("RGB", (largura_pontos, altura_pontos), "white")
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("arial.ttf", 52)
        font_small = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    for linha in epl_code.split("\n"):
        linha = linha.strip()
        if not linha:
            continue
        if linha.startswith("A"):
            partes = linha.split(",")
            if len(partes) < 8:
                continue
            x, y = int(partes[0][1:]), int(partes[1])
            fonte = int(partes[3])
            escala_x, escala_y = int(partes[4]), int(partes[5])
            texto = partes[-1].strip('"')
            font = font_large if fonte == 5 and escala_x >= 7 else font_bold if escala_x >= 2 else font_small
            draw.text((x, y), texto, fill="black", font=font)
        elif linha.startswith("LO"):
            partes = linha[2:].split(",")
            if len(partes) != 4:
                continue
            x, y, comprimento, espessura = map(int, partes)
            draw.line((x, y, x + comprimento, y), fill="black", width=espessura * 2)
        elif linha.startswith("LE"):
            partes = linha[2:].split(",")
            if len(partes) != 5:
                continue
            x, y, _, altura, espessura = map(int, partes)
            draw.line((x, y, x, y + altura), fill="black", width=espessura * 2)

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
    """
    Salva o número do volume no arquivo com backup e retorna o próximo número.
    Args:
        volume (int): Volume a ser salvo.
    Returns:
        int: Próximo volume (volume + 1).
    """
    try:
        if os.path.exists(COUNTER_FILE):
            os.rename(COUNTER_FILE, COUNTER_FILE + ".bak")  # Backup
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            f.write(str(volume))
        return volume + 1
    except Exception as e:
        print(f"Erro ao salvar volume: {e}")
        return volume + 1

def enviar_para_zebra(ip, epl, porta=9100, timeout=5, retries=3):
    for attempt in range(retries):
        try:
            with socket.create_connection((ip, porta), timeout=timeout) as s:
                s.sendall(epl.encode("utf-8"))
            return True
        except Exception as e:
            print(f"Tentativa {attempt + 1}/{retries} falhou: {e}")
            if attempt == retries - 1:
                print(f"Erro ao enviar etiqueta após {retries} tentativas.")
                return False
    return False

def montar_epl(d, largura_pontos, altura_pontos):
    return f"""
N
q{largura_pontos}
Q{altura_pontos},24

; Título
A280,30,0,5,10,10,N,"{d['titulo']}"

; Linhas horizontais da tabela
LO54,120,1100,1
LO54,160,1100,1
LO54,200,1100,1
LO54,240,1100,1
LO54,280,1100,1
LO54,320,1100,1
LO54,360,1100,1
LO54,400,1100,1
LO54,440,1100,1
LO54,480,1100,1
LO190,520,312,1
LO735,520,222,1
LO54,560,1100,1

; Linhas verticais da tabela
LE54,120,0,440,1
LE190,120,0,440,1
LE390,240,0,320,1
LE390,120,0,80,1
LE502,120,0,80,1
LE502,240,0,320,1
LE734,120,0,40,1
LE734,240,0,320,1
LE558,240,0,320,1
LE618,240,0,320,1
LE678,240,0,320,1
LE958,120,0,440,1
LE1152,120,0,440,1

; Conteúdo da tabela
; Linha 1
A62,132,0,3,2,2,N,"Nº do Volume"
A198,132,0,3,1,1,N,"{d['volume']}"
A510,132,0,3,2,2,N,"Ref.Cod.Torra"
A742,132,0,3,1,1,N,"{d['cod_torra']}"

; Linha 2
A62,172,0,3,2,2,N,"Nº do Pedido"
A198,172,0,3,1,1,N,"{d['pedido']}"
A398,172,0,3,2,2,N,"N.F."
A510,172,0,3,1,1,N,"{d['nf']}"

; Linha 3
A62,212,0,3,2,2,N,"Descrição"
A198,212,0,3,1,1,N,"{d['descricao']}"

; Linha 4
A398,252,0,3,2,2,N,"Cor"
A518,252,0,3,2,2,N,"10"
A574,252,0,3,2,2,N,"12"
A630,252,0,3,2,2,N,"14"
A694,252,0,3,2,2,N,"16"

; Linha 7
A398,372,0,3,1,1,N,"{d['cor']}"
A518,372,0,3,1,1,N,"{d['q10']}"
A574,372,0,3,1,1,N,"{d['q12']}"
A630,372,0,3,1,1,N,"{d['q14']}"
A694,372,0,3,1,1,N,"{d['q16']}"

; Linha 10
A66,500,0,3,2,2,N,"Total de"
A66,520,0,3,2,2,N,"peças caixa"
A198,528,0,3,1,1,N,"{d['total']}"
A518,504,0,3,1,1,N,"{d['q10']}"
A574,504,0,3,1,1,N,"{d['q12']}"
A630,504,0,3,1,1,N,"{d['q14']}"
A694,504,0,3,1,1,N,"{d['q16']}"

P1
""".strip() + "\n"

def create_gui():
    root = tk.Tk()
    root.title("Editor de Etiquetas EPL")
    root.geometry("1000x600")

    # Configurar o ícone da janela e da barra de tarefas
    system = platform.system()
    if system == "Windows":
        try:
            icon_path = resource_path("icon_win.ico")
            if not os.path.exists(icon_path):
                raise FileNotFoundError(f"Arquivo 'icon_win.ico' não encontrado em: {icon_path}")
            root.iconbitmap(icon_path)
        except (tk.TclError, FileNotFoundError) as e:
            print(f"Erro ao carregar o ícone 'icon_win.ico': {e}")
            print(f"Verifique se o arquivo 'icon_win.ico' está na pasta do executável ou do script e é um ICO válido (ex.: contém resoluções 16x16 e 32x32 pixels).")
            try:
                icon_path_png = resource_path("icon_lux.png")
                if not os.path.exists(icon_path_png):
                    raise FileNotFoundError(f"Arquivo 'icon_lux.png' não encontrado em: {icon_path_png}")
                icon = tk.PhotoImage(file=icon_path_png)
                root.iconphoto(True, icon)
            except (tk.TclError, FileNotFoundError) as e:
                print(f"Fallback para 'icon_lux.png' falhou: {e}")
                print(f"Verifique se o arquivo 'icon_lux.png' está na pasta do executável ou do script e é um PNG válido (ex.: 32x32 pixels).")
    else:
        try:
            icon_path = resource_path("icon_lux.png")
            if not os.path.exists(icon_path):
                raise FileNotFoundError(f"Arquivo 'icon_lux.png' não encontrado em: {icon_path}")
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
        except (tk.TclError, FileNotFoundError) as e:
            print(f"Erro ao carregar o ícone 'icon_lux.png': {e}")
            print(f"Verifique se o arquivo 'icon_lux.png' está na pasta do executável ou do script e é um PNG válido (ex.: 32x32 pixels).")

    # Configurar o tema e estilo
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Arial", 10))
    style.configure("Update.TButton", background="#0078D7", foreground="white", font=("Arial", 8, "bold"), padding=5, width=20)
    style.map("Update.TButton", background=[("active", "#005BB5")])
    style.configure("Print.TButton", background="#4C75AF", foreground="white", font=("Arial", 8, "bold"), padding=5, width=20)
    style.map("Print.TButton", background=[("active", "#4C50AF")], foreground=[("active", "white")])
    root.configure(bg="#f0f0f0")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.rowconfigure(0, weight=1)

    input_frame = ttk.Frame(root, padding=(10, 50, 10, 0))
    input_frame.grid(row=0, column=0, sticky="nsew")
    preview_frame = ttk.Frame(root, padding=(0, 50, 0, 0))
    preview_frame.grid(row=0, column=1, sticky="nsew")

    # Variáveis para entradas
    largura_var = tk.StringVar(value="15")
    altura_var = tk.StringVar(value="10")
    ip_var = tk.StringVar(value="127.0.0.1")
    titulo_var = tk.StringVar(value="Magazine Torra Torra Ltda")
    volume_var = tk.StringVar(value=str(ler_ultimo_volume() + 1))  # Inicializa com o próximo volume
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

    def get_float(value, field_name):
        """Converte uma string para float, validando se é positiva."""
        if not value:
            return None
        try:
            val = float(value)
            if val <= 0:
                raise ValueError(f"{field_name} deve ser maior que zero.")
            return val
        except ValueError:
            raise ValueError(f"{field_name} deve ser um número válido.")

    def get_int(value, field_name, allow_empty=True):
        """Converte uma string para inteiro, validando se é não-negativo e dentro do limite."""
        if not value and allow_empty:
            return "0"
        try:
            val = int(value)
            if val < 0:
                raise ValueError(f"{field_name} não pode ser negativo.")
            if field_name == "Número do volume" and val > 999999:
                raise ValueError(f"{field_name} não pode exceder 999999.")
            return str(val)
        except ValueError:
            raise ValueError(f"{field_name} deve ser um número inteiro válido.")
    
    def get_string(value, field_name, max_length=50, allow_empty=True):
        """Valida uma string, garantindo que não exceda o comprimento máximo."""
        if not value and allow_empty:
            return "Sem Título"
        if not value:
            raise ValueError(f"{field_name} não pode ser vazio.")
        if len(value) > max_length:
            raise ValueError(f"{field_name} não pode exceder {max_length} caracteres.")
        return value

    def atualizar_visualizacao():
        """Atualiza a pré-visualização da etiqueta"""
        try:
            largura_cm = get_float(largura_var.get(), "Largura da folha")
            altura_cm = get_float(altura_var.get(), "Altura da folha")
            if not largura_cm or not altura_cm:
                raise ValueError("Largura e altura são obrigatórios.")
            
            largura_mm = largura_cm * 10
            altura_mm = altura_cm * 10
            largura_pontos = int(largura_mm * 8)
            altura_pontos = int(altura_mm * 8)

            q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
            q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
            q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
            q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
            total = str(int(q10 or 0) + int(q12 or 0) + int(q14 or 0) + int(q16 or 0))

            volume = get_int(volume_var.get(), "Número do volume", allow_empty=False)
            titulo = get_string(titulo_var.get(), "Título", allow_empty=False)

            d = {
                "titulo": titulo,
                "volume": volume,
                "pedido": pedido_var.get() or "Sem Pedido",
                "nf": nf_var.get() or "Sem NF",
                "descricao": descricao_var.get() or "Sem Descrição",
                "cor": cor_var.get() or "Sem Cor",
                "cod_torra": cod_torra_var.get() or "Sem Código",
                "q10": q10,
                "q12": q12,
                "q14": q14,
                "q16": q16,
                "total": total,
            }

            epl = montar_epl(d, largura_pontos, altura_pontos)
            img = visualizar_epl(epl, largura_pontos, altura_pontos)

            base_size = 500
            new_size = (int(base_size * canvas.scale_factor), int(base_size * canvas.scale_factor))
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            canvas.img = photo
            canvas_width = canvas.winfo_width() or 500
            canvas_height = canvas.winfo_height() or 500
            canvas.delete("all")
            canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo, anchor="center")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            canvas.delete("all")
            canvas.create_text(canvas.winfo_width() / 2 or 250, canvas.winfo_height() / 2 or 250,
                           text="Erro na visualização. Verifique os dados.", anchor="center")

    def zoom(event):
        """Ajusta o zoom da visualização com a roda do mouse."""
        zoom_factor = 1.1 if event.delta > 0 or event.num == 4 else 0.9
        canvas.scale_factor *= zoom_factor
        canvas.scale_factor = max(0.5, min(canvas.scale_factor, 5.0))
        atualizar_visualizacao()

    def start_pan(event):
        """Inicia o arraste da visualização."""
        canvas.scan_mark(event.x, event.y)

    def do_pan(event):
        """Executa o arraste da visualização."""
        canvas.scan_dragto(event.x, event.y, gain=1)

    def proximo_volume():
        """Atualiza o campo 'Número do volume' com o próximo volume do contador."""
        volume_var.set(str(ler_ultimo_volume() + 1))

    def enviar_etiqueta():
        """Envia a etiqueta para a impressora, usando o volume digitado e atualizando o contador."""
        try:
            largura_cm = get_float(largura_var.get(), "Largura da folha")
            altura_cm = get_float(altura_var.get(), "Altura da folha")
            if not largura_cm or not altura_cm:
                raise ValueError("Largura e altura são obrigatórios.")
            ip = ip_var.get()
            if not ip:
                raise ValueError("IP da impressora é obrigatório.")

            largura_mm = largura_cm * 10
            altura_mm = altura_cm * 10
            largura_pontos = int(largura_mm * 8)
            altura_pontos = int(altura_mm * 8)

            q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
            q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
            q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
            q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
            total = str(int(q10 or 0) + int(q12 or 0) + int(q14 or 0) + int(q16 or 0))

            vezes = get_int(vezes_var.get(), "Quantidade de etiquetas", allow_empty=False)
            volume = int(get_int(volume_var.get(), "Número do volume", allow_empty=False))
            titulo = get_string(titulo_var.get(), "Título", allow_empty=False)
            ultimo_volume = ler_ultimo_volume()

            # Alerta para volumes potencialmente duplicados
            if volume <= ultimo_volume:
                resposta = messagebox.askyesno("Aviso", f"O volume {volume} é menor ou igual ao último salvo ({ultimo_volume}). Isso pode causar duplicatas. Continuar?")
                if not resposta:
                    return

            for _ in range(int(vezes)):
                volume_atual = volume
                d = {
                    "titulo": titulo,
                    "volume": str(volume_atual),
                    "pedido": pedido_var.get() or "Sem Pedido",
                    "nf": nf_var.get() or "Sem NF",
                    "descricao": descricao_var.get() or "Sem Descrição",
                    "cor": cor_var.get() or "Sem Cor",
                    "cod_torra": cod_torra_var.get() or "Sem Código",
                    "q10": q10,
                    "q12": q12,
                    "q14": q14,
                    "q16": q16,
                    "total": total,
                }
                epl = montar_epl(d, largura_pontos, altura_pontos)
                if enviar_para_zebra(ip, epl):
                    print(f"Etiqueta enviada. Volume #{volume_atual}")
                    salvar_volume(volume_atual)
                    volume += 1
                else:
                    messagebox.showerror("Erro", "Falha ao enviar para a impressora.")
                    return
            messagebox.showinfo("Sucesso", f"{vezes} etiqueta(s) enviada(s) com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    canvas = tk.Canvas(preview_frame, bg="white", width=500, height=400)
    canvas.pack(expand=True, fill="both")
    canvas.scale_factor = 1.0

    canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<Button-4>", zoom)
    canvas.bind("<Button-5>", zoom)
    canvas.bind("<Button-1>", start_pan)
    canvas.bind("<B1-Motion>", do_pan)

    canvas.create_text(300, 300, text="Preencha os campos e clique em 'Atualizar Visualização'", anchor="center", font=("Arial", 12))

    entries = [
        ("Largura da folha (cm):", largura_var),
        ("Altura da folha (cm):", altura_var),
        ("IP da impressora:", ip_var),
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

    # Configurar o input_frame para expandir
    input_frame = ttk.Frame(root, padding=(20, 50, 15, 50))
    input_frame.grid(row=0, column=0, sticky="nsew")  # Expande em todas as direções
    input_frame.columnconfigure(0, weight=1)  # Labels têm peso menor
    input_frame.columnconfigure(1, weight=3)  # Entradas expandem mais

    # Configurar pesos na janela principal
    root.columnconfigure(0, weight=1)  # input_frame expande
    root.columnconfigure(1, weight=3)  # preview_frame expande mais
    root.rowconfigure(0, weight=1)

    for i, (label, var) in enumerate(entries):
        ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w", padx=(5, 10), pady=5)
        ttk.Entry(input_frame, textvariable=var).grid(row=i, column=1, sticky="ew", pady=3)

    ttk.Button(input_frame, text="Atualizar Visualização", command=atualizar_visualizacao, style="Update.TButton").grid(
        row=len(entries), column=0, sticky="ew", padx=5, pady=10)
    ttk.Button(input_frame, text="Enviar para Impressora", command=enviar_etiqueta, style="Print.TButton").grid(
        row=len(entries), column=1, sticky="ew", padx=5, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()