# 🏛️ PI_CAMARA_DEPUTADOS

## 🛠️ Configuração do Ambiente (PDM)
Este projeto utiliza o **PDM** como gerenciador de pacotes e ambientes virtuais, garantindo o isolamento das dependências de Ciência de Dados.

### 1. Instalar o PDM
Se você ainda não tem o PDM instalado na sua máquina/VM Linux:

`curl -sSL https://pdm-project.org/install-pdm.py | python3 -`

### 2. Inicializar o ambiente e instalar dependências
Após clonar o repositório, navegue até a pasta do projeto e execute:

`pdm install`

### 3. Utilizar o Kernel no Jupyter/VS Code
Para que o VS Code reconheça as bibliotecas instaladas pelo PDM dentro da sua VM:

1. Certifique-se de que o ipykernel está instalado: `pdm add ipykernel`
2. No VS Code, abra o arquivo `.ipynb`.
3. No canto superior direito, clique em **Select Kernel** > **Python Environments**.
4. Aponte para o executável que está em: `./.venv/bin/python`.

---

### 4. Comandos úteis do PDM
* **Adicionar nova biblioteca:** `pdm add nome-da-lib`
* **Remover biblioteca:** `pdm remove nome-da-lib`
* **Rodar script python:** `pdm run python seu_script.py`
* **Sincronizar ambiente:** `pdm sync`

---

### 📂 Dica para o Git: `.gitignore`
Como o PDM cria uma pasta `.venv` dentro do projeto, certifique-se de que o seu arquivo `.gitignore` ignore essa pasta:

**Conteúdo do .gitignore:**
`.venv/`
`__pycache__/`
`.pdm-python`
`.pdm-build/`

**Por que manter o pdm.lock fora do gitignore?** Em Ciência de Dados, é comum manter o `pdm.lock` no Git para garantir que todos os membros do time usem exatamente as mesmas versões das bibliotecas (Pandas, Plotly, etc.), evitando o famoso "na minha máquina funciona".