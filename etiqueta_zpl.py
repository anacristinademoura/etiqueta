# import socket
# import os

# COUNTER_FILE = "contador_volume.txt"


# def ler_proximo_volume():
#     n = 0
#     if os.path.exists(COUNTER_FILE):
#         try:
#             with open(COUNTER_FILE, "r", encoding="utf-8") as f:
#                 n = int(f.read().strip() or "0")
#         except:
#             n = 0
#     n += 1
#     with open(COUNTER_FILE, "w", encoding="utf-8") as f:
#         f.write(str(n))
#     return n


# def enviar_para_zebra(ip, zpl, porta=9100, timeout=5):
#     try:
#         with socket.create_connection((ip, porta), timeout=timeout) as s:
#             s.sendall(zpl.encode("utf-8"))
#         print("Etiqueta enviada com sucesso para a impressora.")
#     except Exception as e:
#         print(f"Erro ao enviar etiqueta: {e}")


# def montar_zpl(d):
#     return f"""
# ^XA
# ^CI28
# ^FWN ; Rotação de 90 graus (texto vertical de cima para baixo)
# ^PW1400
# ^LL1200
# ^LH0,0

# ; Titulo
# ^FO140,70^A2N,50,30^FDMagazine Torra Torra Ltda^FS

# ; Linhas internas da tabela
# ^FO30,150^GB1130,0,2^FS
# ^FO30,200^GB1130,0,2^FS 
# ^FO30,250^GB1130,0,2^FS
# ^FO30,300^GB1130,0,2^FS
# ^FO30,350^GB1130,0,2^FS
# ^FO30,400^GB1130,0,2^FS
# ^FO30,450^GB1130,0,2^FS
# ^FO30,500^GB1130,0,2^FS
# ^FO30,550^GB1130,0,2^FS
# ^FO30,600^GB1130,0,2^FS

# ^FO200,650^GB393,0,2^FS ; Linha cortada 1
# ^FO880,650^GB280,0,2^FS ; Linha cortada 2

# ^FO30,700^GB1130,0,2^FS

# ; Coluna vertical
# ^FO30,150^GB0,550,2^FS ; Coluna vertical esquerda

# ^FO200,150^GB0,550,2^FS

# ^FO450,300^GB0,400,2^FS ; Coluna cortada 1
# ^FO450,150^GB0,100,2^FS ; Coluna cortada 2

# ^FO590,150^GB0,100,2^FS ; Coluna cortada 3
# ^FO590,300^GB0,400,2^FS ; Coluna cortada 4

# ^FO880,150^GB0,50,2^FS ; Coluna cortada 5
# ^FO880,300^GB0,400,2^FS ; Coluna cortada 6

# ^FO1160,150^GB0,550,2^FS ; Coluna vertical esquerda

# ; Colunas menores nas células
# ^FO660,300^GB0,400,2^FS
# ^FO735,300^GB0,400,2^FS
# ^FO810,300^GB0,400,2^FS

# ; Conteúdo da tabela

# ; Linha 1
# ^FO40,165^A0N,30,28^FDNº do Volume^FS ; Célula 1
# ^FO220,165^A0N,30,28^FD{d['volume']}^FS ; Célula 2
# ^FO460,165^A0N,30,28^FD^FS ; Célula 3
# ^FO600,165^A0N,30,28^FDRef.Cod.Torra^FS ; Célula 4
# ^FO890,165^A0N,30,28^FD{d['cod_torra']}^FS ; Célula 5

# ; Linha 2
# ^FO40,215^A0N,30,28^FDNº do Pedido^FS ; Célula 1
# ^FO210,215^A0N,30,28^FD{d['pedido']}^FS ; Célula 2
# ^FO460,215^A0N,30,28^FDN.F.^FS ; Célula 3
# ^FO600,215^A0N,30,28^FD{d['nf']}^FS ; Célula 4

# ; Linha 3
# ^FO40,265^A0N,30,28^FDDescrição^FS ; Célula 1
# ^FO215,265^A0N,30,28^FD{d['descricao']}^FS ; Célula 2
# ^FO460,265^A0N,30,28^FD^FS ; Célula 3
# ^FO600,265^A0N,30,28^FD^FS ; Célula 4

# ; Linha 4
# ^FO40,315^A0N,30,28^FD^FS ; Célula 1
# ; Célula 2
# ^FO460,315^A0N,30,28^FDCor^FS ; Célula 3

# ^FO610,315^A0N,30,28^FD10^FS ; Célula 4
# ^FO680,315^A0N,30,28^FD12^FS ; Célula 5
# ^FO750,315^A0N,30,28^FD14^FS ; Célula 6
# ^FO830,315^A0N,30,28^FD16^FS ; Célula 7

# ^FO890,315^A0N,30,28^FD^FS ; Célula 8

# ; Linha 5
# ^FO40,365^A0N,30,28^FD^FS ; Célula 1
# ^FO210,365^A0N,30,28^FD^FS ; Célula 2
# ^FO460,365^A0N,30,28^FD^FS ; Célula 3

# ^FO610,365^A0N,30,28^FD^FS ; Célula 4
# ^FO680,365^A0N,30,28^FD^FS ; Célula 5
# ^FO750,365^A0N,30,28^FD^FS ; Célula 6
# ^FO830,365^A0N,30,28^FD^FS ; Célula 7

# ^FO890,365^A0N,30,28^FD^FS ; Célula 8

# ; Linha 6
# ^FO40,410^A0N,30,28^FD^FS ; Célula 1
# ^FO210,410^A0N,30,28^FD^FS ; Célula 2
# ^FO460,410^A0N,30,28^FD^FS ; Célula 3

# ^FO610,410^A0N,30,28^FD^FS ; Célula 4
# ^FO680,410^A0N,30,28^FD^FS ; Célula 5
# ^FO750,410^A0N,30,28^FD^FS ; Célula 6
# ^FO830,410^A0N,30,28^FD^FS ; Célula 7

# ^FO890,410^A0N,30,28^FD^FS ; Célula 8

# ; Linha 7
# ^FO40,460^A0N,30,28^FD^FS ; Célula 1
# ^FO210,460^A0N,30,28^FD^FS ; Célula 2
# ^FO460,460^A0N,30,28^FD{d['cor']}^FS ; Célula 3

# ^FO610,460^A0N,30,28^FD{d['q10']}^FS ; Célula 4
# ^FO680,460^A0N,30,28^FD{d['q12']}^FS ; Célula 5
# ^FO750,460^A0N,30,28^FD{d['q14']}^FS ; Célula 6
# ^FO830,460^A0N,30,28^FD{d['q16']}^FS ; Célula 7

# ^FO890,460^A0N,30,28^FD^FS ; Célula 8

# ; Linha 8
# ^FO40,510^A0N,30,28^FD^FS ; Célula 1
# ^FO210,510^A0N,30,28^FD^FS ; Célula 2
# ^FO460,510^A0N,30,28^FD^FS ; Célula 3

# ^FO610,510^A0N,30,28^FD^FS ; Célula 4
# ^FO680,510^A0N,30,28^FD^FS ; Célula 5
# ^FO750,510^A0N,30,28^FD^FS ; Célula 6
# ^FO830,510^A0N,30,28^FD^FS ; Célula 7

# ^FO890,510^A0N,30,28^FD^FS ; Célula 8

# ; Linha 9
# ^FO40,560^A0N,30,28^FD^FS ; Célula 1
# ^FO210,560^A0N,30,28^FD^FS ; Célula 2
# ^FO460,560^A0N,30,28^FD^FS ; Célula 3

# ^FO610,560^A0N,30,28^FD^FS ; Célula 4
# ^FO680,560^A0N,30,28^FD^FS ; Célula 5
# ^FO750,560^A0N,30,28^FD^FS ; Célula 6
# ^FO830,560^A0N,30,28^FD^FS ; Célula 7
# ^FO890,560^A0N,30,28^FD^FS ; Célula 8

# ; Linha 10
# ^FO45,620^A0N,30,28^FDTotal de ^FS ; Célula 1
# ^FO210,610^A0N,30,28^FD^FS ; Célula 2
# ^FO460,610^A0N,30,28^FD^FS ; Célula 3

# ^FO610,630^A0N,30,28^FD{d['q10']}^FS ; Célula 4
# ^FO680,630^A0N,30,28^FD{d['q12']}^FS ; Célula 5
# ^FO750,630^A0N,30,28^FD{d['q14']}^FS ; Célula 6
# ^FO830,630^A0N,30,28^FD{d['q16']}^FS ; Célula 7

# ^FO890,610^A0N,30,28^FD^FS ; Célula 8

# ; Linha 11
# ^FO45,650^A0N,30,28^FDpeças caixa^FS ; Célula 1
# ^FO210,660^A0N,30,28^FD{d['total']}^FS ; Célula 2
# ^FO460,660^A0N,30,28^FD^FS ; Célula 3
# ^FO890,660^A0N,30,28^FD^FS ; Célula 4

# ^XZ
# """.strip() + "\n"


# def main():
#     print("=== Impressão de Etiquetas ===")

#     ip = input("IP da impressora: ")
#     pedido = input("Número do pedido: ")
#     nf = input("Número da nota fiscal: ")
#     descricao = input("Descrição do produto: ")
#     cor = input("Cor do produto: ")
#     cod_torra = input("Código Torra: ")
#     q10 = input("Quantidade tamanho 10: ")
#     q12 = input("Quantidade tamanho 12: ")
#     q14 = input("Quantidade tamanho 14: ")
#     q16 = input("Quantidade tamanho 16: ")
    
#     total = str(int(q10 or 0) + int(q12 or 0) + int(q14 or 0) + int(q16 or 0))

#     vezes = int(input("Quantas etiquetas deseja imprimir? "))

#     for _ in range(vezes):
#         volume = ler_proximo_volume()
#         d = {
#             "volume": volume,
#             "pedido": pedido,
#             "nf": nf,
#             "descricao": descricao,
#             "cor": cor,
#             "cod_torra": cod_torra,
#             "q10": q10,
#             "q12": q12,
#             "q14": q14,
#             "q16": q16,
#             "total": total,
#         }
#         zpl = montar_zpl(d)
#         print("\nZPL gerado:\n", zpl)
#         enviar_para_zebra(ip, zpl)
#         print(f"Etiqueta enviada. Volume #{volume}\n")


# if __name__ == "__main__":
#     main()
