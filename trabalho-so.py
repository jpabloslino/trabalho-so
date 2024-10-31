import time  # Importa o módulo time para capturar tempo real

# Classe que representa um processo
class Processo:
    def __init__(self, estado_atual, prioridade, inicio_memoria, tamanho_mem):
        self.estado_atual = estado_atual  # Estado inicial do processo (ex: "Apto", "Executando", "Bloqueado")
        self.prioridade = prioridade  # Prioridade do processo, utilizado para determinar a ordem de execução
        self.inicio_memoria = inicio_memoria  # Endereço inicial na memória onde o processo será carregado
        self.tamanho_mem = tamanho_mem  # Tamanho da memória ocupada pelo processo
        self.arquivos_abertos = [None] * 20  # Inicializa com 20 posições para arquivos abertos, todos inicialmente como None
        self.tempo_total_cpu = 0  # Tempo total que o processo utilizou a CPU em tempo real
        self.tempo_inicio = None  # Marca o tempo em que o processo começou a usar a CPU
        self.proc_pc = 0  # Contador de programa (PC) para simular a execução do processo
        self.proc_sp = 0  # Registrador de pilha (SP) 
        self.proc_acc = 0  # Registrador acumulador (ACC) 
        self.proc_rx = 0  # Registrador de resultados (RX) 
        self.proximo = None  # Referência para o próximo processo na fila

    def __str__(self):
        # Método que define como o objeto Processo será representado como string
        return (f"Estado: {self.estado_atual}, Prioridade: {self.prioridade}, "
                f"Início Memória: {self.inicio_memoria}, Tamanho Memória: {self.tamanho_mem}, "
                f"Tempo Total CPU (real): {self.tempo_total_cpu:.4f} segundos")

# Inicialização das Estruturas de Controle
MAX_PROCESS = 10  # Número máximo de processos que podem ser gerenciados
tab_desc = [Processo("Apto", i, i * 100, 200) for i in range(MAX_PROCESS)]  # Cria uma lista de processos com estado "Apto"
desc_livre = tab_desc[:]  # Copia inicial dos processos livres para a lista de processos disponíveis
espera_cpu = []  # Fila que armazena processos que estão aguardando para usar a CPU
usando_cpu = None  # Variável que representa o processo que está atualmente usando a CPU
bloqueados = []  # Lista que armazena processos que estão bloqueados

def mostrar_estados():
    # Função que exibe o estado atual dos processos
    print("\n=== Estados dos Processos ===")
    print("Desc Livre:", [str(proc) for proc in desc_livre])  # Exibe processos livres
    print("Espera CPU:", [str(proc) for proc in espera_cpu])  # Exibe processos na fila de espera da CPU
    print("Bloqueados:", [str(proc) for proc in bloqueados])  # Exibe processos bloqueados
    print("Usando CPU:", str(usando_cpu) if usando_cpu else "Nenhum processo usando a CPU")  # Exibe o processo que está usando a CPU, se houver

def adicionar_processo():
    # Função que adiciona um processo à fila de espera da CPU
    for processo in desc_livre:  # Itera sobre os processos disponíveis
        if processo.estado_atual == "Apto":  # Verifica se o processo está "Apto"
            espera_cpu.append(processo)  # Adiciona à fila de espera
            print(f"Processo adicionado à fila de espera de CPU: {processo}")  # Exibe mensagem de adição
            return  # Sai da função após adicionar um processo
    print("Não há processos livres para adicionar.")  # Mensagem se não houver processos disponíveis

def usar_cpu():
    # Função que move um processo da fila de espera para o uso da CPU
    global usando_cpu  # Declara que a variável usando_cpu é global
    if espera_cpu:  # Verifica se há processos na fila de espera
        usando_cpu = espera_cpu.pop(0)  # Remove o primeiro processo da lista de espera
        usando_cpu.estado_atual = "Executando"  # Atualiza o estado para "Executando"
        usando_cpu.tempo_inicio = time.time()  # Registra o tempo de início real
        print(f"Processo movido para usar a CPU: {usando_cpu}")  # Exibe mensagem de mudança de estado
    else:
        print("Não há processos na fila de espera da CPU.")  # Mensagem se não houver processos na fila

def executar_cpu():
    # Função que simula a execução de um processo na CPU
    global usando_cpu  # Declara que a variável usando_cpu é global
    if usando_cpu:  # Verifica se há um processo usando a CPU
        # Simulação do tempo de execução, aqui estamos considerando que a CPU executa por 1 segundo
        time.sleep(1)  # Pausa a execução do programa por 1 segundo para simular o tempo de CPU

        usando_cpu.proc_pc += 1  # Simula a alteração do contador de programa
        
        # Cálculo do tempo real de execução
        tempo_atual = time.time()  # Obtém o tempo atual
        tempo_decorrido = tempo_atual - usando_cpu.tempo_inicio  # Calcula o tempo decorrido em segundos
        usando_cpu.tempo_total_cpu += tempo_decorrido  # Adiciona o tempo decorrido ao tempo total da CPU
        usando_cpu.tempo_inicio = tempo_atual  # Atualiza o tempo de início para o próximo ciclo
        
        print(f"Processo ainda executando (tempo real): {usando_cpu.tempo_total_cpu:.4f} segundos.")  # Exibe o tempo total de execução
    else:
        print("Nenhum processo está usando a CPU no momento.")  # Mensagem se nenhum processo está em execução

def bloquear_processo():
    # Função que bloqueia o processo atual que está usando a CPU
    global usando_cpu  # Declara que a variável usando_cpu é global
    if usando_cpu:  # Verifica se há um processo usando a CPU
        usando_cpu.estado_atual = "Bloqueado"  # Atualiza o estado para "Bloqueado"
        bloqueados.append(usando_cpu)  # Adiciona o processo à lista de bloqueados
        print(f"Processo bloqueado: {usando_cpu}")  # Exibe mensagem de bloqueio
        usando_cpu = None  # Limpa a variável usando_cpu
    else:
        print("Não há processos usando a CPU.")  # Mensagem se nenhum processo está em execução

def desbloquear_processo():
    # Função que desbloqueia o primeiro processo bloqueado e o move para a fila de espera
    if bloqueados:  # Verifica se há processos bloqueados
        processo = bloqueados.pop(0)  # Remove o primeiro processo da lista de bloqueados
        processo.estado_atual = "Apto"  # Ao desbloquear, o estado volta para "Apto"
        espera_cpu.append(processo)  # Adiciona à fila de espera
        print(f"Processo desbloqueado e movido para a fila de espera: {processo}")  # Exibe mensagem de desbloqueio
    else:
        print("Não há processos bloqueados para desbloquear.")  # Mensagem se não houver processos bloqueados

def criar_processo(novo_id):
    # Função para criar um novo processo
    return Processo("Apto", novo_id, novo_id * 100, 200)  # Cria um novo processo com estado "Apto"

def remover_processo():
    # Função que permite ao usuário remover um processo da lista de processos livres
    print("=== Lista de Processos ===")
    for i, processo in enumerate(desc_livre):  # Itera sobre a lista de processos livres
        print(f"{i + 1}. {processo}")  # Exibe cada processo com seu índice
    
    escolha = int(input("Escolha o número do processo que deseja remover (0 para cancelar): ")) - 1  # Captura a escolha do usuário
    if 0 <= escolha < len(desc_livre):  # Verifica se a escolha é válida
        processo_remover = desc_livre[escolha]  # Seleciona o processo a ser removido
        desc_livre.remove(processo_remover)  # Remove o processo da lista de processos livres
        print(f"Processo removido: {processo_remover}")  # Exibe mensagem de remoção

        # Cria um novo processo para manter o total de processos
        novo_id = len(desc_livre)  # Gera um novo ID baseado na quantidade atual de processos
        novo_processo = criar_processo(novo_id)  # Cria um novo processo
        desc_livre.append(novo_processo)  # Adiciona o novo processo à lista de processos livres
        print(f"Novo processo criado: {novo_processo}")  # Exibe mensagem sobre o novo processo
    else:
        print("Escolha inválida ou operação cancelada.")  # Mensagem se a escolha for inválida

def menu():
    # Função que exibe o menu de opções para o usuário e processa suas escolhas
    while True:
        print("\n=== Menu de Controle de Processos ===")
        print("1. Adicionar Processo")  # Opção para adicionar um processo
        print("2. Usar CPU")  # Opção para usar a CPU com um processo
        print("3. Executar CPU (Tempo real de execução)")  # Opção para executar o processo na CPU
        print("4. Bloquear Processo")  # Opção para bloquear o processo atual
        print("5. Desbloquear Processo")  # Opção para desbloquear um processo bloqueado
        print("6. Mostrar Estados")  # Opção para mostrar os estados dos processos
        print("7. Remover Processo")  # Opção para remover um processo
        print("0. Sair")  # Opção para sair do programa
        opcao = input("Escolha uma opção: ")  # Captura a opção escolhida pelo usuário

        # Chama a função correspondente com base na escolha do usuário
        if opcao == '1':
            adicionar_processo()  # Adiciona um processo
        elif opcao == '2':
            usar_cpu()  # Move um processo para usar a CPU
        elif opcao == '3':
            executar_cpu()  # Executa o processo que está usando a CPU
        elif opcao == '4':
            bloquear_processo()  # Bloqueia o processo atual
        elif opcao == '5':
            desbloquear_processo()  # Desbloqueia um processo bloqueado
        elif opcao == '6':
            mostrar_estados()  # Mostra os estados dos processos
        elif opcao == '7':
            remover_processo()  # Remove um processo da lista
        elif opcao == '0':
            print("Saindo...")  # Mensagem de saída
            break  # Sai do loop
        else:
            print("Opção inválida. Tente novamente.")  # Mensagem se a opção for inválida

# Iniciar o programa chamando o menu
menu()
