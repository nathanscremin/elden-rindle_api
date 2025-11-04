# Eldendle API

**Eldendle API — Servidor (backend)**  
Repositório do servidor backend do projeto *Eldendle* — um jogo no estilo *Wordle* focado no universo de **Elden Ring**.  
Projeto do Terceiro Mini Projeto da disciplina de Programação de Scripts (Fatec Rio Claro). O servidor foi implementado em **Python** com **FastAPI** e expõe endpoints prontos para consumo por um frontend.

---

## 🚀 Como rodar o servidor (local)

1. **Clone o repositório**
```bash
git clone https://github.com/nathanscremin/eldendle_api.git
cd eldendle_api
```

2. **Crie e ative um ambiente virtual (recomendado)**
```bash
# Cria o ambiente virtual na pasta .venv
python -m venv .venv

# Ativa o ambiente (Windows)
.\.venv\Scripts\activate

# Ativa o ambiente (Linux / macOS)
# source .venv/bin/activate
```

3. **Instale as dependências**
```bash
cd server
pip install -r requirements.txt
```

4. **Inicie o servidor**
```bash
uvicorn app.main:app --reload
```
- `app.main` refere-se ao arquivo `main.py` dentro da pasta `app`.  
- `:app` é o objeto `app = FastAPI()` no arquivo.  
- `--reload` reinicia o servidor automaticamente a cada alteração no código.

> O servidor ficará disponível em: `http://127.0.0.1:8000`

---

## 📚 Documentação interativa (Swagger)
Com o servidor em execução, acesse a documentação automática do FastAPI:
- `http://127.0.0.1:8000/docs`

Lá você pode testar todos os endpoints via interface web.

---

## 🗺️ Endpoints principais

### 🎮 Jogo (sessão)
#### `POST /api/game/start`
Inicia uma nova sessão de jogo. O servidor sorteia um boss aleatório e retorna o `game_id`.

**Resposta (exemplo)**:
```json
{
  "game_id": "seu-uuid-unico-aqui"
}
```

#### `POST /api/guess/{game_id}/{guess_name}`
Submete um palpite (`guess_name`) para uma sessão específica (`game_id`). Retorna o feedback comparando atributos do palpite com a resposta correta.

**Resposta (exemplo)**:
```json
{
  "nome": "incorrect",
  "regiao": "partial",
  "fase": "higher",
  "tipo": "correct",
  "raca": "incorrect",
  "localizacao_especifica": "incorrect",
  "drop_principal": "incorrect",
  "obrigatorio": "correct",
  "runes": "lower"
}
```

**Legenda do feedback**
- `correct`: acerto exato  
- `incorrect`: erro total  
- `partial`: parcialmente correto (ex.: acertou a região, mas errou a localização específica)  
- `higher`: o valor correto é maior que o palpite (usado para `fase` e `runes`)  
- `lower`: o valor correto é menor que o palpite

---

## 📊 Dados (Bosses)

### `GET /api/bosses/names`
Retorna uma lista simples com os nomes (strings) de todos os bosses disponíveis. Ideal para popular um autocomplete ou menu de seleção no cliente.

**Resposta (exemplo)**:
```json
[
  "Godrick the Grafted",
  "Rennala, Queen of the Full Moon",
  "Starscourge Radahn",
  "..."
]
```

### `GET /api/boss/details/{boss_name}`
Retorna o objeto completo com todos os dados do boss solicitado. O cliente pode usar este endpoint após cada palpite para exibir imagem e detalhes do boss.

**Resposta (exemplo)**:
```json
{
  "nome": "Godrick the Grafted",
  "regiao": "Limgrave",
  "fase": 2,
  "tipo": "Demigod",
  "raca": "Humanoid",
  "localizacao_especifica": "Stormveil Castle",
  "drop_principal": "Godrick's Great Rune",
  "obrigatorio": true,
  "runes": 20000,
  "imagem_url": "https://eldenring.wiki.fextralife.com/..."
}
```

---

## ✅ Observações práticas
- Garanta que o `requirements.txt` contenha `fastapi`, `uvicorn`, e quaisquer bibliotecas auxiliares usadas pelo projeto.  
- Para produção, remova `--reload` e use um gerenciador de processos (systemd, gunicorn/uvicorn workers, containerização, etc.).  
- Se for expor imagens externas, valide e normalize as `imagem_url` para evitar hotlinking ou problemas de CORS no frontend.

---

Se quiser, posso:
- adicionar um `README` mais enxuto com badges e links;  
- gerar um `docker-compose.yml` básico para rodar a API;  
- ou aplicar ajustes específicos no conteúdo (ex.: padronizar termos, traduzir campos).  
