# 💰 FinTrack v2

Controle financeiro pessoal com backend Python e banco de dados.
Os dados ficam salvos no arquivo `fintrack.db` e não se perdem ao reiniciar.

---

## Arquivos do projeto

```
fintrack-v2/
├── main.py           ← backend (FastAPI + SQLite)
├── requirements.txt  ← dependências Python
├── index.html        ← frontend (abre direto no navegador)
└── fintrack.db       ← banco de dados (criado automaticamente)
```

---

## Como rodar

Siga este passo a passo caso esteja abrindo o projeto pela primeira vez em uma máquina nova para evitar erros de ambiente, comandos não reconhecidos ou falhas de compilação.

### Passo 1: Instalação do Python
Antes de abrir o terminal, certifique-se que o Python estar instalado corretamente.

### Passo 2: Configuração do Ambiente e Comandos
Abra o terminal na pasta do projeto:

```bash
# 1. Criar o ambiente virtual (Aguarde alguns segundos até a linha liberar novamente)
python -m venv venv

# 2. Ativar o ambiente virtual (Obrigatório antes de qualquer instalação ou execução)
# Note que aparecerá um "(venv)" antes do caminho da pasta no seu terminal.
venv\Scripts\activate

# 3. Atualizar o gerenciador de pacotes interno para evitar conflitos de download
python -m pip install --upgrade pip

# 4. Instalar as dependências com os nomes exatos (Atenção ao 'uvicorn' com V)
pip install fastapi uvicorn pydantic
```

### 2. Frontend

Com o backend rodando, abra o `index.html` direto no navegador.

---

## O que mudou em relação à versão anterior

| Antes (só código pyton)    | Agora (HTML + Backend)        |
|----------------------------|-------------------------------|
|                            | Dados no banco SQLite         |
|                            | Persistem para sempre         |
|                            | FastAPI rodando na porta 8000 |

---

## Próximos passos

- [ ] Categorias de gasto
- [ ] Filtrar por tipo (entrada/saída)
- [ ] Dashboard com gráficos
- [ ] Login e múltiplos usuários
