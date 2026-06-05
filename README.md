# Finance — Controle Financeiro Pessoal

Controle financeiro com visão mensal. Registre entradas e saídas,
navegue entre meses e acompanhe seu saldo mês a mês.

---

## Arquivos do projeto

```
finance/
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

## Funcionalidades

- Registrar entradas e saídas com descrição
- Resumo do mês: saldo, total de entradas e saídas
- Navegar entre meses com as setas ‹ ›
- Dados salvos no banco SQLite (não se perdem ao reiniciar)

---

## Próximos passos

- [ ] Categorias (Moradia, Mercado,Transporte...)
- [ ] Filtrar por tipo (entrada/saída)
- [ ] Gráfico de gastos por categoria
- [ ] Login e múltiplos usuários
