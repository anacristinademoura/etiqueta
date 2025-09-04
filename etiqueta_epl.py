import socket
import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

COUNTER_FILE = "contador_volume.txt"


def visualizar_epl(epl_code, largura_pontos, altura_pontos):
    img = Image.new("RGB", (largura_pontos, altura_pontos), "white")
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("arial.ttf", 72)  # Aumentado para corresponder à escala 10,10
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

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
            font = font_large if fonte == 5 and escala_x >= 7 else font_small
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

    img.save("etiqueta.png")
    return img


def ler_proximo_volume():
    n = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                n = int(f.read().strip() or "0")
        except:
            n = 0
    n += 1
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        f.write(str(n))
    return n


def enviar_para_zebra(ip, epl, porta=9100, timeout=5):
    try:
        with socket.create_connection((ip, porta), timeout=timeout) as s:
            s.sendall(epl.encode("utf-8"))
        return True
    except Exception as e:
        print(f"Erro ao enviar etiqueta: {e}")
        return False


def montar_epl(d, largura_pontos, altura_pontos):
    return f"""
N
q{largura_pontos}
Q{altura_pontos},24

; Título
A100,20,0,5,10,10,N,"Magazine Torra Torra Ltda"

; Linhas horizontais da tabela
LO24,120,{largura_pontos-48},2
LO24,160,{largura_pontos-48},2
LO24,200,{largura_pontos-48},2
LO24,240,{largura_pontos-48},2
LO24,280,{largura_pontos-48},2
LO24,320,{largura_pontos-48},2
LO24,360,{largura_pontos-48},2
LO24,400,{largura_pontos-48},2
LO24,440,{largura_pontos-48},2
LO24,480,{largura_pontos-48},2
LO160,520,314,2
LO704,520,224,2
LO24,560,{largura_pontos-48},2

; Linhas verticais da tabela
LE24,120,0,440,2
LE160,120,0,440,2
LE360,240,0,320,2
LE360,120,0,80,2
LE472,120,0,80,2
LE472,240,0,320,2
LE704,120,0,40,2
LE704,240,0,320,2
LE928,120,0,440,2
LE528,240,0,320,2
LE588,240,0,320,2
LE648,240,0,320,2

; Conteúdo da tabela

; Linha 1
A32,132,0,3,1,1,N,"Nº do Volume"
A176,132,0,3,1,1,N,"{d['volume']}"
A480,132,0,3,1,1,N,"Ref.Cod.Torra"
A712,132,0,3,1,1,N,"{d['cod_torra']}"

; Linha 2
A32,172,0,3,1,1,N,"Nº do Pedido"
A168,172,0,3,1,1,N,"{d['pedido']}"
A368,172,0,3,1,1,N,"N.F."
A480,172,0,3,1,1,N,"{d['nf']}"

; Linha 3
A32,212,0,3,1,1,N,"Descrição"
A172,212,0,3,1,1,N,"{d['descricao']}"

; Linha 4
A368,252,0,3,1,1,N,"Cor"
A488,252,0,3,1,1,N,"10"
A544,252,0,3,1,1,N,"12"
A600,252,0,3,1,1,N,"14"
A664,252,0,3,1,1,N,"16"

; Linha 7
A368,372,0,3,1,1,N,"{d['cor']}"
A488,372,0,3,1,1,N,"{d['q10']}"
A544,372,0,3,1,1,N,"{d['q12']}"
A600,372,0,3,1,1,N,"{d['q14']}"
A664,372,0,3,1,1,N,"{d['q16']}"

; Linha 10
A36,496,0,3,1,1,N,"Total de"
A168,496,0,3,1,1,N,"peças caixa"
A168,528,0,3,1,1,N,"{d['total']}"
A488,504,0,3,1,1,N,"{d['q10']}"
A544,504,0,3,1,1,N,"{d['q12']}"
A600,504,0,3,1,1,N,"{d['q14']}"
A664,504,0,3,1,1,N,"{d['q16']}"

P1
""".strip() + "\n"


def create_gui():
    root = tk.Tk()
    root.title("Editor de Etiquetas EPL")
    root.geometry("800x600")

    # Frame para entradas
    input_frame = ttk.Frame(root, padding="10")
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Frame para visualização
    preview_frame = ttk.Frame(root, padding="10")
    preview_frame.grid(row=0, column=1, sticky="nsew")

    # Variáveis para entradas (inicializadas como vazias)
    largura_var = tk.StringVar(value="15")
    altura_var = tk.StringVar(value="10")
    ip_var = tk.StringVar(value="")
    pedido_var = tk.StringVar(value="")
    nf_var = tk.StringVar(value="")
    descricao_var = tk.StringVar(value="")
    cor_var = tk.StringVar(value="")
    cod_torra_var = tk.StringVar(value="")
    q10_var = tk.StringVar(value="")
    q12_var = tk.StringVar(value="")
    q14_var = tk.StringVar(value="")
    q16_var = tk.StringVar(value="")
    vezes_var = tk.StringVar(value="1")

    # Função para validar e obter número float
    def get_float(value, field_name):
        if not value:
            return None
        try:
            val = float(value)
            if val <= 0:
                raise ValueError(f"{field_name} deve ser maior que zero.")
            return val
        except ValueError:
            raise ValueError(f"{field_name} deve ser um número válido.")

    # Função para validar e obter número inteiro
    def get_int(value, field_name, allow_empty=True):
        if not value and allow_empty:
            return "0"
        try:
            val = int(value)
            if val < 0:
                raise ValueError(f"{field_name} não pode ser negativo.")
            return str(val)
        except ValueError:
            raise ValueError(f"{field_name} deve ser um número inteiro válido.")

    # Função para atualizar a visualização
    def atualizar_visualizacao():
        try:
            # Validar campos obrigatórios
            largura_cm = get_float(largura_var.get(), "Largura da folha")
            altura_cm = get_float(altura_var.get(), "Altura da folha")
            if not largura_cm or not altura_cm:
                raise ValueError("Largura e altura são obrigatórios.")

            largura_mm = largura_cm * 10
            altura_mm = altura_cm * 10
            largura_pontos = int(largura_mm * 8)
            altura_pontos = int(altura_mm * 8)

            # Validar quantidades
            q10 = get_int(q10_var.get(), "Quantidade tamanho 10")
            q12 = get_int(q12_var.get(), "Quantidade tamanho 12")
            q14 = get_int(q14_var.get(), "Quantidade tamanho 14")
            q16 = get_int(q16_var.get(), "Quantidade tamanho 16")
            total = str(int(q10 or 0) + int(q12 or 0) +
                        int(q14 or 0) + int(q16 or 0))

            # Usar valores vazios para campos não obrigatórios
            d = {
                "volume": ler_proximo_volume(),
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

            # Redimensionar imagem para caber na tela
            img.thumbnail((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            preview_label.configure(image=photo)
            preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            preview_label.configure(image=None, text="Erro na visualização. Verifique os dados.")

    # Função para enviar para a impressora
    def enviar_etiqueta():
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
            total = str(int(q10 or 0) + int(q12 or 0) +
                        int(q14 or 0) + int(q16 or 0))

            vezes = get_int(vezes_var.get(), "Quantidade de etiquetas", allow_empty=False)

            for _ in range(int(vezes)):
                d = {
                    "volume": ler_proximo_volume(),
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
                    print(f"Etiqueta enviada. Volume #{d['volume']}")
                else:
                    messagebox.showerror("Erro", "Falha ao enviar para a impressora.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Campos de entrada
    entries = [
        ("Largura da folha (cm):", largura_var),
        ("Altura da folha (cm):", altura_var),
        ("IP da impressora:", ip_var),
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
        ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
        ttk.Entry(input_frame, textvariable=var).grid(row=i, column=1, sticky="ew", pady=2)

    # Botões
    ttk.Button(input_frame, text="Atualizar Visualização", command=atualizar_visualizacao).grid(row=len(entries), column=0, columnspan=2, pady=10)
    ttk.Button(input_frame, text="Enviar para Impressora", command=enviar_etiqueta).grid(row=len(entries)+1, column=0, columnspan=2, pady=10)

    # Área de visualização
    preview_label = ttk.Label(preview_frame, text="Preencha os campos e clique em 'Atualizar Visualização'")
    preview_label.grid(row=0, column=0)

    root.mainloop()


if __name__ == "__main__":
    create_gui()