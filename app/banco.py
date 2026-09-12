import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def inserir_cofre(dados: dict) -> dict:
    resposta = (
        supabase
        .table("cofres")
        .insert(dados)
        .execute()
    )

    return resposta.data[0]


def buscar_cofre(cofre_id: str) -> dict | None:
    resposta = (
        supabase
        .table("cofres")
        .select("*")
        .eq("id", cofre_id)
        .execute()
    )

    if not resposta.data:
        return None

    return resposta.data[0]


def inserir_segredo(dados: dict) -> dict:
    resposta = (
        supabase
        .table("segredos")
        .insert(dados)
        .execute()
    )

    return resposta.data[0]


def listar_segredos(cofre_id: str) -> list:
    resposta = (
        supabase
        .table("segredos")
        .select("id, titulo, usuario, url, criado_em, atualizado_em")
        .eq("cofre_id", cofre_id)
        .execute()
    )

    return resposta.data


def buscar_segredo(
    cofre_id: str,
    segredo_id: str
) -> dict | None:
    resposta = (
        supabase
        .table("segredos")
        .select("*")
        .eq("id", segredo_id)
        .eq("cofre_id", cofre_id)
        .execute()
    )

    if not resposta.data:
        return None

    return resposta.data[0]


def atualizar_segredo(
    cofre_id: str,
    segredo_id: str,
    dados: dict
) -> dict | None:
    dados["atualizado_em"] = datetime.now(
        timezone.utc
    ).isoformat()

    resposta = (
        supabase
        .table("segredos")
        .update(dados)
        .eq("id", segredo_id)
        .eq("cofre_id", cofre_id)
        .execute()
    )

    if not resposta.data:
        return None

    return resposta.data[0]


def remover_segredo(
    cofre_id: str,
    segredo_id: str
) -> bool:
    segredo = buscar_segredo(cofre_id, segredo_id)

    if segredo is None:
        return False

    (
        supabase
        .table("segredos")
        .delete()
        .eq("id", segredo_id)
        .eq("cofre_id", cofre_id)
        .execute()
    )

    return True