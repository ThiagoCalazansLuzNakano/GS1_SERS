from datetime import datetime

# Configuração dos limites (Limiares de Decisão)
TEMP_MAX = 60.0  #(superaquecimento) Graus Celsius
TEMP_MIN = 0.0 #(congelamento)
ENERGIA_MIN = 20.0  # Porcentagem de energia
SINAL_MIN = 20.0  # Porcentagem de qualidade de sinal


class MonitorMissaoEspacial:
    def __init__(self):
        self.modo_seguranca = False

    def obter_dados_usuario(self):
        # Solicita que o operador insira os dados manualmente via teclado.
        print("\n📥 [ENTRADA DE DADOS] Digite os valores atuais dos sensores:")

        # Estrutura de repetição para garantir que o usuário digite números válidos
        while True:
            try:
                temperatura = float(input("-> Insira a Temperatura Atual🌡️ (°C): "))
                energia = float(input("-> Insira o Nível de Energia Atual🔋 (%): "))
                comunicacao = float(input("-> Insira a Qualidade do Sinal📡 (%): "))
                break
            except ValueError:
                print("\n❌ Erro: Por favor, insira valores aceitaveis")

        # Define o status dos módulos com base no estado do sistema
        if self.modo_seguranca:
            status_modulos = {"Propulsão": "DESLIGADO (ECO)", "Modo de Segurança": "LIGADO", "Painéis_Solares": "OTIMIZADO"}
        else:
            status_modulos = {"Propulsão": "LIGADO", "Modo de Segurança": "DESLIGADO", "Painéis_Solares": "LIGADO"}

        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "temperatura": temperatura,
            "energia": energia,
            "comunicacao": comunicacao,
            "modulos": status_modulos
        }

    def analisar_e_tomar_decisao(self, dados):
        # Aplica uma tomada de decisão com base nos dados inseridos.
        alertas = []
        acoes = []

        # 1. Verificação da temperatura
        if dados["temperatura"] > TEMP_MAX:
            alertas.append(f"[PERIGO!] Risco de superaquecimento (Crítico para os eletrônicos): {dados['temperatura']}°C!")
            acoes.append("Alterando a orientação da nave para colocar os sistemas na sombra.")
        elif dados["temperatura"] < TEMP_MIN:
            alertas.append(f"[PERIGO!] Risco de congelamento (Crítico para as baterias): {dados['temperatura']}°C!")
            acoes.append("Ativando aquecedores térmicos internos para proteger as baterias.")

        # 2. Verificação da comunicação
        if dados["comunicacao"] < SINAL_MIN:
            alertas.append(f"[ALERTA!] Sinal crítico LOS(Loss of Signal) iminente: {dados['comunicacao']}%")
            acoes.append("Redirecionando todas as antenas para a estação terrestre.")

        # 3. Verificação da energia e sustentabilidade
        if dados["energia"] < ENERGIA_MIN:
            alertas.append(f"[CRÍTICO!] Nível de energia crítica: {dados['energia']}%")
            if not self.modo_seguranca:
                self.modo_seguranca = True
                acoes.append("Protocolo de eco-sustentabilidade ativado automaticamente.")
                acoes.append("Desligando Propulsão e direcionando painéis solares para o Sol.")
        else:
            if self.modo_seguranca and dados["energia"] > 40.0:
                self.modo_seguranca = False
                acoes.append("Energia normalizada. Desativando protocolo de economia.")

        return alertas, acoes

    def exibir_painel(self, dados, alertas, acoes):
        # Exibe o relatório na tela.
        print("\n" + "=" * 60)
        print(f" TELEMETRIA PROCESSADA - HORÁRIO: {dados['timestamp']} ")
        print("=" * 60)
        print(f"|🌡️Temperatura:         {dados['temperatura']}°C")
        print(f"|🔋Status de Energia:   {dados['energia']}% {'[MODO ECONÔMICO]' if self.modo_seguranca else '[NORMAL]'}")
        print(f"|📡Sinal de Comunicação: {dados['comunicacao']}%")
        print("-" * 60)
        print(" STATUS DOS MÓDULOS:")
        for modulo, status in dados["modulos"].items():
            print(f"  - {modulo}: {status}")

        if alertas:
            print("-" * 60)
            print(" 🚨ALERTAS GERADOS🚨:")
            for alerta in alertas:
                print(f"  ⚠️ {alerta}")

        if acoes:
            print("-" * 60)
            print(" DECISÕES AUTOMATIZADAS DO SISTEMA:")
            for acao in acoes:
                print(f"  ⚙️ {acao}")
        print("=" * 60)

    def executar(self):
        # Loop até que o usuário decida sair.
        print("=== Sistema de Monitoramento Energético Interativo Iniciado ===")

        while True:
            dados = self.obter_dados_usuario()
            alertas, acoes = self.analisar_e_tomar_decisao(dados)
            self.exibir_painel(dados, alertas, acoes)

            # Pergunta se o usuário deseja continuar ou parar o monitoramento
            continuar = input(
                "\nDeseja inserir os dados atualizados? (S para sim/Qualquer outra tecla para sair): ").strip().upper()
            if continuar != 'S':
                print("\nEncerrando sistema de monitoramento espacial. Até logo, capitão!")
                break

# Inicialização do Sistema inteligente de monitoramento
if __name__ == "__main__":
    monitor = MonitorMissaoEspacial()
    monitor.executar()