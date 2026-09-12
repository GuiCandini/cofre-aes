import base64

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


ITERACOES_PADRAO = 210_000
TAMANHO_CHAVE = 32
TAMANHO_SAL = 16
TAMANHO_NONCE = 12

FRASE_VERIFICADORA = "cofre-ok"


def para_b64(dados: bytes) -> str:
    """Converte bytes para texto em Base64."""
    return base64.b64encode(dados).decode("utf-8")


def de_b64(texto: str) -> bytes:
    """Converte um texto Base64 novamente para bytes."""
    return base64.b64decode(texto.encode("utf-8"))


def derivar_chave(
    senha_mestra: str,
    sal: bytes,
    iteracoes: int
) -> bytes:
    """Transforma a senha-mestra em uma chave de 32 bytes."""

    return PBKDF2(
        senha_mestra.encode("utf-8"),
        sal,
        dkLen=TAMANHO_CHAVE,
        count=iteracoes,
        hmac_hash_module=SHA256
    )


def gerar_sal() -> bytes:
    """Gera um sal aleatório para o cofre."""
    return get_random_bytes(TAMANHO_SAL)


def cifrar(
    chave: bytes,
    texto_claro: str,
    aad: bytes
) -> tuple[str, str, str]:
    """
    Cifra um texto e devolve:
    nonce, criptograma e etiqueta em Base64.
    """

    nonce = get_random_bytes(TAMANHO_NONCE)

    cifra = AES.new(
        chave,
        AES.MODE_GCM,
        nonce=nonce
    )

    cifra.update(aad)

    criptograma, etiqueta = cifra.encrypt_and_digest(
        texto_claro.encode("utf-8")
    )

    return (
        para_b64(nonce),
        para_b64(criptograma),
        para_b64(etiqueta)
    )


def decifrar(
    chave: bytes,
    nonce_b64: str,
    cripto_b64: str,
    etiqueta_b64: str,
    aad: bytes
) -> str:
    """Decifra o texto e verifica a etiqueta."""

    nonce = de_b64(nonce_b64)
    criptograma = de_b64(cripto_b64)
    etiqueta = de_b64(etiqueta_b64)

    cifra = AES.new(
        chave,
        AES.MODE_GCM,
        nonce=nonce
    )

    cifra.update(aad)

    texto_claro = cifra.decrypt_and_verify(
        criptograma,
        etiqueta
    )

    return texto_claro.decode("utf-8")


def criar_verificador(
    chave: bytes,
    cofre_id: str
) -> tuple[str, str, str]:
    """Cria o verificador da senha-mestra."""

    return cifrar(
        chave,
        FRASE_VERIFICADORA,
        cofre_id.encode("utf-8")
    )


def senha_mestra_correta(
    chave: bytes,
    nonce: str,
    cripto: str,
    etiqueta: str,
    cofre_id: str
) -> bool:
    """Confere se a senha-mestra está correta."""

    try:
        texto = decifrar(
            chave,
            nonce,
            cripto,
            etiqueta,
            cofre_id.encode("utf-8")
        )

        return texto == FRASE_VERIFICADORA

    except ValueError:
        return False


def montar_aad(cofre_id: str, segredo_id: str) -> bytes:
    """Monta os dados associados de um segredo."""

    return f"{cofre_id}|{segredo_id}".encode("utf-8")