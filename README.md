# Editor de Etiquetas EPL

## Descrição
Este projeto é uma aplicação gráfica em Python para criação e impressão de etiquetas no formato EPL (Eltron Programming Language), compatível com impressoras térmicas como a ELGIN L42Pro e ZDesigner TLP 2844. A aplicação permite:

- Visualização prévia das etiquetas com base no código EPL gerado.
- Impressão direta em impressoras térmicas no Windows.
- Gerenciamento de volumes com salvamento automático e backup.
- Suporte a diferentes grades de tamanhos (10/12/14/16, 1/2/3, 4/5/6, P/M/G).
- Interface gráfica amigável usando Tkinter para preenchimento de dados e visualização.

A aplicação é ideal para ambientes onde é necessário gerar etiquetas personalizadas com informações como número de volume, pedido, descrição, tamanhos e quantidades.

## Requisitos

- **Sistema Operacional**: Windows (impressão direta suportada apenas no Windows).
- **Python**: Versão 3.6 ou superior.
- **Dependências**:
    - Pillow (PIL) para renderização de imagens.
    - pywin32 (apenas no Windows, para comunicação com impressoras).
    - tkinter (geralmente incluído com Python, para a interface gráfica).
- Uma impressora térmica compatível com EPL (ex.: ELGIN L42Pro, ZDesigner TLP 2844).
- Fonte TrueType (ex.: **arial.ttf**) para melhor renderização de texto (opcional).

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu_usuario/editor-etiquetas-epl.git
cd editor-etiquetas-epl
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install pillow pywin32
```

4. Certifique-se de que a fonte **arial.ttf** está disponível no sistema ou ajuste o caminho no código (**visualizar_epl**).

5. Execute a aplicação:
```bash
python main.py
```


## Uso

1. **Iniciar a aplicação**:
    - Execute o script principal (main.py) para abrir a interface gráfica.

2. **Preencher os campos**:
    - Insira informações como título, número do volume, pedido, nota fiscal, descrição, cor, código e quantidades por tamanho.
    - Escolha a grade de tamanhos (10/12/14/16, 1/2/3, 4/5/6 ou P/M/G) no menu suspenso.
    - Defina a quantidade de etiquetas a serem impressas.

3. **Visualizar a etiqueta**:
    - Clique em Atualizar Visualização para ver uma prévia da etiqueta no canvas à direita.
    - Use o mouse para arrastar (pan) ou a roda do mouse para zoom.

4. **Imprimir etiquetas**:
    - Selecione a impressora (ex.: ELGIN L42Pro) no campo "Nome da impressora".
    - Clique em Imprimir Etiqueta para enviar as etiquetas à impressora.
    - O número do volume é incrementado automaticamente e salvo em contador_volume.txt.

5. **Gerenciamento de volumes**:
    - O número do volume é salvo em contador_volume.txt com backup em contador_volume.txt.bak.
    - A aplicação alerta se o número do volume for menor ou igual ao último salvo.

## Estrutura do Projeto
    - main.py: Script principal contendo a lógica da aplicação, interface gráfica e funções de geração/impressão de etiquetas.
    - contador_volume.txt: Arquivo que armazena o último número de volume.
    - contador_volume.txt.bak: Backup do arquivo de volume.
    - icon_win.ico / icon_lux.png: Ícones opcionais para a interface gráfica (Windows/Linux).

## Funcionalidades Principais
    - Geração de EPL: Monta o código EPL com base nos dados fornecidos, suportando diferentes grades de tamanhos.
    - Visualização: Renderiza a etiqueta como uma imagem usando a biblioteca PIL, com suporte a texto rotacionado e fontes TrueType.
    - Impressão: Envia o código EPL diretamente para a impressora via **pywin32** (Windows).
    - Interface Gráfica: Interface intuitiva com Tkinter, incluindo campos dinâmicos para quantidades e suporte a zoom/arrastar na visualização.
    - Gerenciamento de Erros: Validações para entradas numéricas, tamanhos de texto e compatibilidade com a impressora.

## Limitações
    - Impressão: Suportada apenas no Windows devido à dependência do pywin32.
    - Fonte: A renderização de texto depende de uma fonte TrueType (ex.: arial.ttf). Caso não esteja disponível, usa a fonte padrão do PIL.
    - Grades de tamanhos: Suporta apenas as grades predefinidas (10/12/14/16, 1/2/3, 4/5/6, P/M/G).
    - Resolução: A visualização é otimizada para etiquetas de 10cm x 15cm (80 pontos/cm).

## Contribuição
    - Faça um fork do repositório.
    - Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade).
    - Commit suas alterações (git commit -m 'Adiciona nova funcionalidade').
    - Push para a branch (git push origin feature/nova-funcionalidade).
    - Abra um Pull Request.

## Licença
Este projeto está licenciado sob a MIT License.

## Contato
Para dúvidas ou sugestões, entre em contato pelo GitHub Issues ou via e-mail: seu_email@exemplo.com.



