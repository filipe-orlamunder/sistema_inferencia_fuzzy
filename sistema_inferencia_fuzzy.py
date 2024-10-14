import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Variáveis de entrada e saída
refeicao = ctrl.Antecedent(np.arange(0, 11, 1), 'refeicao')
servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
tempo = ctrl.Antecedent(np.arange(0, 11, 1), 'tempo')
gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')

# Funções de pertinência para Refeição
refeicao['insossa'] = fuzz.trimf(refeicao.universe, [0, 0, 5])
refeicao['mediana'] = fuzz.trimf(refeicao.universe, [0, 5, 10])
refeicao['saborosa'] = fuzz.trimf(refeicao.universe, [5, 10, 10])

# Funções de pertinência para Serviço
servico['ruim'] = fuzz.trimf(servico.universe, [0, 0, 5])
servico['razoavel'] = fuzz.trimf(servico.universe, [0, 5, 10])
servico['excelente'] = fuzz.trimf(servico.universe, [5, 10, 10])

# Funções de pertinência para Tempo de Atendimento
tempo['demorado'] = fuzz.trimf(tempo.universe, [0, 0, 5])
tempo['mediano'] = fuzz.trimf(tempo.universe, [0, 5, 10])
tempo['rapido'] = fuzz.trimf(tempo.universe, [5, 10, 10])

# Funções de pertinência para Gorjeta
gorjeta['nenhuma'] = fuzz.trimf(gorjeta.universe, [0, 0, 10])
gorjeta['baixa'] = fuzz.trimf(gorjeta.universe, [0, 10, 15])
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [10, 15, 20])
gorjeta['generosa'] = fuzz.trimf(gorjeta.universe, [15, 25, 25])

# Definindo as regras fuzzy
regra1 = ctrl.Rule(refeicao['insossa'] & servico['ruim'], gorjeta['baixa'])
regra2 = ctrl.Rule(refeicao['saborosa'] & servico['excelente'], gorjeta['generosa'])
regra3 = ctrl.Rule(tempo['demorado'], gorjeta['nenhuma'])
regra4 = ctrl.Rule(tempo['mediano'] | tempo['rapido'], gorjeta['media'])

# Sistema de controle (criação)
sistema_gorjeta_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4])
sistema_gorjeta = ctrl.ControlSystemSimulation(sistema_gorjeta_ctrl)

# Fuzzificação: Definindo entradas (podem ser alterados conforme necessidade)
sistema_gorjeta.input['refeicao'] = 6.5  # Exemplo: refeição saborosa
sistema_gorjeta.input['servico'] = 9.0   # Exemplo: serviço excelente
sistema_gorjeta.input['tempo'] = 4.0     # Exemplo: tempo de atendimento mediano

# Calcular a gorjeta com base nas regras
sistema_gorjeta.compute()

# Resultado da defuzzificação
print(f"Gorjeta recomendada: {sistema_gorjeta.output['gorjeta']}%")

# Visualizar o resultado
gorjeta.view(sim=sistema_gorjeta)
plt.show()
