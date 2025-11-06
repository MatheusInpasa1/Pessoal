import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import streamlit as st

class CalculadoraPropostaCompleta:
    def __init__(self):
        self.fatores = {}
        self.resultados = {}
        
    def coletar_dados_atual(self):
        """Coleta informações sobre a situação atual"""
        st.header("📊 Situação Atual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.fatores['salario_atual'] = st.number_input(
                "Salário atual bruto mensal (R$)", 
                min_value=0.0, value=5000.0, step=100.0
            )
            self.fatores['beneficios_atual'] = st.number_input(
                "Valor dos benefícios (VR, VT, plano saúde, etc.) mensal (R$)", 
                min_value=0.0, value=1000.0, step=100.0
            )
            self.fatores['bonus_atual'] = st.number_input(
                "Bônus/PLR anual (R$)", 
                min_value=0.0, value=5000.0, step=500.0
            )
            
        with col2:
            self.fatores['ferias_atual'] = st.number_input(
                "Dias de férias atuais", 
                min_value=10, max_value=40, value=30
            )
            self.fatores['home_office_atual'] = st.slider(
                "Dias de home office por semana", 
                0, 5, 2
            )
            self.fatores['tempo_viagem_atual'] = st.slider(
                "Tempo de deslocamento diário (horas)", 
                0.0, 4.0, 1.5, 0.5
            )
    
    def coletar_expectativas(self):
        """Coleta expectativas e informações da nova empresa"""
        st.header("🚀 Nova Oportunidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.fatores['custo_vida_nova'] = st.slider(
                "Variação no custo de vida (%)", 
                -50.0, 100.0, 10.0, 5.0
            ) / 100
            
            self.fatores['dias_presencial_novo'] = st.slider(
                "Dias de trabalho presencial na nova empresa (por semana)", 
                0, 5, 3
            )
            
            self.fatores['tempo_viagem_novo'] = st.slider(
                "Tempo de deslocamento novo (horas/dia)", 
                0.0, 4.0, 0.5, 0.5
            )
            
            self.fatores['custo_transporte_novo'] = st.number_input(
                "Custo mensal estimado de transporte (R$)", 
                min_value=0.0, value=200.0, step=50.0
            )
        
        with col2:
            st.subheader("Avaliação Qualitativa (1-10)")
            self.fatores['crescimento_carreira'] = st.slider(
                "Potencial de crescimento na nova empresa", 
                1, 10, 7
            )
            self.fatores['estabilidade'] = st.slider(
                "Estabilidade da nova empresa", 
                1, 10, 6
            )
            self.fatores['beneficios_qualidade'] = st.slider(
                "Qualidade dos benefícios", 
                1, 10, 7
            )
    
    def calcular_impostos_clt(self, salario_bruto):
        """Calcula impostos CLT conforme legislação 2024"""
        # INSS 2024
        if salario_bruto <= 1412.00:
            inss = salario_bruto * 0.075
        elif salario_bruto <= 2666.68:
            inss = (1412.00 * 0.075) + ((salario_bruto - 1412.00) * 0.09)
        elif salario_bruto <= 4000.03:
            inss = (1412.00 * 0.075) + ((2666.68 - 1412.00) * 0.09) + ((salario_bruto - 2666.68) * 0.12)
        elif salario_bruto <= 7786.02:
            inss = (1412.00 * 0.075) + ((2666.68 - 1412.00) * 0.09) + ((4000.03 - 2666.68) * 0.12) + ((salario_bruto - 4000.03) * 0.14)
        else:
            inss = 908.85  # Teto do INSS
        
        # IRRF 2024
        base_irrf = salario_bruto - inss
        if base_irrf <= 2259.20:
            irrf = 0
        elif base_irrf <= 2826.65:
            irrf = (base_irrf * 0.075) - 169.44
        elif base_irrf <= 3751.05:
            irrf = (base_irrf * 0.15) - 381.44
        elif base_irrf <= 4664.68:
            irrf = (base_irrf * 0.225) - 662.77
        else:
            irrf = (base_irrf * 0.275) - 896.00
        
        salario_liquido = salario_bruto - inss - irrf
        
        return {
            'salario_bruto': salario_bruto,
            'inss': inss,
            'irrf': irrf,
            'salario_liquido': salario_liquido,
            'descontos_totais': inss + irrf
        }
    
    def calcular_impostos_pj(self, pro_labore, faturamento_restante):
        """Calcula impostos para PJ (Simples Nacional)"""
        # Pro-labore (tratado como salário)
        impostos_pro_labore = self.calcular_impostos_clt(pro_labore)
        
        # Simples Nacional sobre faturamento (aproximação)
        # Anexo III - Serviços
        if faturamento_restante <= 180000:
            aliquota_simples = 0.06  # 6% aproximadamente para serviços
        elif faturamento_restante <= 360000:
            aliquota_simples = 0.112
        elif faturamento_restante <= 720000:
            aliquota_simples = 0.135
        elif faturamento_restante <= 1800000:
            aliquota_simples = 0.16
        elif faturamento_restante <= 3600000:
            aliquota_simples = 0.21
        else:
            aliquota_simples = 0.33
        
        imposto_simples = faturamento_restante * aliquota_simples
        
        # Custo contábil mensal estimado
        custo_contabilidade = 300.0
        
        total_impostos_pj = impostos_pro_labore['descontos_totais'] + imposto_simples + custo_contabilidade
        renda_liquida_pj = pro_labore + faturamento_restante - total_impostos_pj
        
        return {
            'pro_labore': pro_labore,
            'faturamento_restante': faturamento_restante,
            'imposto_pro_labore': impostos_pro_labore['descontos_totais'],
            'imposto_simples': imposto_simples,
            'custo_contabilidade': custo_contabilidade,
            'total_impostos': total_impostos_pj,
            'renda_liquida': renda_liquida_pj,
            'aliquota_efetiva': (total_impostos_pj / (pro_labore + faturamento_restante)) * 100
        }
    
    def comparar_clt_pj(self, valor_clt_bruto, valor_pj_total):
        """Compara CLT vs PJ considerando todos os fatores"""
        # CLT
        clt = self.calcular_impostos_clt(valor_clt_bruto)
        clt['ferias'] = valor_clt_bruto
        clt['decimo_terceiro'] = valor_clt_bruto
        clt['fgts'] = valor_clt_bruto * 0.08
        clt['total_anual'] = (clt['salario_liquido'] * 13) + clt['ferias'] + clt['fgts'] * 12
        
        # PJ (considerando 80% do valor CLT como pro-labore e 20% como lucro)
        pro_labore = valor_pj_total * 0.8
        faturamento_restante = valor_pj_total * 0.2
        pj = self.calcular_impostos_pj(pro_labore, faturamento_restante)
        pj['total_anual'] = pj['renda_liquida'] * 12
        
        return {'CLT': clt, 'PJ': pj}
    
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
    
    def calcular_equivalencia_pj_clt(self, valor_clt):
        """Calcula valor PJ equivalente ao CLT considerando benefícios"""
        # CLT tem 13º, férias, FGTS, etc. PJ precisa ser ~30-40% maior
        fator_equivalencia = 1.35
        return valor_clt * fator_equivalencia
    
    def gerar_dashboard(self):
        """Gera dashboard completo com Streamlit"""
        faixa = self.calcular_faixa_recomendada()
        salario_total_atual = self.fatores['salario_atual'] + self.fatores['beneficios_atual']
        valor_hora_atual = self.calcular_valor_hora_atual()
        
        # Comparação CLT vs PJ
        comparacao_clt_pj = self.comparar_clt_pj(faixa['ideal'], self.calcular_equivalencia_pj_clt(faixa['ideal']))
        
        # Layout do dashboard
        st.markdown("---")
        st.header("📈 Dashboard de Análise")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            aumento_ideal = ((faixa['ideal'] - salario_total_atual) / salario_total_atual) * 100
            st.metric("Aumento Ideal", f"{aumento_ideal:.1f}%", f"R$ {faixa['ideal'] - salario_total_atual:,.0f}")
        
        with col2:
            st.metric("Valor/Hora Atual", f"R$ {valor_hora_atual:.2f}")
        
        with col3:
            tempo_economizado = (self.fatores['tempo_viagem_atual'] - self.fatores['tempo_viagem_novo']) * 2 * self.fatores['dias_presencial_novo'] * 4.33
            st.metric("Horas Economizadas/mês", f"{tempo_economizado:.1f}h")
        
        with col4:
            liquido_clt = comparacao_clt_pj['CLT']['salario_liquido']
            st.metric("Líquido CLT Ideal", f"R$ {liquido_clt:,.0f}")
        
        # Abas para diferentes análises
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Valores", "⚖️ CLT vs PJ", "📊 Gráficos", "✅ Checklist"])
        
        with tab1:
            self._mostrar_aba_valores(faixa, salario_total_atual)
        
        with tab2:
            self._mostrar_aba_clt_pj(comparacao_clt_pj, faixa)
        
        with tab3:
            self._mostrar_aba_graficos(faixa, salario_total_atual, comparacao_clt_pj)
        
        with tab4:
            self._mostrar_aba_checklist()
    
    def _mostrar_aba_valores(self, faixa, salario_total_atual):
        """Mostra aba de valores recomendados"""
        st.subheader("💵 Valores Recomendados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Mínimo Aceitável:** R$ {faixa['minimo']:,.2f}")
            st.info(f"**Valor Ideal:** R$ {faixa['ideal']:,.2f}")
            st.info(f"**Máximo Negociação:** R$ {faixa['maximo_negociacao']:,.2f}")
        
        with col2:
            st.metric("Salário Atual Total", f"R$ {salario_total_atual:,.2f}")
            st.metric("Equivalente PJ", f"R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}")
            
            # Simulador de negociação
            st.subheader("💼 Simulador de Negociação")
            proposta_empresa = st.number_input(
                "Proposta recebida (R$)", 
                value=float(faixa['minimo']),
                step=500.0
            )
            
            if proposta_empresa:
                if proposta_empresa < faixa['minimo']:
                    st.error("❌ Abaixo do mínimo aceitável")
                elif proposta_empresa < faixa['ideal']:
                    st.warning("⚠️ Dentro da faixa, mas abaixo do ideal")
                    contraproposta = proposta_empresa * 1.15
                    st.info(f"**Sugestão de contraproposta:** R$ {contraproposta:,.2f}")
                else:
                    st.success("✅ Ótima proposta!")
    
    def _mostrar_aba_clt_pj(self, comparacao, faixa):
        """Mostra comparação detalhada CLT vs PJ"""
        st.subheader("⚖️ Comparação CLT vs PJ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 CLT")
            clt = comparacao['CLT']
            st.write(f"**Bruto:** R$ {clt['salario_bruto']:,.2f}")
            st.write(f"**INSS:** R$ {clt['inss']:,.2f}")
            st.write(f"**IRRF:** R$ {clt['irrf']:,.2f}")
            st.write(f"**Líquido:** R$ {clt['salario_liquido']:,.2f}")
            st.write(f"**FGTS/ano:** R$ {clt['fgts'] * 12:,.2f}")
            st.write(f"**Total Anual:** R$ {clt['total_anual']:,.2f}")
        
        with col2:
            st.markdown("#### 🏢 PJ")
            pj = comparacao['PJ']
            st.write(f"**Pro-labore:** R$ {pj['pro_labore']:,.2f}")
            st.write(f"**Faturamento:** R$ {pj['faturamento_restante']:,.2f}")
            st.write(f"**Impostos:** R$ {pj['total_impostos']:,.2f}")
            st.write(f"**Alíquota Efetiva:** {pj['aliquota_efetiva']:.1f}%")
            st.write(f"**Líquido:** R$ {pj['renda_liquida']:,.2f}")
            st.write(f"**Total Anual:** R$ {pj['total_anual']:,.2f}")
        
        # Recomendação
        st.markdown("---")
        if comparacao['PJ']['renda_liquida'] > comparacao['CLT']['salario_liquido']:
            st.success("**🎯 Recomendação:** PJ pode ser mais vantajoso financeiramente")
        else:
            st.info("**🎯 Recomendação:** CLT oferece mais segurança e benefícios")
    
    def _mostrar_aba_graficos(self, faixa, salario_total_atual, comparacao_clt_pj):
        """Mostra gráficos comparativos"""
        st.subheader("📊 Análise Visual")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Comparação de valores
        categorias = ['Atual', 'Mínimo', 'Ideal', 'Máximo']
        valores = [salario_total_atual, faixa['minimo'], faixa['ideal'], faixa['maximo_negociacao']]
        cores = ['lightgray', 'orange', 'green', 'lightblue']
        
        bars1 = ax1.bar(categorias, valores, color=cores)
        ax1.set_ylabel('Valor Mensal (R$)')
        ax1.set_title('Comparação de Propostas')
        for bar, valor in zip(bars1, valores):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                    f'R$ {valor:,.0f}', ha='center', va='bottom')
        
        # Gráfico 2: Fatores qualitativos
        fatores = ['Crescimento', 'Estabilidade', 'Benefícios']
        valores_fatores = [self.fatores['crescimento_carreira'], 
                          self.fatores['estabilidade'], 
                          self.fatores['beneficios_qualidade']]
        
        bars2 = ax2.bar(fatores, valores_fatores, color=['purple', 'red', 'blue'])
        ax2.set_ylim(0, 10)
        ax2.set_ylabel('Avaliação (1-10)')
        ax2.set_title('Fatores Qualitativos')
        
        # Gráfico 3: CLT vs PJ
        modalidades = ['CLT Líquido', 'PJ Líquido']
        valores_liq = [comparacao_clt_pj['CLT']['salario_liquido'], 
                      comparacao_clt_pj['PJ']['renda_liquida']]
        
        bars3 = ax3.bar(modalidades, valores_liq, color=['#1f77b4', '#ff7f0e'])
        ax3.set_ylabel('Valor Mensal (R$)')
        ax3.set_title('Comparação CLT vs PJ (Líquido)')
        for bar, valor in zip(bars3, valores_liq):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300, 
                    f'R$ {valor:,.0f}', ha='center', va='bottom')
        
        # Gráfico 4: Impostos
        impostos_clt = [comparacao_clt_pj['CLT']['inss'], comparacao_clt_pj['CLT']['irrf']]
        impostos_pj = [comparacao_clt_pj['PJ']['imposto_pro_labore'], 
                      comparacao_clt_pj['PJ']['imposto_simples'],
                      comparacao_clt_pj['PJ']['custo_contabilidade']]
        
        ax4.pie(impostos_clt + impostos_pj, 
                labels=['INSS', 'IRRF', 'Pro-labore', 'Simples', 'Contabilidade'],
                autopct='%1.1f%%')
        ax4.set_title('Distribuição de Impostos')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def _mostrar_aba_checklist(self):
        """Mostra checklist de decisão"""
        st.subheader("✅ Checklist de Decisão")
        
        # Calcular pontuação
        decisions = {
            "💰 Salário dentro da faixa ideal": True,  # Sempre true pois é calculado
            "🚀 Potencial de crescimento ≥ 7": self.fatores['crescimento_carreira'] >= 7,
            "🏢 Estabilidade ≥ 6": self.fatores['estabilidade'] >= 6,
            "🏠 Até 3 dias presenciais": self.fatores['dias_presencial_novo'] <= 3,
            "⏰ Deslocamento ≤ 1h/dia": self.fatores['tempo_viagem_novo'] <= 1.0,
            "📈 Benefícios ≥ 7": self.fatores['beneficios_qualidade'] >= 7,
            "💸 Custo de vida suportável": self.fatores['custo_vida_nova'] <= 0.2
        }
        
        pontuacao = sum(decisions.values())
        total = len(decisions)
        
        for item, atendido in decisions.items():
            emoji = "✅" if atendido else "❌"
            st.write(f"{emoji} {item}")
        
        st.metric("Pontuação da Oportunidade", f"{pontuacao}/{total}")
        
        if pontuacao >= 5:
            st.success("🎉 Esta oportunidade parece excelente!")
        elif pontuacao >= 3:
            st.warning("⚠️ Avalie cuidadosamente os trade-offs")
        else:
            st.error("❌ Considere outras oportunidades")
        
        # Exportar relatório
        st.markdown("---")
        st.subheader("📤 Exportar Relatório")
        
        if st.button("💾 Gerar Relatório Completo"):
            relatorio = self._gerar_relatorio_texto()
            st.download_button(
                label="📥 Baixar Relatório (.txt)",
                data=relatorio,
                file_name=f"relatorio_proposta_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    def _gerar_relatorio_texto(self):
        """Gera relatório completo em texto"""
        faixa = self.calcular_faixa_recomendada()
        comparacao = self.comparar_clt_pj(faixa['ideal'], self.calcular_equivalencia_pj_clt(faixa['ideal']))
        
        relatorio = f"""
RELATÓRIO DE PROPOSTA SALARIAL - {datetime.now().strftime('%d/%m/%Y %H:%M')}

SITUAÇÃO ATUAL:
- Salário bruto: R$ {self.fatores['salario_atual']:,.2f}
- Benefícios: R$ {self.fatores['beneficios_atual']:,.2f}
- Total atual: R$ {self.fatores['salario_atual'] + self.fatores['beneficios_atual']:,.2f}
- Tempo deslocamento: {self.fatores['tempo_viagem_atual']}h/dia

NOVA OPORTUNIDADE:
- Custo de vida: {self.fatores['custo_vida_nova']*100:.1f}%
- Dias presenciais: {self.fatores['dias_presencial_novo']}/semana
- Novo deslocamento: {self.fatores['tempo_viagem_novo']}h/dia

VALORES RECOMENDADOS:
- Mínimo aceitável: R$ {faixa['minimo']:,.2f}
- Valor ideal CLT: R$ {faixa['ideal']:,.2f}
- Equivalente PJ: R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
- Máximo negociação: R$ {faixa['maximo_negociacao']:,.2f}

COMPARAÇÃO CLT vs PJ:
- CLT Líquido: R$ {comparacao['CLT']['salario_liquido']:,.2f}
- PJ Líquido: R$ {comparacao['PJ']['renda_liquida']:,.2f}
- Diferença: R$ {comparacao['PJ']['renda_liquida'] - comparacao['CLT']['salario_liquido']:,.2f}

FATORES QUALITATIVOS:
- Crescimento: {self.fatores['crescimento_carreira']}/10
- Estabilidade: {self.fatores['estabilidade']}/10  
- Benefícios: {self.fatores['beneficios_qualidade']}/10

RECOMENDAÇÕES:
- Estratégia de negociação: Buscar R$ {faixa['ideal']:,.2f} (CLT)
- Contraproposta mínima: R$ {faixa['minimo']:,.2f}
- Considerar PJ se oferecerem acima de R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
        """
        return relatorio

# Interface Streamlit
def main():
    st.set_page_config(
        page_title="Calculadora de Proposta Salarial - Completa",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Calculadora de Proposta Salarial - Completa")
    st.markdown("### Análise completa com comparação CLT vs PJ e cálculos fiscais")
    
    calculadora = CalculadoraPropostaCompleta()
    
    # Coletar dados
    with st.form("dados_principais"):
        calculadora.coletar_dados_atual()
        calculadora.coletar_expectativas()
        
        submitted = st.form_submit_button("🎯 Calcular Análise Completa", type="primary")
    
    if submitted:
        calculadora.gerar_dashboard()

if __name__ == "__main__":
    main()
