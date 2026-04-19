# pi_camara_deputados

🛠 Configuração do Ambiente de Desenvolvimento
Este projeto utiliza o PDM (Python Development Master) para gerenciar dependências e ambientes virtuais. Isso garante que todos utilizem as mesmas versões de bibliotecas e evita conflitos com o Python do sistema.

1. Pré-requisitos
Antes de começar, você precisa ter o pipx instalado para gerenciar o PDM isoladamente:

Bash
# Instalar pipx
sudo apt update
sudo apt install pipx
pipx ensurepath
(Reinicie o terminal após a instalação do pipx)

2. Instalação do PDM
Com o pipx pronto, instale o PDM globalmente:

Bash
pipx install pdm
3. Inicializando o Projeto
Após clonar o repositório, entre na pasta e sincronize as dependências:

Bash
pdm install
Este comando criará automaticamente uma pasta .venv local e instalará todas as bibliotecas listadas no arquivo pdm.lock.

📦 Gestão de Bibliotecas
Para manter o ambiente de todos sincronizado, não utilize pip install. Use os comandos do PDM:

Adicionar uma nova biblioteca
Se precisar de uma nova biblioteca (ex: pandas), execute:

Bash
pdm add pandas
Isso atualizará os arquivos pyproject.toml e pdm.lock. Não esqueça de commitar esses arquivos no Git.

Adicionar dependências de desenvolvimento
Para ferramentas de teste ou formatação (ex: pytest):

Bash
pdm add -d pytest
Executar o código
Para garantir que o Python utilize o ambiente correto:

Bash
pdm run python seu_script.py
💡 Dica: VS Code
Para que o VS Code reconheça as bibliotecas instaladas:

Pressione Ctrl + Shift + P.

Digite Python: Select Interpreter.

Escolha o interpretador que aponta para a pasta .venv dentro deste projeto.

Deseja que eu adicione uma seção específica sobre como rodar o banco de dados que você está desenvolvendo para a faculdade?