from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import sqlite3
import os

app = FastAPI(title="Finance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Banco de dados ───────────────────────────────────────────────────────────
DB = os.path.join(os.path.dirname(__file__), "finance.db")

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo      TEXT NOT NULL,
                valor     REAL NOT NULL,
                descricao TEXT NOT NULL,
                data      TEXT NOT NULL,
                mes       TEXT NOT NULL  -- formato: "2025-06" para filtrar por mês
            )
        """)

criar_tabela()

# ─── Schema ───────────────────────────────────────────────────────────────────
class TransacaoEntrada(BaseModel):
    tipo: str
    valor: float
    descricao: str
    data: Optional[str] = None

# ─── Rotas ────────────────────────────────────────────────────────────────────

@app.get("/transacoes")
def listar(mes: Optional[str] = Query(None, description="Formato: YYYY-MM, ex: 2025-06")):
    """
    Retorna transações filtradas por mês.
    Se não informar o mês, retorna o mês atual.
    """
    if not mes:
        mes = datetime.now().strftime("%Y-%m")

    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM transacoes WHERE mes = ? ORDER BY id DESC",
            (mes,)
        ).fetchall()

    transacoes = [dict(r) for r in rows]

    entradas = sum(t["valor"] for t in transacoes if t["tipo"] == "entrada")
    saidas   = sum(t["valor"] for t in transacoes if t["tipo"] == "saida")

    return {
        "mes":            mes,
        "transacoes":     transacoes,
        "saldo":          entradas - saidas,
        "total_entradas": entradas,
        "total_saidas":   saidas,
    }


@app.get("/meses")
def listar_meses():
    """Retorna todos os meses que possuem transações registradas"""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT mes FROM transacoes ORDER BY mes DESC"
        ).fetchall()

    meses = [r["mes"] for r in rows]

    # Garante que o mês atual sempre aparece na lista
    mes_atual = datetime.now().strftime("%Y-%m")
    if mes_atual not in meses:
        meses.insert(0, mes_atual)

    return {"meses": meses}


@app.post("/transacoes", status_code=201)
def adicionar(dados: TransacaoEntrada):
    if dados.tipo not in ("entrada", "saida"):
        raise HTTPException(400, "tipo deve ser 'entrada' ou 'saida'")
    if dados.valor <= 0:
        raise HTTPException(400, "valor deve ser maior que zero")

    agora = datetime.now()
    data  = dados.data or agora.strftime("%d/%m/%Y %H:%M")
    mes   = agora.strftime("%Y-%m")  # extrai o mês da data atual

    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO transacoes (tipo, valor, descricao, data, mes) VALUES (?, ?, ?, ?, ?)",
            (dados.tipo, dados.valor, dados.descricao, data, mes)
        )
        novo_id = cursor.lastrowid

    return {
        "id": novo_id, "tipo": dados.tipo, "valor": dados.valor,
        "descricao": dados.descricao, "data": data, "mes": mes
    }


@app.delete("/transacoes/{id}", status_code=204)
def deletar(id: int):
    with get_conn() as conn:
        alteradas = conn.execute(
            "DELETE FROM transacoes WHERE id = ?", (id,)
        ).rowcount

    if alteradas == 0:
        raise HTTPException(404, "Transação não encontrada")

