from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth import create_jwt_token, verify_jwt_token, hash_password, verify_password
from database import Base, engine, get_db
from models import UserRegister, UserLogin, UserDB
import httpx

app = FastAPI()

# Cria as tabelas no banco de dados, caso ainda não existam
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Endpoint de registro de usuário
@app.post("/registrar")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email já registrado")
    hashed_password = hash_password(user.senha)
    new_user = UserDB(nome=user.nome, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_jwt_token(user.email, user.nome)
    return {"jwt": token}

# Endpoint de autenticação de usuário
@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if not db_user or not verify_password(user.senha, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = create_jwt_token(user.email, db_user.nome)
    return {"jwt": token}

# Endpoint de aquisição de dados (restrito a usuários autenticados)
@app.get("/consultar")
async def get_data(token: str = Depends(oauth2_scheme)):
    # Verificar o token
    verify_jwt_token(token)

    api_url = "https://api.deezer.com/chart"
    try:
        # Fazer a requisição GET à API Deezer
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Erro ao acessar a API Deezer")

        # Processar a resposta JSON
        data = response.json()
        top_tracks = data["tracks"]["data"][:10]  # Limitar aos 10 primeiros resultados

        # Formatar a resposta com as 10 músicas mais populares
        top_songs = [
            {
                "rank": idx + 1,
                "title": track["title"],
                "artist": track["artist"]["name"],
                "album": track["album"]["title"],
                "preview_url": track["preview"]
            }
            for idx, track in enumerate(top_tracks)
        ]

        return {"top_songs": top_songs}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter músicas: {e}")
