# Cofre de Senhas Corporativo com AES-GCM

API desenvolvida para armazenar credenciais de forma criptografada, utilizando AES-256 no modo GCM e derivação de chave com PBKDF2.

Este projeto foi desenvolvido como atividade da disciplina de Criptografia Aplicada da Pontifícia Universidade Católica de Goiás.

## Autor

* Guilherme Gomes Candini

## Objetivo

O objetivo do projeto é desenvolver uma API de cofre de senhas corporativo capaz de armazentschonar credenciais em um banco de dados PostgreSQL sem salvar as senhas em texto claro.

Mesmo que alguém consiga consultar ou copiar o banco de dados, encontrará apenas os dados criptografados. Para recuperar uma senha, é necessário conhecer a senha-mestra do cofre.

O projeto utiliza:

* AES-256 no modo GCM para cifrar as senhas;
* PBKDF2 com HMAC-SHA-256 para derivar a chave;
* nonce aleatório para cada operação de cifragem;
* etiqueta de autenticação para detectar adulterações;
* AAD para vincular o criptograma ao cofre e ao segredo correspondente.

## Tecnologias utilizadas

* Python 3.10 ou superior;
* FastAPI;
* Uvicorn;
* PyCryptodome;
* Supabase;
* PostgreSQL;
* Python Dotenv;
* Git e GitHub.

## Estrutura do projeto

```text
cofre-aes/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── cripto.py
│   ├── banco.py
│   └── modelos.py
├── sql/
│   └── esquema.sql
├── testes/
│   ├── resultados.md
│   └── evidencias/
├── .env.exemplo
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidade dos arquivos

* `app/cripto.py`: derivação da chave, cifragem, decifragem e verificação criptográfica.
* `app/banco.py`: comunicação com o banco de dados do Supabase.
* `app/modelos.py`: modelos de dados recebidos pela API.
* `app/main.py`: rotas, códigos HTTP e integração entre as camadas.
* `sql/esquema.sql`: criação das tabelas e políticas de acesso.
* `testes/resultados.md`: descrição dos cinco testes obrigatórios.
* `testes/evidencias`: capturas de tela dos testes.
* `.env.exemplo`: exemplo das variáveis necessárias para conexão.
* `.gitignore`: impede o envio de arquivos sigilosos.
* `requirements.txt`: lista das dependências do projeto.

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.10 ou superior;
* Git;
* uma conta no Supabase;
* um editor de código, como o Visual Studio Code.

Para verificar a versão do Python:

```bash
python --version
```

No Windows, também pode ser utilizado:

```bash
py --version
```

## Instalação

### 1. Baixar o projeto

Clone o repositório:

```bash
git clone https://github.com/GuiCandini/cofre-aes
```

Entre na pasta:

```bash
cd cofre-aes
```

Caso o projeto tenha sido baixado como arquivo ZIP, extraia o conteúdo e abra o terminal dentro da pasta `cofre-aes`.

### 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Caso o comando `python` não seja reconhecido:

```powershell
py -m venv .venv
```

No Linux ou macOS:

```bash
python3 -m venv .venv
```

### 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois tente novamente:

```powershell
.venv\Scripts\Activate.ps1
```

No Prompt de Comando do Windows:

```cmd
.venv\Scripts\activate.bat
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Após a ativação, o terminal deverá apresentar `(.venv)` no início da linha.

### 4. Instalar as dependências

Com o ambiente virtual ativo, execute:

```bash
python -m pip install --upgrade pip
```

Depois instale as dependências:

```bash
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` ainda não tenha sido gerado, utilize:

```bash
pip install fastapi "uvicorn[standard]" pycryptodome supabase python-dotenv
```

Em seguida, gere o arquivo:

```bash
pip freeze > requirements.txt
```

## Configuração do Supabase

### 1. Criar um projeto

Acesse o site do Supabase e crie um projeto.

Durante a criação:

1. Informe um nome para o projeto.
2. Defina uma senha para o banco PostgreSQL.
3. Escolha uma região próxima.
4. Aguarde a conclusão da criação.

A senha do banco PostgreSQL não é a senha-mestra utilizada pelo cofre.

### 2. Criar as tabelas

No painel do Supabase:

1. Acesse `SQL Editor`.
2. Clique em `New query`.
3. Copie o conteúdo do arquivo `sql/esquema.sql`.
4. Cole no editor.
5. Clique em `Run`.

O script cria as tabelas:

* `cofres`;
* `segredos`.

Também são criadas as políticas de acesso necessárias para a realização do projeto acadêmico.

### 3. Obter as credenciais da API

No painel do Supabase, procure a área de configurações da API e copie:

* URL do projeto;
* chave pública, chamada de `publishable key` ou `anon key`.

### 4. Criar o arquivo de configuração

Na raiz do projeto, crie um arquivo chamado `.env`.

Coloque:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica
```

Substitua os valores pelas informações do seu projeto Supabase.

Não utilize aspas e não coloque espaços antes ou depois do sinal de igualdade.

O arquivo `.env` contém informações de conexão e não deve ser enviado ao GitHub.

O arquivo `.env.exemplo` deve conter apenas valores fictícios:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica
```

## Executar a aplicação

Entre na pasta principal do projeto:

```bash
cd cofre-aes
```

Ative o ambiente virtual.

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa do FastAPI ficará disponível em:

```text
http://127.0.0.1:8000/docs
```

Na página `/docs`, é possível testar todas as rotas com o botão `Try it out`.

Para parar a aplicação, pressione `Ctrl + C` no terminal.

## Utilização da senha-mestra

Na criação do cofre, a senha-mestra é enviada no corpo da requisição.

Nas demais rotas, ela deve ser enviada no seguinte cabeçalho HTTP:

```text
X-Senha-Mestra
```

A senha-mestra não é armazenada no banco de dados.

A cada requisição, ela é utilizada junto com o sal e o número de iterações do cofre para derivar temporariamente a chave criptográfica.

## Rotas da API

| Método   | Rota                                       | Descrição                          |
| -------- | ------------------------------------------ | ---------------------------------- |
| `GET`    | `/`                                        | Verifica se a API está funcionando |
| `POST`   | `/cofres`                                  | Cria um novo cofre                 |
| `POST`   | `/cofres/{cofre_id}/abrir`                 | Verifica a senha-mestra            |
| `POST`   | `/cofres/{cofre_id}/segredos`              | Cadastra e cifra uma credencial    |
| `GET`    | `/cofres/{cofre_id}/segredos`              | Lista os metadados das credenciais |
| `GET`    | `/cofres/{cofre_id}/segredos/{segredo_id}` | Decifra e devolve uma credencial   |
| `PUT`    | `/cofres/{cofre_id}/segredos/{segredo_id}` | Atualiza uma credencial            |
| `DELETE` | `/cofres/{cofre_id}/segredos/{segredo_id}` | Exclui uma credencial              |

## Códigos HTTP utilizados

| Código | Significado                                                 |
| ------ | ----------------------------------------------------------- |
| `200`  | Operação realizada com sucesso                              |
| `201`  | Cofre ou segredo criado                                     |
| `401`  | Senha-mestra incorreta                                      |
| `404`  | Cofre ou segredo não encontrado                             |
| `422`  | Dados enviados em formato inválido                          |
| `500`  | Registro adulterado ou falha na autenticação do criptograma |

## Exemplos de utilização

### Criar um cofre

Rota:

```text
POST /cofres
```

Corpo da requisição:

```json
{
  "nome": "Cofre de Testes",
  "senha_mestra": "MinhaSenhaMestre@2026"
}
```

Resposta esperada:

```json
{
  "mensagem": "cofre criado com sucesso",
  "cofre_id": "UUID-GERADO-PELA-API"
}
```

O identificador retornado deve ser guardado para acessar o cofre nas próximas rotas.

### Verificar a senha-mestra

Rota:

```text
POST /cofres/{cofre_id}/abrir
```

Cabeçalho:

```text
X-Senha-Mestra: MinhaSenhaMestre@2026
```

Resposta esperada:

```json
{
  "mensagem": "senha-mestra correta"
}
```

### Cadastrar uma credencial

Rota:

```text
POST /cofres/{cofre_id}/segredos
```

Cabeçalho:

```text
X-Senha-Mestra: MinhaSenhaMestre@2026
```

Corpo:

```json
{
  "titulo": "Banco de dados",
  "usuario": "administrador",
  "url": "https://sistema.exemplo.com.br",
  "senha": "SenhaDoSistema@123"
}
```

Resposta esperada:

```json
{
  "mensagem": "segredo criado com sucesso",
  "segredo_id": "UUID-GERADO-PELA-API"
}
```

### Listar as credenciais

Rota:

```text
GET /cofres/{cofre_id}/segredos
```

A listagem apresenta somente:

* identificador;
* título;
* usuário;
* URL;
* datas de criação e atualização.

A listagem não apresenta:

* senha em texto claro;
* nonce;
* criptograma;
* etiqueta de autenticação.

### Consultar uma credencial

Rota:

```text
GET /cofres/{cofre_id}/segredos/{segredo_id}
```

Cabeçalho:

```text
X-Senha-Mestra: MinhaSenhaMestre@2026
```

Resposta esperada:

```json
{
  "id": "UUID-DO-SEGREDO",
  "titulo": "Banco de dados",
  "usuario": "administrador",
  "url": "https://sistema.exemplo.com.br",
  "senha": "SenhaDoSistema@123"
}
```

### Atualizar uma credencial

Rota:

```text
PUT /cofres/{cofre_id}/segredos/{segredo_id}
```

Corpo:

```json
{
  "titulo": "Banco de dados atualizado",
  "usuario": "administrador",
  "url": "https://sistema.exemplo.com.br",
  "senha": "NovaSenha@2026"
}
```

Durante a atualização, um novo nonce aleatório é gerado.

### Excluir uma credencial

Rota:

```text
DELETE /cofres/{cofre_id}/segredos/{segredo_id}
```

A API verifica a senha-mestra e remove o registro informado.

## Parâmetros criptográficos

O projeto utiliza os seguintes parâmetros:

| Parâmetro                | Valor                |
| ------------------------ | -------------------- |
| Algoritmo                | AES                  |
| Tamanho da chave         | 256 bits ou 32 bytes |
| Modo de operação         | GCM                  |
| Função de derivação      | PBKDF2               |
| Função interna do PBKDF2 | HMAC-SHA-256         |
| Iterações                | 210.000              |
| Tamanho do sal           | 16 bytes             |
| Tamanho do nonce         | 12 bytes             |
| Tamanho da etiqueta      | 16 bytes             |

## Justificativa dos parâmetros criptográficos

### PBKDF2

Uma senha criada por uma pessoa não possui o tamanho nem a aleatoriedade exigidos por uma chave AES-256.

O PBKDF2 recebe a senha-mestra, um sal aleatório e uma quantidade de iterações. O resultado é uma chave de 32 bytes adequada para utilização pelo AES-256.

O projeto utiliza 210.000 iterações para tornar cada tentativa de derivação mais lenta. Para o usuário legítimo, esse tempo ocorre apenas durante as requisições. Para um atacante, o mesmo custo seria aplicado em cada tentativa de descoberta da senha-mestra.

### Sal

Cada cofre recebe um sal aleatório de 16 bytes.

O sal não precisa ser secreto e pode ser armazenado no banco. Sua função é impedir que cofres com a mesma senha-mestra produzam exatamente a mesma chave.

### AES-GCM

O modo GCM fornece confidencialidade e integridade.

A confidencialidade impede que a senha seja lida diretamente no banco. A integridade permite detectar alterações realizadas no criptograma.

Cada operação de cifragem gera:

* nonce;
* criptograma;
* etiqueta de autenticação.

### Nonce

O nonce possui 12 bytes e é gerado aleatoriamente em cada operação.

Mesmo que a mesma senha seja cadastrada duas vezes, os nonces e os criptogramas serão diferentes.

Ao atualizar uma senha, o sistema também gera um novo nonce.

Um nonce não deve ser reutilizado com a mesma chave.

### Etiqueta de autenticação

A etiqueta é gerada pelo AES-GCM durante a cifragem.

Durante a decifragem, a biblioteca verifica a etiqueta antes de devolver o texto claro. Se o criptograma tiver sido alterado, a operação gera um `ValueError`, tratado pela API como registro adulterado.

### AAD

O AAD corresponde aos dados associados autenticados. Ele não é cifrado, mas participa do cálculo da etiqueta.

Para cada segredo, o projeto utiliza:

```text
cofre_id|segredo_id
```

Isso vincula o criptograma ao cofre e ao registro original.

Caso alguém copie o criptograma de uma credencial para outro registro, a API utilizará um AAD diferente e recusará a decifragem.

## Informações armazenadas

O banco de dados armazena:

* identificador do cofre;
* nome do cofre;
* sal;
* número de iterações;
* verificador criptográfico;
* identificador do segredo;
* título;
* usuário;
* URL;
* nonce;
* criptograma;
* etiqueta;
* datas de criação e atualização.

## Informações que não são armazenadas

O sistema não armazena:

* senha-mestra;
* chave derivada;
* senhas em texto claro;
* histórico das senhas digitadas.

A senha-mestra e a chave derivada existem apenas durante o processamento da requisição.

## Verificador do cofre

Durante a criação do cofre, a aplicação cifra a frase fixa:

```text
cofre-ok
```

Nas requisições seguintes, a chave derivada é utilizada para tentar decifrar esse verificador.

Se a decifragem falhar, a senha-mestra está incorreta e a API retorna:

```text
401 Unauthorized
```

Se o verificador funcionar, mas um segredo específico falhar, a senha-mestra está correta e o registro foi adulterado. Nesse caso, a API retorna:

```text
500 Internal Server Error
```

## Testes realizados

### Teste 1 — Nonces distintos

A mesma senha foi cadastrada duas vezes no mesmo cofre, utilizando títulos diferentes.

Resultado esperado:

* nonces diferentes;
* criptogramas diferentes;
* senhas originais iguais.

Esse teste demonstra que o sistema gera um nonce aleatório para cada cifragem.

### Teste 2 — Senha-mestra incorreta

Foi realizada uma tentativa de leitura utilizando uma senha-mestra incorreta.

Resultado esperado:

```text
401 Unauthorized
```

Nenhum conteúdo do segredo deve ser devolvido.

### Teste 3 — Consulta direta ao banco

Foi realizada uma consulta direta à tabela `segredos`:

```sql
select
    titulo,
    usuario,
    nonce,
    criptograma,
    etiqueta
from public.segredos;
```

Resultado esperado:

* nenhuma senha legível;
* apenas valores criptográficos em Base64.

### Teste 4 — Registro adulterado

Um caractere do campo `criptograma` foi alterado diretamente no banco de dados.

Após a alteração, foi realizada uma tentativa de leitura pela API utilizando a senha-mestra correta.

Resultado esperado:

```text
500 Internal Server Error
```

Resposta:

```json
{
  "detail": "registro adulterado"
}
```

Esse teste demonstra que a etiqueta do AES-GCM detecta modificações no criptograma.

### Teste 5 — Troca de criptogramas

Os campos `nonce`, `criptograma` e `etiqueta` de um segredo foram copiados para outro registro do mesmo cofre.

Mesmo utilizando a senha-mestra correta, a leitura do registro de destino foi recusada.

Resultado esperado:

```text
500 Internal Server Error
```

Esse teste demonstra que o AAD vincula o criptograma ao seu registro original.

As descrições completas dos resultados estão no arquivo:

```text
testes/resultados.md
```

As capturas de tela estão na pasta:

```text
testes/evidencias/
```

## Modelo de ameaças

O cofre oferece proteção nas seguintes situações:

* cópia integral do banco por uma pessoa não autorizada;
* consulta SQL direta às tabelas;
* alteração do criptograma;
* troca de dados criptográficos entre registros.

O projeto não protege contra:

* comprometimento do servidor durante a execução;
* descoberta ou divulgação da senha-mestra;
* utilização de uma senha-mestra fraca;
* acesso ao computador enquanto a aplicação está sendo utilizada;
* ausência de controle individual de usuários.

## Limitações

Este sistema foi desenvolvido para fins acadêmicos e não deve ser utilizado diretamente em produção.

As principais limitações são:

* não existe autenticação individual de usuários;
* não existe autorização por usuário ou grupo;
* não existe auditoria de acessos;
* não existe registro de quem consultou cada senha;
* não existe bloqueio após várias tentativas incorretas;
* não existe troca automática da senha-mestra;
* a senha-mestra passa pela memória do servidor durante a requisição;
* título, usuário e URL permanecem armazenados em texto claro;
* as políticas do Supabase foram abertas para permitir os testes acadêmicos;
* a segurança do cofre depende da utilização de uma senha-mestra forte.

## Cuidados de segurança

É proibido armazenar ou publicar:

* arquivo `.env`;
* senha-mestra;
* chave derivada;
* senhas em texto claro;
* chaves fixas no código;
* nonces fixos;
* sais fixos.

Também não devem ser utilizados `print()` ou arquivos de log para registrar senhas, chaves ou senhas-mestras.

O arquivo `.gitignore` deve conter:

```gitignore
.venv/
.env
__pycache__/
*.pyc
.vscode/
```

Antes de enviar o projeto ao GitHub, deve ser executado:

```bash
git status
```

O arquivo `.env` não pode aparecer na lista de arquivos versionados.

## Envio ao GitHub

Na pasta principal do projeto, execute:

```bash
git init
git add .
git status
git commit -m "Cofre de senhas com AES-GCM"
git branch -M main
git remote add origin URL_DO_REPOSITORIO
git push -u origin main
```

Antes do `git commit`, é obrigatório conferir o resultado de `git status`.

Se o `.env` aparecer, não realize o envio. Confira o `.gitignore` e remova o arquivo da área de preparação:

```bash
git rm --cached .env
```

Depois verifique novamente:

```bash
git status
```

## Estado do projeto

O projeto implementa:

* criação de cofres;
* verificação da senha-mestra;
* cadastro de credenciais;
* listagem de metadados;
* consulta e decifragem de credenciais;
* atualização com geração de novo nonce;
* exclusão de credenciais;
* detecção de registros adulterados;
* proteção contra troca de criptogramas entre registros.
