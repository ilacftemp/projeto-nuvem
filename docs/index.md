# Documentação do Projeto de Nuvem

#### Criado por Ilana Chaia Finger
#### Link para o DockerHub: [https://hub.docker.com/r/ilacf/app-nuvem](https://hub.docker.com/r/ilacf/app-nuvem)

Este documento fornece uma visão geral do projeto, incluindo a configuração, endpoints da API e todos os requisitos para rodar a aplicação.

## Introdução
Este projeto é uma aplicação web construída com FastAPI, SQLAlchemy, JWT para autenticação e usa uma base de dados MySQL para armazenar os dados de usuários e as senhas criptografadas com hash. Ele permite o registro e login de usuários de maneira segura e consulta (apenas para usuários autenticados) às 10 músicas mais populares do Deezer na data da requisição.

## Configuração
Para configurar o projeto, siga os passos abaixo:

1. Instale a imagem do docker com o seguinte comando: 
```sh
docker pull ilacf/app-nuvem:latest
```

2. Se quiser customizar suas variáveis de ambiente, crie um arquivo `.env` de acordo com o formato no arquivo `.env.example`. 

!!! help "Aviso"
    Sempre tome cuidado com os arquivos `.env` e garanta que ele está no arquivo `.gitignore` antes de publicar seu projeto para não vazar suas credenciais ou dados sensíveis!

3. Acesse o **github** e copie o arquivo `compose.yaml` para sua máquina a partir [desse link](https://github.com/ilacftemp/projeto-nuvem/blob/master/compose.yaml).

4. No mesmo diretório que criou o `compose.yaml`, rode o comando no terminal:
```sh
docker compose up -d
```

5. Agora basta testar os **endpoints** pelo aplicativo `Postman` ou pelo `terminal`, como mostrado em [Usando a API](#usando-a-api).

## Endpoints da API
A API possui os seguintes endpoints:

- **POST /registrar**: Registra um novo usuário.
- **POST /login**: Autentica um usuário e retorna um token JWT.
- **GET /consultar**: Consulta dados protegidos (requer autenticação).

Para mais detalhes, consulte a [documentação dos endpoints](endpoints.md).

## Usando a API

### Registro de usuário:


=== "Linux" 
    ```sh
    curl -X POST http://localhost:8000/registrar -d '{"nome": "seu_nome", "email": "seu_email@mail.com", "senha": "sua_senha"}'
    ```

=== "Windows"
    ```sh
    Invoke-RestMethod -Uri "http://localhost:8000/registrar" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "nome": "seu_nome", "email": "seu_email@mail.com", "senha": "sua_senha" }'
    ```

### Login de usuário:

=== "Linux"

    ```sh
    curl -X POST http://localhost:8000/login -d '{"email": "seu_email@mail.com", "senha": "sua_senha"}'
    ```

=== "Windows"

    ```sh
    Invoke-RestMethod -Uri "http://localhost:8000/login" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{ "email": "seu_email@mail.com", "senha": "sua_senha" }'
    ```

### Consulta das 10 músicas mais populares no Deezer atualmente:

=== "Linux"

    ```sh
    curl -X GET http://localhost:8000/consultar -H 'Authorization: Bearer {token_jwt_aqui}'
    ```

=== "Windows"

    ```sh
    Invoke-RestMethod -Uri "http://localhost:8000/consultar" -Method GET -Headers @{ "Authorization" = "Bearer {token_jwt_aqui}" }
    ```

### Testando a API

Video e fotos da execução e teste da API e dos endpoints [aqui](testando_api.md)

## Autenticação
A autenticação é feita utilizando JWT. O JWT (JSON Web Token) é um padrão compacto e seguro para transmitir informações entre duas partes em formato JSON, comumente usado para autenticação. Ele possui três partes: o cabeçalho (definindo o tipo do token e algoritmo), o payload (contendo as informações do usuário e dados adicionais) e a assinatura, que garante a integridade do token. Na autenticação com JWT, o servidor gera o token após validar as credenciais do usuário, e o cliente o envia nas requisições seguintes para acesso a recursos protegidos.

O uso de JWT oferece várias vantagens, como a possibilidade de uma autenticação sem estado (stateless), facilitando a escalabilidade, além de ser seguro e flexível, permitindo adicionar informações de usuário e expiração diretamente no token. Isso o torna ideal para aplicações distribuídas e APIs, onde a autenticação precisa ser leve e independente de sessões no servidor.

## Banco de Dados
O projeto utiliza um banco de dados MySQL gerado automaticamente pelo docker durante a inicialização.