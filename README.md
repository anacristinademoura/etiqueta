# Leia-me: Editor de Etiquetas EPL

Este programa (`etiqueta_epl.py`) permite criar e visualizar etiquetas no formato EPL2 para impressoras Zebra, além de enviá-las para impressão via rede. Ele gera etiquetas com informações como número do volume, pedido, nota fiscal, descrição, cor, código de torra, quantidades por tamanho e total de peças. O programa inclui uma interface gráfica com visualização da etiqueta, zoom, e suporte a ícones personalizados.

## Requisitos

### Software

- **Python 3.6 ou superior**: Necessário para executar o script `.py`.
- **Bibliotecas Python**:
    - **Pillow**: Para renderizar a visualização da etiqueta.
        - Instale com: `pip install Pillow`
    - **PyInstaller (opcional)**: Para gerar o executável `.exe`.
        - Instale com: `pip install pyinstaller`

### Arquivos Necessários

- `etiqueta_epl.py`: O script principal.
- `icon_win.ico`: Ícone para a janela e barra de tarefas no Windows (deve conter resoluções 16x16, 32x32, 64x64 pixels).
- `icon_lux.png`: Ícone alternativo para outros sistemas ou fallback (recomendado: 32x32 pixels).

Coloque esses arquivos na mesma pasta do script (ex.: `C:\Users\SeuUsuario\Documentos\Python\Etiqueta\`).

### Hardware

- Impressora Zebra compatível com EPL2 (ex.: ZP450, ZP500, GK420).
- Conexão de rede: A impressora deve estar na mesma rede que o computador, com um endereço IP acessível.

### Configuração da Impressora

1. **Obtenha o IP da impressora**:
    - Consulte o manual da impressora ou o painel de controle para encontrar o endereço IP (ex.: `192.168.1.100`).
    - Verifique a conexão com:
      ```bash
      ping <IP_DA_IMPRESSORA>
      telnet <IP_DA_IMPRESSORA> 9100
      ```
    Se o Telnet conectar, a impressora está acessível.

2. **Confirme o protocolo**:
    - O programa usa o protocolo EPL2 na porta 9100 (padrão para impressoras Zebra).
    - Verifique no manual da impressora se ela suporta EPL2. Se usar ZPL, o código precisará ser ajustado.

3. **Tamanho do papel**:
    - Configure a impressora para o tamanho de etiqueta correto (padrão no programa: 15 cm x 10 cm).
    - Ajuste os campos **Largura da folha (cm)** e **Altura da folha (cm)** na interface, se necessário.

## Executando o Programa

### Como Script Python (.py)

1. **Verifique as dependências**:
    - Certifique-se de que o **Pillow** está instalado:
      ```bash
      pip install Pillow
      ```

2. **Coloque os arquivos na pasta correta**:
    - Certifique-se de que `etiqueta_epl.py`, `icon_win.ico`, e `icon_lux.png` estão na mesma pasta (ex.: `C:\Users\SeuUsuario\Documentos\Python\Etiqueta\`).

3. **Execute o script**:
    - Abra um terminal na pasta do script e execute:
      ```bash
      python etiqueta_epl.py
      ```

4. **Use a interface**:
    - A interface gráfica abrirá com campos para inserir dados da etiqueta.
    - Preencha os campos:
      - **Largura da folha (cm)**: Tamanho horizontal da etiqueta (ex.: 15).
      - **Altura da folha (cm)**: Tamanho vertical da etiqueta (ex.: 10).
      - **IP da impressora**: Insira o IP da impressora (ex.: `192.168.1.100`).
      - **Número do volume**: Número da etiqueta (ex.: 100). Pode ser editado manualmente e só incrementa ao imprimir.
      - **Outros campos**: Pedido, NF, descrição, cor, código de torra, quantidades por tamanho (10, 12, 14, 16), e quantas etiquetas.
    - Clique em **Atualizar Visualização** para ver a etiqueta.
    - Use a roda do mouse para aplicar zoom e arraste a imagem com o botão esquerdo.
    - Clique em **Enviar para Impressora** para imprimir. O número do volume será incrementado automaticamente após cada impressão.

### Como Executável (.exe)

1. **Gere o .exe com PyInstaller**:
    - Certifique-se de que o **PyInstaller** está instalado:
      ```bash
      pip install pyinstaller
      ```

2. **Na pasta do script, execute**:
    ```bash
    pyinstaller --onefile --windowed --icon=icon_win.ico --add-data "icon_win.ico;." --add-data "icon_lux.png;." --clean etiqueta_epl.py
    ```

    No Linux/Mac, use `:` em vez de `;`:
    ```bash
    pyinstaller --onefile --windowed --icon=icon_win.ico --add-data "icon_win.ico:." --add-data "icon_lux.png:." --clean etiqueta_epl.py
    ```

    O arquivo `etiqueta_epl.exe` será gerado na pasta `dist`.

3. **Execute o .exe**:
    - Navegue até a pasta `dist` (ex.: `C:\Users\SeuUsuario\Documentos\Python\Etiqueta\dist`).
    - Execute `etiqueta_epl.exe`:
      ```bash
      dist\etiqueta_epl.exe
      ```

4. **Use a interface**:
    - Siga as mesmas instruções do modo `.py` para preencher os campos e imprimir.

## Funcionalidades

### Visualização da Etiqueta

- Clique em **Atualizar Visualização** (botão azul) para renderizar a etiqueta com os dados inseridos.
- Use a roda do mouse para aplicar zoom (0.5x a 5.0x) e arraste com o botão esquerdo para mover a imagem.

### Impressão

- Insira o **IP correto da impressora** no campo "IP da impressora".
- Clique em **Enviar para Impressora** (botão azul acinzentado) para enviar a etiqueta.
- O campo **Quantas etiquetas** determina quantas cópias serão impressas, incrementando o volume a cada impressão.

### Número do Volume

- O campo **Número do volume** é inicializado com o próximo número disponível (baseado em `contador_volume.txt`).
- Pode ser editado manualmente para visualização sem alterar o contador.
- O contador é incrementado e salvo em `contador_volume.txt` apenas ao imprimir.

### Ícones

- O programa usa `icon_win.ico` para a janela e barra de tarefas no Windows.
- `icon_lux.png` é usado como fallback ou em outros sistemas.

## Solução de Problemas

### Impressora Não Imprime

#### Causa: IP incorreto ou impressora offline.

- Verifique o IP no campo "IP da impressora".
- Teste a conexão:
  ```bash
  ping <IP_DA_IMPRESSORA>
  telnet <IP_DA_IMPRESSORA> 9100
  ```

Se o telnet conectar, a impressora está acessível.

### Verifique o protocolo:

- O programa usa EPL2 na porta 9100 (padrão para impressoras Zebra).

- Confirme no manual da impressora se ela suporta EPL2. Para ZPL, o código precisa de ajustes.

### Configure o tamanho do papel:

- Ajuste a impressora para o tamanho da etiqueta (padrão: 15 cm x 10 cm).

- Modifique os campos "Largura da folha" e "Altura da folha" na interface, se necessário.

### Instalação e Execução

- Como Script Python (.py)

### Instale as dependências:
```bash
pip install Pillow
```

### Organize os arquivos:

- Coloque etiqueta_epl.py, icon_win.ico, e icon_lux.png na mesma pasta.

### Execute o script:

- Abra um terminal na pasta do script e execute:
```bash
python etiqueta_epl.py
```
Como Executável (.exe)

- Gere o .exe com PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon_win.ico --add-data "icon_win.ico;." --add-data "icon_lux.png;." --clean etiqueta_epl.py
```
- No Linux/Mac, use : em vez de ;:
```bash
pyinstaller --onefile --windowed --icon=icon_win.ico --add-data "icon_win.ico:." --add-data "icon_lux.png:." --clean etiqueta_epl.py
```
O arquivo etiqueta_epl.exe será gerado em dist.

### Execute o .exe:
Navegue até dist (ex.: C:\Users\SeuUsuario\Documentos\Python\Etiqueta\dist).

**Execute:**
```bash
dist\etiqueta_epl.exe
```

### Uso do Programa

**Abra o programa:**

A interface gráfica exibe campos para inserir dados da etiqueta.

**Preencha os campos:**

- Largura da folha (cm): Ex.: 15.
- Altura da folha (cm): Ex.: 10.
- IP da impressora: Insira o IP correto (ex.: 192.168.1.100, não use 127.0.0.1).
- Número do volume: Ex.: 100 (editável, incrementa ao imprimir).
- Número do pedido: Ex.: 123.
- Número da nota fiscal: Ex.: 456.
- Descrição do produto: Ex.: Camiseta.
- Cor do produto: Ex.: Azul.
- Código Torra: Ex.: 789.
- Quantidade tamanho 10, 12, 14, 16: Ex.: 10, 20, 30, 40.
- Quantas etiquetas: Ex.: 1.

**Visualize a etiqueta:**

- Clique em Atualizar Visualização (botão azul).
- Use a roda do mouse para zoom e o botão esquerdo para arrastar.

**Imprima a etiqueta:**

- Clique em Enviar para Impressora (botão azul acinzentado).
- O programa envia a etiqueta para impressora.

Verifique a impressão e a mensagem no console (ex.: Etiqueta enviada. Volume #100).

## Solução de Problemas

**Impressora não imprime:**

- Causa: IP incorreto ou impressora offline.
**Solução:** Verifique o IP e teste com:
```bash
ping <IP_DA_IMPRESSORA>
telnet <IP_DA_IMPRESSORA> 9100
```
Corrija o IP no campo "IP da impressora".

- Causa: Impressora não suporta EPL2.
**Solução:** Confirme o protocolo no manual. Para ZPL, o código precisa de ajustes.

- Causa: Tamanho de papel incorreto.
**Solução:** Ajuste "Largura da folha" e "Altura da folha" na interface.

## Ícone não aparece:

- Causa: Arquivos icon_win.ico ou icon_lux.png ausentes/inválidos.
**Solução:** Confirme que os arquivos estão na pasta e são válidos (ICO: 16x16, 32x32, 64x64; PNG: 32x32).

- Limpe o cache de ícones do Windows:
```bash
taskkill /f /im explorer.exe
del %localappdata%\Microsoft\Windows\Explorer\iconcache*.db
start explorer.exe
```

## Erro na visualização:
- Causa: Campos obrigatórios inválidos.
**Solução:** Preencha "Largura da folha", "Altura da folha", e "Número do volume" com valores válidos.



