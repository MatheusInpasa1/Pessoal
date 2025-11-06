import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class CalculadoraProposta:
    def __init__(self):
        self.fatores = {}
        self.resultados = {}
        
    def coletar_dados_atual(self):
        """Coleta informações sobre a situação atual"""
        print("=== SITUAÇÃO ATUAL ===")
        
        self.fatores['salario_atual'] = float(input("Salário atual bruto mensal: R$ "))
        self.fatores['beneficios_atual'] = float(input("Valor dos benefícios (VR, VT, plano saúde, etc.) mensal: R$ "))
        self.fatores['bonus_atual'] = float(input("Bônus/PLR anual (em R$): R$ "))
        self.fatores['ferias_atual'] = float(input("Dias de férias atuais: "))
        self.fatores['home_office_atual'] = int(input("Dias de home office por semana (0-5): "))
        self.fatores['tempo_viagem_atual'] = float(input("Tempo de deslocamento diário (horas): "))
        
    def coletar_expectativas(self):
        """Coleta expectativas e informações da nova empresa"""
        print("\n=== EXPECTATIVAS E NOVA EMPRESA ===")
        
        self.fatores['custo_vida_nova'] = float(input("Aumento percentual no custo de vida na nova localização (%): ")) / 100
        self.fatores['dias_presencial_novo'] = int(input("Dias de trabalho presencial na nova empresa (por semana): "))
        self.fatores['tempo_viagem_novo'] = float(input("Tempo de deslocamento novo (horas/dia): "))
        self.fatores['custo_transporte_novo'] = float(input("Custo mensal estimado de transporte: R$ "))
        
        # Fatores qualitativos
        print("\nAvalie os seguintes fatores (1-10):")
        self.fatores['crescimento_carreira'] = int(input("Potencial de crescimento na nova empresa: "))
        self.fatores['estabilidade'] = int(input("Estabilidade da nova empresa: "))
        self.fatores['beneficios_qualidade'] = int(input("Qualidade dos benefícios: "))
        
    def calcular_valor_hora_atual(self):
        """Calcula o valor real por hora considerando tempo de deslocamento"""
        salario_mensal = self.fatores['salario_atual']
        horas_trabalho = 8 * 22  # 8 horas/dia, 22 dias/mês
        horas_deslocamento = self.fatores['tempo_viagem_atual'] * 2 * 22  # Ida e volta
        
        horas_totais = horas_trabalho + horas_deslocamento
        return (salario_mensal + self.fatores['beneficios_atual']) / horas_totais
    
    def calcular_compensacao_minima(self):
        """Calcula a compensação mínima aceitável"""
        # Salário atual total anual
        salario_anual_atual = (self.fatores['salario_atual'] + self.fatores['beneficios_atual']) * 13
        salario_anual_atual += self.fatores['bonus_atual']
        
        # Ajuste pelo custo de vida
        salario_ajustado = salario_anual_atual * (1 + self.fatores['custo_vida_nova'])
        
        # Ajuste por qualidade de vida (tempo de deslocamento)
        tempo_viagem_atual = self.fatores['tempo_viagem_atual'] * 2 * 22 * 12
        tempo_viagem_novo = self.fatores['tempo_viagem_novo'] * 2 * self.fatores['dias_presencial_novo'] * 4.33 * 12
        
        diferenca_tempo = tempo_viagem_atual - tempo_viagem_novo
        # Valor do tempo: considerando R$ 50/hora (valor subjetivo do tempo livre)
        valor_tempo = diferenca_tempo * 50
        
        compensacao_minima_anual = salario_ajustado - valor_tempo
        compensacao_minima_mensal = compensacao_minima_anual / 13
        
        return compensacao_minima_mensal
    
    def calcular_valor_ideal(self):
        """Calcula o valor ideal a ser pedido"""
        compensacao_minima = self.calcular_compensacao_minima()
        
        # Fator de crescimento (15-30% acima do mínimo)
        fator_crescimento = 1.2 + (self.fatores['crescimento_carreira'] / 50)
        
        # Fator de negociação (margem para barganha)
        fator_negociacao = 1.15
        
        valor_ideal_mensal = compensacao_minima * fator_crescimento * fator_negociacao
        
        # Ajuste pelos fatores qualitativos
        fator_qualitativo = (self.fatores['crescimento_carreira'] + 
                           self.fatores['estabilidade'] + 
                           self.fatores['beneficios_qualidade']) / 30
        
        valor_ideal_mensal *= (1 + fator_qualitativo)
        
        return valor_ideal_mensal
    
    def calcular_faixa_recomendada(self):
        """Calcula uma faixa de valores recomendados"""
        minimo = self.calcular_compensacao_minima()
        ideal = self.calcular_valor_ideal()
        
        # Faixa: mínimo até 20% acima do ideal para negociação
        maximo = ideal * 1.2
        
        return {
            'minimo': minimo,
            'ideal': ideal,
            'maximo_negociacao': maximo
        }
    
    def gerar_relatorio(self):
        """Gera um relatório completo"""
        faixa = self.calcular_faixa_recomendada()
        valor_hora_atual = self.calcular_valor_hora_atual()
        
        print("\n" + "="*60)
        print("RELATÓRIO DE PROPOSTA SALARIAL")
        print("="*60)
        
        print(f"\n💰 VALORES RECOMENDADOS:")
        print(f"• Mínimo aceitável: R$ {faixa['minimo']:,.2f}")
        print(f"• Valor ideal: R$ {faixa['ideal']:,.2f}")
        print(f"• Máximo para negociação: R$ {faixa['maximo_negociacao']:,.2f}")
        
        print(f"\n📊 COMPARAÇÃO COM ATUAL:")
        salario_total_atual = self.fatores['salario_atual'] + self.fatores['beneficios_atual']
        aumento_percentual = ((faixa['ideal'] - salario_total_atual) / salario_total_atual) * 100
        
        print(f"• Salário total atual: R$ {salario_total_atual:,.2f}")
        print(f"• Aumento recomendado: {aumento_percentual:.1f}%")
        print(f"• Valor/hora atual: R$ {valor_hora_atual:.2f}")
        
        print(f"\n⚖️ FATORES CONSIDERADOS:")
        print(f"• Custo de vida: +{self.fatores['custo_vida_nova']*100:.1f}%")
        print(f"• Redução tempo deslocamento: {self.fatores['tempo_viagem_atual'] - self.fatores['tempo_viagem_novo']:.1f}h/dia")
        print(f"• Potencial crescimento: {self.fatores['crescimento_carreira']}/10")
        
    def plotar_comparacao(self):
        """Cria um gráfico comparativo"""
        faixa = self.calcular_faixa_recomendada()
        salario_total_atual = self.fatores['salario_atual'] + self.fatores['beneficios_atual']
        
        categorias = ['Salário Atual', 'Mínimo Aceitável', 'Valor Ideal', 'Máximo Negociação']
        valores = [salario_total_atual, faixa['minimo'], faixa['ideal'], faixa['maximo_negociacao']]
        
        plt.figure(figsize=(12, 8))
        
        # Gráfico principal
        plt.subplot(2, 1, 1)
        bars = plt.bar(categorias, valores, color=['lightgray', 'orange', 'green', 'lightblue'])
        plt.ylabel('Valor Mensal (R$)')
        plt.title('Comparação de Propostas Salariais')
        
        # Adicionar valores nas barras
        for bar, valor in zip(bars, valores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                    f'R$ {valor:,.2f}', ha='center', va='bottom')
        
        # Gráfico de fatores
        plt.subplot(2, 1, 2)
        fatores = ['Crescimento', 'Estabilidade', 'Benefícios']
        valores_fatores = [self.fatores['crescimento_carreira'], 
                          self.fatores['estabilidade'], 
                          self.fatores['beneficios_qualidade']]
        
        plt.bar(fatores, valores_fatores, color=['purple', 'red', 'blue'])
        plt.ylim(0, 10)
        plt.ylabel('Avaliação (1-10)')
        plt.title('Fatores Qualitativos Considerados')
        
        plt.tight_layout()
        plt.show()

def main():
    calculadora = CalculadoraProposta()
    
    print("🧮 CALCULADORA DE PROPOSTA SALARIAL")
    print("Vamos calcular quanto pedir na sua nova proposta!\n")
    
    # Coletar dados
    calculadora.coletar_dados_atual()
    calculadora.coletar_expectativas()
    
    # Calcular e mostrar resultados
    calculadora.gerar_relatorio()
    
    # Plotar gráficos
    resposta = input("\nDeseja ver a análise gráfica? (s/n): ").lower()
    if resposta == 's':
        calculadora.plotar_comparacao()
    
    # Salvar relatório
    resposta_salvar = input("\nDeseja salvar o relatório em arquivo? (s/n): ").lower()
    if resposta_salvar == 's':
        with open(f"relatorio_proposta_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", 'w') as f:
            f.write("RELATÓRIO DE PROPOSTA SALARIAL\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"Salário atual: R$ {calculadora.fatores['salario_atual']:,.2f}\n")
            faixa = calculadora.calcular_faixa_recomendada()
            f.write(f"Valor ideal recomendado: R$ {faixa['ideal']:,.2f}\n")
        
        print("Relatório salvo com sucesso!")

if __name__ == "__main__":
    main()
