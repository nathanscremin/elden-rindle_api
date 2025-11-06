import requests

url = 'http://127.0.0.1:8000/'
try:
    resposta_status = requests.get(url)
    if resposta_status.status_code == 200:
        print(f'CÓDIGO [{resposta_status.status_code}] - Conexão com o servidor realizada com êxito!')
    elif resposta_status.status_code == 404:
        print(f'CÓDIGO [{resposta_status.status_code}] - Servidor não encontrado no endereço!')
    elif resposta_status.status_code == 500:
        print(f'CÓDIGO [{resposta_status.status_code}] - O servidor não conseguiu processar o pedido inicial!')
    else:
        print(f'CÓDIGO [{resposta_status.status_code}] - Erro desconhecido na conexão.')

except requests.exceptions.ConnectionError:
    print(f'FALHA NA CONEXÃO - Não foi possível conectar ao servidor em {url}')
    print('Verifique o endereço IP, a porta e se o servidor do seu amigo está online.')
    exit()

try:
    start = requests.post(url + "app/game/start")
    start.raise_for_status() 
    game_id = start.json()['game_id']
    print(f'Jogo iniciado! Game ID: {game_id}')
except requests.exceptions.RequestException as e:
    print(f'Erro ao iniciar o jogo: {e}')
    exit()

def mostrar_lista_bosses():
    try:
        response = requests.get(url + "api/bosses/names")
        if response.status_code == 200:
            boss_names = response.json()
            print("\n--- Lista de Bosses de Elden Ring ---")
            for name in boss_names:
                print(f"- {name}")
            print("--------------------------------------\n")
        else:
            print(f'CÓDIGO [{response.status_code}] - Erro ao buscar a lista de bosses.')
    except requests.exceptions.RequestException as e:
        print(f'Erro de conexão ao buscar lista: {e}')

while True:
    print("O que você deseja fazer?")
    print("1 - Fazer um palpite")
    print("2 - Ver a lista de bosses")
    print("S - Sair do jogo")
    
    escolha = input("Digite sua escolha (1, 2 ou S): ").strip().upper()
    print(' ') 

    if escolha == '1':
        # Fazer um palpite
        guess_name = input('Qual boss é esse? ')
        try:
            resposta_nome = requests.post(url + 'api/guess/' + game_id + '/' + guess_name)

            if resposta_nome.status_code == 200:
                resultado = resposta_nome.json()
                acertou = True

                for valor in resultado.values():
                    if valor != 'correct':  
                        acertou = False
                        break

                if acertou:
                    print(' ')
                    print('Parabéns, você ganhou!')
                    print(' ')
                    print("--- Detalhes Finais ---")
                    for chave, valor in resultado.items():
                        print(f'{chave}: {valor}')
                    print("------------------------")
                    break 
                else:
                    print("\n--- Dicas do Palpite ---")
                    texto_formatado = ""
                    for chave, valor in resultado.items():
                        texto_formatado += f'{chave}: {valor}\n'
                    print(texto_formatado.strip())
                    print("--------------------------")

            elif resposta_nome.status_code == 404:
                print(f'CÓDIGO [{resposta_nome.status_code}] - Boss "{guess_name}" não encontrado na base de dados!')
            elif resposta_nome.status_code == 500:
                print(f'CÓDIGO [{resposta_nome.status_code}] - Erro no d servidor ao processar o palpite!')
            else:
                print(f'CÓDIGO [{resposta_nome.status_code}] - Erro desconhecido ao enviar palpite.')
        
        except requests.exceptions.RequestException as e:
            print(f'Erro de conexão ao enviar palpite: {e}')

    elif escolha == '2':
        mostrar_lista_bosses()

    elif escolha == 'S':
        print("Obrigado por jogar!")
        break
    
    else:

        print("Opção inválida. Por favor, digite '1', '2' ou 'S'.")
