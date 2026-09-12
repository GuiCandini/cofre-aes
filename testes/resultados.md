# Resultados dos testes

## Teste 1 — Nonces distintos

Foram cadastrados dois segredos contendo a mesma senha.

Resultado observado: os campos nonce e criptograma ficaram diferentes.

Conclusão: o sistema gera um nonce aleatório para cada operação de cifragem.

Evidência: `evidencias/teste1-nonces-diferentes.png`

## Teste 2 — Senha-mestra incorreta

Foi realizada uma tentativa de leitura com uma senha-mestra incorreta.

Resultado observado: a API retornou o código HTTP 401 e não apresentou o conteúdo do segredo.

Evidência: `evidencias/teste2-senha-incorreta.png`

## Teste 3 — Dados visualizados diretamente no banco

Foi realizada uma consulta direta à tabela de segredos no Supabase.

Resultado observado: a senha original não estava armazenada em texto claro. Foram encontrados somente nonce, criptograma e etiqueta em Base64.

Evidência: `evidencias/teste3-dados-criptografados.png`

## Teste 4 — Registro adulterado

Um caractere do criptograma foi alterado diretamente no banco.

Resultado observado: a API recusou a descriptografia e retornou o código HTTP 500 com a mensagem "registro adulterado".

Evidência: `evidencias/teste4-registro-adulterado.png`

## Teste 5 — Troca de criptogramas

Os campos criptográficos de um segredo foram copiados para outro registro.

Resultado observado: a API recusou a descriptografia porque o AAD não correspondia ao identificador do registro de destino.

Evidência: `evidencias/teste5-copia-realizada.png` e `evidencias/teste5-leitura-recusada`