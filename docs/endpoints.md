# Endpoints da API

## POST /registrar
Registra um novo usuário.

### Request
```json
{
    "nome": "string",
    "email": "string",
    "senha": "string"
}
```

### Reponse

```json
{
    "jwt": "string"
}
```

## POST /login
Autentica um usuário e retorna um token JWT.

### Request
```json
{
    "email": "string",
    "senha": "string"
}
```

### Response
```json
{
    "jwt": "string"
}
```


## GET /consultar
Consulta dados protegidos (requer autenticação).

### Request
Authorization: Bearer <token>

### Response
```json
{
    "top_songs": [
        {
            "rank": 1,
            "title": "string",
            "artist": "string",
            "album": "string",
            "preview_url": "string"
        },
        ...
    ]
}
```