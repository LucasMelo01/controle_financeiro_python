from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import sqlite3
import os

app = FastAPI(title="FinTrack API")

# Permite o HTML abrir direto no navegador conversar com o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de dados (SQLite) ───
# O arquivo fintrack.db é criado automaticamente na mesma pasta
DB = os.path.join(os.path.dirname(__file__), "fintrack.db")

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # retorna dicionários em vez de tuplas
    return conn

def criar_tabela():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo      TEXT    NOT NULL,
                valor     REAL    NOT NULL,
                descricao TEXT    NOT NULL,
                data      TEXT    NOT NULL
            )
        """)

criar_tabela()  # roda ao iniciar o servidor

# Schema ────
class TransacaoEntrada(BaseModel):
    tipo: str       # 'entrada' ou 'saida'
    valor: float
    descricao: str
    data: Optional[str] = None

# Rotas ─────

@app.get("/transacoes")
def listar():
    """Retorna todas as transações + saldo calculado"""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM transacoes ORDER BY id DESC"
        ).fetchall()

    transacoes = [dict(r) for r in rows]

    entradas = sum(t["valor"] for t in transacoes if t["tipo"] == "entrada")
    saidas   = sum(t["valor"] for t in transacoes if t["tipo"] == "saida")

    return {
        "transacoes":     transacoes,
        "saldo":          entradas - saidas,
        "total_entradas": entradas,
        "total_saidas":   saidas,
    }


@app.post("/transacoes", status_code=201)
def adicionar(dados: TransacaoEntrada):
    """Adiciona uma nova transação no banco"""
    if dados.tipo not in ("entrada", "saida"):
        raise HTTPException(400, "tipo deve ser 'entrada' ou 'saida'")
    if dados.valor <= 0:
        raise HTTPException(400, "valor deve ser maior que zero")

    data = dados.data or datetime.now().strftime("%d/%m/%Y %H:%M")

    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO transacoes (tipo, valor, descricao, data) VALUES (?, ?, ?, ?)",
            (dados.tipo, dados.valor, dados.descricao, data)
        )
        novo_id = cursor.lastrowid

    return {"id": novo_id, "tipo": dados.tipo, "valor": dados.valor,
            "descricao": dados.descricao, "data": data}


@app.delete("/transacoes/{id}", status_code=204)
def deletar(id: int):
    """Remove uma transação pelo id"""
    with get_conn() as conn:
        alteradas = conn.execute(
            "DELETE FROM transacoes WHERE id = ?", (id,)
        ).rowcount

    if alteradas == 0:
        raise HTTPException(404, "Transação não encontrada")
