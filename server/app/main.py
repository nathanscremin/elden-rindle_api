import random
import uuid
from fastapi import FastAPI, HTTPException
from typing import List

from .database import BOSS_DATABASE
from .models import Boss, GuessFeedback, FeedbackStatus

# Inicialização do FastAPI
app = FastAPI()

ACTIVE_GAMES: Dict[str, Boss] = {}

def get_new_random_boss() -> Boss:
    all_boss_names = list(BOSS_DATABASE.keys())
    random_boss_name = random.choice(all_boss_names)
    
    print(f"--- Novo jogo criado. Resposta: {random_boss_name} ---")
    
    return Boss(**BOSS_DATABASE[random_boss_name])

@app.get("/")
def read_root():
    return{"Projeto" : "Eldendle API"}

@app.get("/api/bosses/names", response_model=List[str])
def get_all_boss_names():
    # Endpoint para os palpites.
    return list(BOSS_DATABASE.keys())

@app.get("/api/boss/details/{boss_name}", response_model=Boss)
def get_boss_details(boss_name: str):
    # Endpoint para o cliente pegar os dados do boss
    if boss_name not in BOSS_DATABASE:
        raise HTTPException(status_code=404, detail="Boss não encontrado.")
    return BOSS_DATABASE[boss_name]
    
@app.post("/app/game/start")
def start_new_game():
    game_id = str(uuid.uuid4())
    
    correct_boss = get_new_random_boss()
    
    ACTIVE_GAMES[game_id] = correct_boss
    
    return {"game_id": game_id}

@app.post("/api/guess/{guess_name}", response_model=GuessFeedback)
def process_guess(game_id: str, guess_name: str):
    # Endpoint principal, o cliente envia o nome e o servidor compara com o BOSS_DO_DIA
    
    correct_boss_data = ACTIVE_GAMES.get(game_id)
    
    if not correct_boss_data:
        raise HTTPException(status_code=404, detail="Sessão de jogo não encontrada. Inicie um novo jogo.")
    
    if guess_name not in BOSS_DATABASE:
        raise HTTPException(status_code=404, detail="Boss (palpite) não encontrado")
    
    guess_data = Boss(**BOSS_DATABASE[guess_name])
    feedback = {}
    
    feedback["nome"] = "correct" if guess_data.nome == BOSS_DO_DIA_DADOS.nome else "incorrect"
    feedback["regiao"] = "correct" if guess_data.regiao == BOSS_DO_DIA_DADOS.regiao else "incorrect"
    feedback["tipo"] = "correct" if guess_data.tipo == BOSS_DO_DIA_DADOS.tipo else "incorrect"
    feedback["raca"] = "correct" if guess_data.raca == BOSS_DO_DIA_DADOS.raca else "incorrect"
    feedback["localizacao_especifica"] = "correct" if guess_data.localizacao_especifica == BOSS_DO_DIA_DADOS.localizacao_especifica else "incorrect"
    feedback["drop_principal"] = "correct" if guess_data.drop_principal == BOSS_DO_DIA_DADOS.drop_principal else "incorrect"
    feedback["obrigatorio"] = "correct" if guess_data.obrigatorio == BOSS_DO_DIA_DADOS.obrigatorio else "incorrect"
    
    # Lógica "Maior / Menor" para Fases
    if guess_data.fase == BOSS_DO_DIA_DADOS.fase:
        feedback["fase"] = "correct"
    elif guess_data.fase < BOSS_DO_DIA_DADOS.fase:
        feedback["fase"] = "higher" # Significa que a resposta correta tem MAIS fases
    else:
        feedback["fase"] = "lower"  # Significa que a resposta correta tem MENOS fases

    # Lógica "Maior / Menor" para Runas
    if guess_data.runes == BOSS_DO_DIA_DADOS.runes:
        feedback["runes"] = "correct"
    elif guess_data.runes < BOSS_DO_DIA_DADOS.runes:
        feedback["runes"] = "higher" # Significa que a resposta correta dropa MAIS runas
    else:
        feedback["runes"] = "lower"  # Significa que a resposta correta dropa MENOS runas
    
    # 4. Retorna o feedback para o cliente
    return GuessFeedback(**feedback)