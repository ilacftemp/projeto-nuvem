from datetime import datetime, timezone, timedelta
import jwt
import hashlib
import hmac
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()
SECRET_KEY = os.getenv("SENHA_SECRETA", "WABADADOO!SENHA_H1PERS_ECRETA!")  # Certifique-se de configurar a chave no .env
ALGORITHM = "HS256"

# Função para criar o token JWT
def create_jwt_token(email: str, name: str) -> str:
    payload = {
        "email": email,
        "name": name,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Expira em 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Função para verificar o token JWT
def verify_jwt_token(token: str):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido ou malformado.")

# Função para hashear a senha
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Função para verificar a senha hasheada
def verify_password(password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed_password)
