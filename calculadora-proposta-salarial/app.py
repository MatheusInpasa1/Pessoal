import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Classe adaptada do calculadora_proposta.py
class CalculadoraPropostaStreamlit:
    def __init__(self):
        self.fatores = {}
    
    def calcular_compensacao_minima(self, dados):
        salario_anual_atual = (dados['salario_atual'] + dados['beneficios_atual']) * 13
        salario_anual_atual += dados['bonus_atual']
        
        salario_ajustado = salario_anual_atual * (1 + dados['custo_vida_nova']/100)
        
        tempo_viagem_atual = dados['tempo_viagem_atual'] * 2 * 22 * 12
        tempo_viagem_novo = dados['tempo_viagem_novo'] * 2 * dados['dias_presencial_novo'] * 4.33 * 12
        
        diferenca_tempo = tempo_viagem_atual - tempo_viagem_novo
        valor_tempo = diferenca_tempo * 50
        
        compensacao_minima_anual = salario_ajustado - valor_tempo
        return compensacao_minima_anual / 13
    
    def calcular_valor_ideal(self, dados, compensacao_minima):
        fator_crescimento = 1.2 + (dados['crescimento_carreira'] / 50)
        fator_negociacao = 1.15
        valor_ideal = compensacao_minima * fator_crescimento * fator_negociacao
        
        fator_qualitativo = (dados['crescimento_carreira'] + 
                           dados['estabilidade'] + 
                           dados['beneficios_qualidade']) / 30
        
        return valor_ideal * (1 + fator_qualitativo)
    
    def calcular_faixa_recomendada(self, dados):
        minimo = self.calcular_compensacao_minima(dados)
        ideal = self.calcular_valor_ideal(dados, minimo)
        maximo = ideal * 1.2
        
        return {
            'minimo': minimo,
            'ideal': ideal,
            'maximo_negociacao': maximo
        }

# Interface Streamlit
def main():
    st.set_page_config(
        page_title="Calculadora de Proposta Salarial",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("🧮 Calculadora de Proposta Salarial")
    st.markdown("Calcule o valor ideal para sua próxima proposta baseado em múltiplos fatores")
    
    calculadora = CalculadoraPropostaStreamlit()
    
    with st.form("proposta_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Situação Atual")
            salario_atual = st.number_input("Salário bruto mensal (R$)", value=5000.0, step=100.0)
            beneficios_atual = st.number_input("Benefícios mensais (R$)", value=1000.0, step=100.0)
            bonus_atual = st.number_input("Bônus anual (R$)", value=5000.0, step=500.0)
            tempo_viagem_atual = st.slider("Deslocamento atual (horas/dia)", 0.0, 4.0, 1.5, 0.5)
        
        with col2:
            st.subheader("🚀 Nova Empresa")
            custo_vida_nova = st.slider("Variação custo de vida (%)", -50.0, 100.0, 10.0, 5.0)
            dias_presencial_novo = st.slider("Dias presenciais/semana", 0, 5, 3)
            tempo_viagem_novo = st.slider("Novo deslocamento (horas/dia)", 0.0, 4.0, 0.5, 0.5)
            crescimento_carreira = st.slider("Potencial crescimento (1-10)", 1, 10, 7)
            estabilidade = st.slider("Estabilidade (1-10)", 1, 10, 6)
            beneficios_qualidade = st.slider("Qualidade benefícios (1-10)", 1, 10, 7)
        
        submitted = st.form_submit_button("🎯 Calcular Proposta", type="primary")
        
        if submitted:
            dados = {
                'salario_atual': salario_atual,
                'beneficios_atual': beneficios_atual,
                'bonus_atual': bonus_atual,
                'tempo_viagem_atual': tempo_viagem_atual,
                'custo_vida_nova': custo_vida_nova,
                'dias_presencial_novo': dias_presencial_novo,
                'tempo_viagem_novo': tempo_viagem_novo,
                'crescimento_carreira': crescimento_carreira,
                'estabilidade': estabilidade,
                'beneficios_qualidade': beneficios_qualidade
            }
            
            faixa = calculadora.calcular_faixa_recomendada(dados)
            salario_total_atual = salario_atual + beneficios_atual
            
            # Mostrar resultados
            st.success("### 📈 Resultados da Análise")
            
            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("Mínimo Aceitável", f"R$ {faixa['minimo']:,.2f}", 
                         delta=f"{((faixa['minimo'] - salario_total_atual)/salario_total_atual*100):.1f}%")
            with col4:
                st.metric("Valor Ideal", f"R$ {faixa['ideal']:,.2f}",
                         delta=f"{((faixa['ideal'] - salario_total_atual)/salario_total_atual*100):.1f}%")
            with col5:
                st.metric("Máximo Negociação", f"R$ {faixa['maximo_negociacao']:,.2f}",
                         delta=f"{((faixa['maximo_negociacao'] - salario_total_atual)/salario_total_atual*100):.1f}%")
            
            # Gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            categorias = ['Salário Atual', 'Mínimo Aceitável', 'Valor Ideal', 'Máximo Negociação']
            valores = [salario_total_atual, faixa['minimo'], faixa['ideal'], faixa['maximo_negociacao']]
            cores = ['lightgray', 'orange', 'green', 'lightblue']
            
            bars = ax.bar(categorias, valores, color=cores)
            ax.set_ylabel('Valor Mensal (R$)')
            ax.set_title('Comparação de Valores Recomendados')
            ax.tick_params(axis='x', rotation=45)
            
            for bar, valor in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                       f'R$ {valor:,.0f}', ha='center', va='bottom', fontweight='bold')
            
            st.pyplot(fig)

if __name__ == "__main__":
    main()
