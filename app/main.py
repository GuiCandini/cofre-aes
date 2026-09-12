from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException

from app.modelos import (
    NovoCofre,
    NovoSegredo,
    AtualizarSegredo
)

from app.cripto import (
    ITERACOES_PADRAO,
    gerar_sal,
    para_b64,
    de_b64,
    derivar_chave,
    cifrar,
    decifrar,
    criar_verificador,
    senha_mestra_correta,
    montar_aad
)

from app.banco import (
    inserir_cofre,
    buscar_cofre,
    inserir_segredo,
    listar_segredos,
    buscar_segredo,
    atualizar_segredo,
    remover_segredo
)


app = FastAPI(
    title="Cofre de Senhas",
    description="API de cofre de senhas com AES-GCM e PBKDF2",
    version="1.0.0"
)


def autenticar_cofre(
    cofre_id: str,
    senha_mestra: str
) -> tuple[dict, bytes]:
    """
    Busca o cofre, deriva a chave e confere a senha-mestra.
    """

    cofre = buscar_cofre(cofre_id)

    if cofre is None:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
        chave,
        cofre["verificador_nonce"],
        cofre["verificador_criptograma"],
        cofre["verificador_etiqueta"],
        cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    return cofre, chave


@app.get("/")
def inicio():
    return {
        "mensagem": "API do Cofre de Senhas funcionando"
    }


@app.post("/cofres", status_code=201)
def criar_cofre(dados: NovoCofre):
    cofre_id = str(uuid4())

    sal = gerar_sal()

    chave = derivar_chave(
        dados.senha_mestra,
        sal,
        ITERACOES_PADRAO
    )

    nonce, criptograma, etiqueta = criar_verificador(
        chave,
        cofre_id
    )

    inserir_cofre({
        "id": cofre_id,
        "nome": dados.nome,
        "kdf_sal": para_b64(sal),
        "kdf_iteracoes": ITERACOES_PADRAO,
        "verificador_nonce": nonce,
        "verificador_criptograma": criptograma,
        "verificador_etiqueta": etiqueta
    })

    return {
        "mensagem": "cofre criado com sucesso",
        "cofre_id": cofre_id
    }


@app.post("/cofres/{cofre_id}/abrir")
def abrir_cofre(
    cofre_id: str,
    x_senha_mestra: str = Header(
        ...,
        alias="X-Senha-Mestra"
    )
):
    autenticar_cofre(
        cofre_id,
        x_senha_mestra
    )

    return {
        "mensagem": "senha-mestra correta"
    }


@app.post(
    "/cofres/{cofre_id}/segredos",
    status_code=201
)
def criar_segredo(
    cofre_id: str,
    dados: NovoSegredo,
    x_senha_mestra: str = Header(
        ...,
        alias="X-Senha-Mestra"
    )
):
    _, chave = autenticar_cofre(
        cofre_id,
        x_senha_mestra
    )

    segredo_id = str(uuid4())

    aad = montar_aad(
        cofre_id,
        segredo_id
    )

    nonce, criptograma, etiqueta = cifrar(
        chave,
        dados.senha,
        aad
    )

    inserir_segredo({
        "id": segredo_id,
        "cofre_id": cofre_id,
        "titulo": dados.titulo,
        "usuario": dados.usuario,
        "url": dados.url,
        "nonce": nonce,
        "criptograma": criptograma,
        "etiqueta": etiqueta
    })

    return {
        "mensagem": "segredo criado com sucesso",
        "segredo_id": segredo_id
    }


@app.get("/cofres/{cofre_id}/segredos")
def obter_lista_de_segredos(
    cofre_id: str,
    x_senha_mestra: str = Header(
        ...,
        alias="X-Senha-Mestra"
    )
):
    autenticar_cofre(
        cofre_id,
        x_senha_mestra
    )

    return listar_segredos(cofre_id)


@app.get(
    "/cofres/{cofre_id}/segredos/{segredo_id}"
)
def ler_segredo(
    cofre_id: str,
    segredo_id: str,
    x_senha_mestra: str = Header(
        ...,
        alias="X-Senha-Mestra"
    )
):
    _, chave = autenticar_cofre(
        cofre_id,
        x_senha_mestra
    )

    segredo = buscar_segredo(
        cofre_id,
        segredo_id
    )

    if segredo is None:
        raise HTTPException(
            status_code=404,
            detail="segredo não encontrado"
        )

    aad = montar_aad(
        cofre_id,
        segredo_id
    )

    try:
        senha = decifrar(
            chave,
            segredo["nonce"],
            segredo["criptograma"],
            segredo["etiqueta"],
            aad
        )

    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="registro adulterado"
        )

    return {
        "id": segredo["id"],
        "titulo": segredo["titulo"],
        "usuario": segredo["usuario"],
        "url": segredo["url"],
        "senha": senha
    }


@app.put(
    "/cofres/{cofre_id}/segredos/{segredo_id}"
)
def alterar_segredo(
    cofre_id: str,
    segredo_id: str,
    dados: AtualizarSegredo,
    x_senha_mestra: str = Header(
        ...,
        alias="X-Senha-Mestra"
    )
):
    _, chave = autenticar_cofre(
        cofre_id,
        x_senha_mestra
    )

    segredo_atual = buscar_segredo(
        cofre_id,
        segredo_id
    )

    if segredo_atual is None:
        raise HTTPException(
            status_code=404,
            detail="segredo não encontrado"
        )

    aad = montar_aad(
        cofre_id,
        segredo_id
    )

    # A função cifrar gera obrigatoriamente um nonce novo.
    nonce, criptograma, etiqueta = cifrar(
        chave,
        dados.senha,
        aad
    )

    atualizacao = {
        "titulo": (
            dados.titulo
            if dados.titulo is not None
            else segredo_atual["titulo"]
        ),
        "usuario": (
            dados.usuario
            if dados.usuario is not None
            else segredo_atual["usuario"]
        ),
        "url": (
            dados.url
            if dados.url is not None
            else segredo_atual["url"]
        ),
        "nonce": nonce,
        "criptograma": criptograma,
        "etiqueta": etiqueta
    }

    atualizar_segredo(
        cofre_id,
        segredo_id,
        atualizacao
    )

    return {
        "mensagem": "segredo atualizado com sucesso"
    }


@app.delete(
    "/cofres/{cofre_id}/segredos/{segredo_id}"
)
def excluir_segredo(
    cofre_id: str,
    segredo_id: str,
    x_senha_mestra: str = Header(
        ...,
        alias="X-Senha-Mestra"
    )
):
    autenticar_cofre(
        cofre_id,
        x_senha_mestra
    )

    removido = remover_segredo(
        cofre_id,
        segredo_id
    )

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="segredo não encontrado"
        )

    return {
        "mensagem": "segredo removido com sucesso"
    }