import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import streamlit as st

class CalculadoraPropostaCompleta:
    def __init__(self):
        # Usar session_state para persistir dados
        if 'fatores' not in st.session_state:
            st.session_state.fatores = {}
        if 'resultados' not in st.session_state:
            st.session_state.resultados = {}
        
    @property
    def fatores(self):
        return st.session_state.fatores
    
    @fatores.setter
    def fatores(self, value):
        st.session_state.fatores = value
        
    def coletar_dados_atual(self):
        """Coleta informações sobre a situação atual"""
        st.header("📊 Situação Atual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Usar chaves únicas para cada input
            self.fatores['salario_atual'] = st.number_input(
                "Salário atual bruto mensal (R$)", 
                min_value=0.0, 
                value=float(self.fatores.get('salario_atual', 5000.0)), 
                step=100.0,
                key="salario_atual_input"
            )
            self.fatores['beneficios_atual'] = st.number_input(
                "Valor dos benefícios (VR, VT, plano saúde, etc.) mensal (R$)", 
                min_value=0.0, 
                value=float(self.fatores.get('beneficios_atual', 1000.0)), 
                step=100.0,
                key="beneficios_atual_input"
            )
            self.fatores['bonus_atual'] = st.number_input(
                "Bônus/PLR anual (R$)", 
                min_value=0.0, 
                value=float(self.fatores.get('bonus_atual', 5000.0)), 
                step=500.0,
                key="bonus_atual_input"
            )
            
        with col2:
            self.fatores['ferias_atual'] = st.number_input(
                "Dias de férias atuais", 
                min_value=10, max_value=40, 
                value=int(self.fatores.get('ferias_atual', 30)),
                key="ferias_atual_input"
            )
            self.fatores['home_office_atual'] = st.slider(
                "Dias de home office por semana", 
                0, 5, 
                value=int(self.fatores.get('home_office_atual', 2)),
                key="home_office_atual_input"
            )
            self.fatores['tempo_viagem_atual'] = st.slider(
                "Tempo de deslocamento diário (horas)", 
                0.0, 4.0, 
                value=float(self.fatores.get('tempo_viagem_atual', 1.5)), 
                0.5,
                key="tempo_viagem_atual_input"
            )
    
    def coletar_expectativas(self):
        """Coleta expectativas e informações da nova empresa"""
        st.header("🚀 Nova Oportunidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            custo_vida_temp = st.slider(
                "Variação no custo de vida (%)", 
                -50.0, 100.0, 
                value=float(self.fatores.get('custo_vida_nova', 10.0) * 100), 
                5.0,
                key="custo_vida_input"
            )
            self.fatores['custo_vida_nova'] = custo_vida_temp / 100
            
            self.fatores['dias_presencial_novo'] = st.slider(
                "Dias de trabalho presencial na nova empresa (por semana)", 
                0, 5, 
                value=int(self.fatores.get('dias_presencial_novo', 3)),
                key="dias_presencial_input"
            )
            
            self.fatores['tempo_viagem_novo'] = st.slider(
                "Tempo de deslocamento novo (horas/dia)", 
                0.0, 4.0, 
                value=float(self.fatores.get('tempo_viagem_novo', 0.5)), 
                0.5,
                key="tempo_viagem_novo_input"
            )
            
            self.fatores['custo_transporte_novo'] = st.number_input(
                "Custo mensal estimado de transporte (R$)", 
                min_value=0.0, 
                value=float(self.fatores.get('custo_transporte_novo', 200.0)), 
                step=50.0,
                key="custo_transporte_input"
            )
        
        with col2:
            st.subheader("Avaliação Qualitativa (1-10)")
            self.fatores['crescimento_carreira'] = st.slider(
                "Potencial de crescimento na nova empresa", 
                1, 10, 
                value=int(self.fatores.get('crescimento_carreira', 7)),
                key="crescimento_input"
            )
            self.fatores['estabilidade'] = st.slider(
                "Estabilidade da nova empresa", 
                1, 10, 
                value=int(self.fatores.get('estabilidade', 6)),
                key="estabilidade_input"
            )
            self.fatores['beneficios_qualidade'] = st.slider(
                "Qualidade dos benefícios", 
                1, 10, 
                value=int(self.fatores.get('beneficios_qualidade', 7)),
                key="beneficios_qualidade_input"
            )
    
    def calcular_impostos_clt(self, salario_bruto):
        """Calcula impostos CLT conforme legislação 2024"""
        # INSS 2024 - Faixas atualizadas
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
        
        # IRRF 2024 - Faixas atualizadas
        base_irrf = salario_bruto - inss
        
        # Dedução por dependente (R$ 189,59 por dependente)
        deducao_dependente = 0  # Você pode adicionar dependentes se quiser
        
        base_irrf_calculada = base_irrf - deducao_dependente
        
        if base_irrf_calculada <= 2259.20:
            irrf = 0
        elif base_irrf_calculada <= 2826.65:
            irrf = (base_irrf_calculada * 0.075) - 169.44
        elif base_irrf_calculada <= 3751.05:
            irrf = (base_irrf_calculada * 0.15) - 381.44
        elif base_irrf_calculada <= 4664.68:
            irrf = (base_irrf_calculada * 0.225) - 662.77
        else:
            irrf = (base_irrf_calculada * 0.275) - 896.00
        
        # Garantir que IRRF não seja negativo
        irrf = max(0, irrf)
        
        salario_liquido = salario_bruto - inss - irrf
        
        return {
            'salario_bruto': salario_bruto,
            'inss': inss,
            'irrf': irrf,
            'salario_liquido': salario_liquido,
            'descontos_totais': inss + irrf,
            'aliquota_efetiva': ((inss + irrf) / salario_bruto) * 100
        }
    
    def calcular_impostos_pj(self, pro_labore, faturamento_restante):
        """Calcula impostos para PJ (Simples Nacional)"""
        try:
            # Pro-labore (tratado como salário)
            impostos_pro_labore = self.calcular_impostos_clt(pro_labore)
            
            # Simples Nacional sobre faturamento (aproximação para serviços)
            # Anexo III - Serviços
            faturamento_anual = faturamento_restante * 12
            
            if faturamento_anual <= 180000:
                aliquota_simples = 0.06  # 6% aproximadamente para serviços
            elif faturamento_anual <= 360000:
                aliquota_simples = 0.112
            elif faturamento_anual <= 720000:
                aliquota_simples = 0.135
            elif faturamento_anual <= 1800000:
                aliquota_simples = 0.16
            elif faturamento_anual <= 3600000:
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
        except Exception as e:
            st.error(f"Erro no cálculo PJ: {e}")
            return {
                'pro_labore': pro_labore,
                'faturamento_restante': faturamento_restante,
                'imposto_pro_labore': 0,
                'imposto_simples': 0,
                'custo_contabilidade': 0,
                'total_impostos': 0,
                'renda_liquida': pro_labore + faturamento_restante,
                'aliquota_efetiva': 0
            }
    
    def comparar_clt_pj(self, valor_clt_bruto, valor_pj_total):
        """Compara CLT vs PJ considerando todos os fatores"""
        try:
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
        except Exception as e:
            st.error(f"Erro na comparação CLT/PJ: {e}")
            return {'CLT': {}, 'PJ': {}}
    
    def calcular_valor_hora_atual(self):
        """Calcula o valor real por hora considerando tempo de deslocamento"""
        try:
            salario_mensal = self.fatores.get('salario_atual', 0)
            beneficios = self.fatores.get('beneficios_atual', 0)
            tempo_viagem = self.fatores.get('tempo_viagem_atual', 0)
            
            horas_trabalho = 8 * 22  # 8 horas/dia, 22 dias/mês
            horas_deslocamento = tempo_viagem * 2 * 22  # Ida e volta
            
            horas_totais = horas_trabalho + horas_deslocamento
            
            if horas_totais > 0:
                return (salario_mensal + beneficios) / horas_totais
            else:
                return 0
        except:
            return 0
    
    def calcular_compensacao_minima(self):
        """Calcula a compensação mínima aceitável"""
        try:
            # Salário atual total anual
            salario_atual = self.fatores.get('salario_atual', 0)
            beneficios_atual = self.fatores.get('beneficios_atual', 0)
            bonus_atual = self.fatores.get('bonus_atual', 0)
            custo_vida = self.fatores.get('custo_vida_nova', 0)
            tempo_viagem_atual = self.fatores.get('tempo_viagem_atual', 0)
            tempo_viagem_novo = self.fatores.get('tempo_viagem_novo', 0)
            dias_presencial = self.fatores.get('dias_presencial_novo', 0)
            
            salario_anual_atual = (salario_atual + beneficios_atual) * 13
            salario_anual_atual += bonus_atual
            
            # Ajuste pelo custo de vida
            salario_ajustado = salario_anual_atual * (1 + custo_vida)
            
            # Ajuste por qualidade de vida (tempo de deslocamento)
            tempo_viagem_atual_horas = tempo_viagem_atual * 2 * 22 * 12
            tempo_viagem_novo_horas = tempo_viagem_novo * 2 * dias_presencial * 4.33 * 12
            
            diferenca_tempo = tempo_viagem_atual_horas - tempo_viagem_novo_horas
            # Valor do tempo: considerando R$ 50/hora (valor subjetivo do tempo livre)
            valor_tempo = diferenca_tempo * 50
            
            compensacao_minima_anual = salario_ajustado - valor_tempo
            compensacao_minima_mensal = compensacao_minima_anual / 13
            
            return max(compensacao_minima_mensal, salario_atual)  # Não menor que atual
        except Exception as e:
            st.error(f"Erro no cálculo da compensação mínima: {e}")
            return self.fatores.get('salario_atual', 5000)
    
    def calcular_valor_ideal(self):
        """Calcula o valor ideal a ser pedido"""
        try:
            compensacao_minima = self.calcular_compensacao_minima()
            
            crescimento = self.fatores.get('crescimento_carreira', 5)
            estabilidade = self.fatores.get('estabilidade', 5)
            beneficios_qualidade = self.fatores.get('beneficios_qualidade', 5)
            
            # Fator de crescimento (15-30% acima do mínimo)
            fator_crescimento = 1.2 + (crescimento / 50)
            
            # Fator de negociação (margem para barganha)
            fator_negociacao = 1.15
            
            valor_ideal_mensal = compensacao_minima * fator_crescimento * fator_negociacao
            
            # Ajuste pelos fatores qualitativos
            fator_qualitativo = (crescimento + estabilidade + beneficios_qualidade) / 30
            
            valor_ideal_mensal *= (1 + fator_qualitativo)
            
            return valor_ideal_mensal
        except Exception as e:
            st.error(f"Erro no cálculo do valor ideal: {e}")
            return self.calcular_compensacao_minima() * 1.3
    
    def calcular_faixa_recomendada(self):
        """Calcula uma faixa de valores recomendados"""
        try:
            minimo = self.calcular_compensacao_minima()
            ideal = self.calcular_valor_ideal()
            
            # Faixa: mínimo até 20% acima do ideal para negociação
            maximo = ideal * 1.2
            
            return {
                'minimo': minimo,
                'ideal': ideal,
                'maximo_negociacao': maximo
            }
        except Exception as e:
            st.error(f"Erro no cálculo da faixa: {e}")
            return {
                'minimo': 5000,
                'ideal': 6000,
                'maximo_negociacao': 7000
            }
    
    def calcular_equivalencia_pj_clt(self, valor_clt):
        """Calcula valor PJ equivalente ao CLT considerando benefícios"""
        # CLT tem 13º, férias, FGTS, etc. PJ precisa ser ~30-40% maior
        fator_equivalencia = 1.35
        return valor_clt * fator_equivalencia
    
    def gerar_dashboard(self):
        """Gera dashboard completo com Streamlit"""
        try:
            faixa = self.calcular_faixa_recomendada()
            salario_total_atual = self.fatores.get('salario_atual', 0) + self.fatores.get('beneficios_atual', 0)
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
                tempo_economizado = (self.fatores.get('tempo_viagem_atual', 0) - self.fatores.get('tempo_viagem_novo', 0)) * 2 * self.fatores.get('dias_presencial_novo', 0) * 4.33
                st.metric("Horas Economizadas/mês", f"{tempo_economizado:.1f}h")
            
            with col4:
                liquido_clt = comparacao_clt_pj['CLT'].get('salario_liquido', 0)
                st.metric("Líquido CLT Ideal", f"R$ {liquido_clt:,.0f}")
            
            # Abas para diferentes análises
            tab1, tab2, tab3, tab4 = st.tabs(["💰 Valores", "⚖️ CLT vs PJ", "📊 Gráficos", "✅ Checklist"])
            
            with tab1:
                self._mostrar_aba_valores(faixa, salario_total_atual, comparacao_clt_pj)
            
            with tab2:
                self._mostrar_aba_clt_pj(comparacao_clt_pj, faixa)
            
            with tab3:
                self._mostrar_aba_graficos(faixa, salario_total_atual, comparacao_clt_pj)
            
            with tab4:
                self._mostrar_aba_checklist()
                
        except Exception as e:
            st.error(f"Erro ao gerar dashboard: {e}")
            st.info("Verifique se todos os campos foram preenchidos corretamente.")
    
    def _mostrar_aba_valores(self, faixa, salario_total_atual, comparacao_clt_pj):
        """Mostra aba de valores recomendados"""
        st.subheader("💵 Valores Recomendados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Mínimo Aceitável:** R$ {faixa['minimo']:,.2f}")
            st.info(f"**Valor Ideal CLT:** R$ {faixa['ideal']:,.2f}")
            st.info(f"**Máximo Negociação:** R$ {faixa['maximo_negociacao']:,.2f}")
            st.info(f"**Equivalente PJ:** R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}")
        
        with col2:
            st.metric("Salário Atual Total", f"R$ {salario_total_atual:,.2f}")
            
            # Mostrar líquidos
            liquido_clt = comparacao_clt_pj['CLT'].get('salario_liquido', 0)
            liquido_pj = comparacao_clt_pj['PJ'].get('renda_liquida', 0)
            
            st.metric("Líquido CLT Ideal", f"R$ {liquido_clt:,.2f}")
            st.metric("Líquido PJ Ideal", f"R$ {liquido_pj:,.2f}")
            
            # Simulador de negociação - USAR SESSION_STATE
            st.subheader("💼 Simulador de Negociação")
            
            # Inicializar proposta_empresa no session_state se não existir
            if 'proposta_empresa' not in st.session_state:
                st.session_state.proposta_empresa = float(faixa['minimo'])
            
            proposta_empresa = st.number_input(
                "Proposta recebida (R$)", 
                value=st.session_state.proposta_empresa,
                step=500.0,
                key="proposta_empresa_input"
            )
            
            # Atualizar session_state
            st.session_state.proposta_empresa = proposta_empresa
            
            if proposta_empresa:
                if proposta_empresa < faixa['minimo']:
                    st.error("❌ Abaixo do mínimo aceitável")
                    st.info(f"**Contraproposta mínima:** R$ {faixa['minimo']:,.2f}")
                elif proposta_empresa < faixa['ideal']:
                    st.warning("⚠️ Dentro da faixa, mas abaixo do ideal")
                    contraproposta = max(proposta_empresa * 1.15, faixa['ideal'])
                    st.success(f"**Sugestão de contraproposta:** R$ {contraproposta:,.2f}")
                else:
                    st.success("✅ Ótima proposta!")
                    st.balloons()
    
    def _mostrar_aba_clt_pj(self, comparacao, faixa):
        """Mostra comparação detalhada CLT vs PJ"""
        st.subheader("⚖️ Comparação CLT vs PJ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 CLT - Detalhamento")
            clt = comparacao['CLT']
            if clt:
                st.write(f"**Bruto:** R$ {clt.get('salario_bruto', 0):,.2f}")
                st.write(f"**INSS:** R$ {clt.get('inss', 0):,.2f}")
                st.write(f"**IRRF:** R$ {clt.get('irrf', 0):,.2f}")
                st.write(f"**Líquido:** R$ {clt.get('salario_liquido', 0):,.2f}")
                st.write(f"**Alíquota Efetiva:** {clt.get('aliquota_efetiva', 0):.1f}%")
                st.write(f"**FGTS/ano:** R$ {clt.get('fgts', 0) * 12:,.2f}")
                st.write(f"**Total Anual:** R$ {clt.get('total_anual', 0):,.2f}")
            else:
                st.warning("Dados CLT não disponíveis")
        
        with col2:
            st.markdown("#### 🏢 PJ - Detalhamento")
            pj = comparacao['PJ']
            if pj:
                st.write(f"**Pro-labore:** R$ {pj.get('pro_labore', 0):,.2f}")
                st.write(f"**Faturamento:** R$ {pj.get('faturamento_restante', 0):,.2f}")
                st.write(f"**Total Bruto:** R$ {pj.get('pro_labore', 0) + pj.get('faturamento_restante', 0):,.2f}")
                st.write(f"**Impostos:** R$ {pj.get('total_impostos', 0):,.2f}")
                st.write(f"**Alíquota Efetiva:** {pj.get('aliquota_efetiva', 0):.1f}%")
                st.write(f"**Líquido:** R$ {pj.get('renda_liquida', 0):,.2f}")
                st.write(f"**Total Anual:** R$ {pj.get('total_anual', 0):,.2f}")
            else:
                st.warning("Dados PJ não disponíveis")
        
        # Recomendação
        st.markdown("---")
        if pj and clt:
            if pj.get('renda_liquida', 0) > clt.get('salario_liquido', 0):
                st.success("**🎯 Recomendação:** PJ pode ser mais vantajoso financeiramente")
            else:
                st.info("**🎯 Recomendação:** CLT oferece mais segurança e benefícios")
    
    def _mostrar_aba_graficos(self, faixa, salario_total_atual, comparacao_clt_pj):
        """Mostra gráficos comparativos"""
        st.subheader("📊 Análise Visual")
        
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Gráfico 1: Comparação de valores
            categorias = ['Atual', 'Mínimo', 'Ideal', 'Máximo']
            valores = [salario_total_atual, faixa['minimo'], faixa['ideal'], faixa['maximo_negociacao']]
            cores = ['lightgray', 'orange', 'green', 'lightblue']
            
            bars1 = ax1.bar(categorias, valores, color=cores)
            ax1.set_ylabel('Valor Mensal (R$)')
            ax1.set_title('Comparação de Propostas (Bruto)')
            for bar, valor in zip(bars1, valores):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                        f'R$ {valor:,.0f}', ha='center', va='bottom')
            
            # Gráfico 2: Fatores qualitativos
            fatores = ['Crescimento', 'Estabilidade', 'Benefícios']
            valores_fatores = [
                self.fatores.get('crescimento_carreira', 5), 
                self.fatores.get('estabilidade', 5), 
                self.fatores.get('beneficios_qualidade', 5)
            ]
            
            bars2 = ax2.bar(fatores, valores_fatores, color=['purple', 'red', 'blue'])
            ax2.set_ylim(0, 10)
            ax2.set_ylabel('Avaliação (1-10)')
            ax2.set_title('Fatores Qualitativos')
            
            # Gráfico 3: CLT vs PJ
            modalidades = ['CLT Líquido', 'PJ Líquido']
            valores_liq = [
                comparacao_clt_pj['CLT'].get('salario_liquido', 0), 
                comparacao_clt_pj['PJ'].get('renda_liquida', 0)
            ]
            
            bars3 = ax3.bar(modalidades, valores_liq, color=['#1f77b4', '#ff7f0e'])
            ax3.set_ylabel('Valor Mensal (R$)')
            ax3.set_title('Comparação CLT vs PJ (Líquido)')
            for bar, valor in zip(bars3, valores_liq):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300, 
                        f'R$ {valor:,.0f}', ha='center', va='bottom')
            
            # Gráfico 4: Impostos
            impostos_clt = [
                comparacao_clt_pj['CLT'].get('inss', 0), 
                comparacao_clt_pj['CLT'].get('irrf', 0)
            ]
            impostos_pj = [
                comparacao_clt_pj['PJ'].get('imposto_pro_labore', 0), 
                comparacao_clt_pj['PJ'].get('imposto_simples', 0),
                comparacao_clt_pj['PJ'].get('custo_contabilidade', 0)
            ]
            
            ax4.pie(impostos_clt + impostos_pj, 
                    labels=['INSS', 'IRRF', 'Pro-labore', 'Simples', 'Contabilidade'],
                    autopct='%1.1f%%')
            ax4.set_title('Distribuição de Impostos')
            
            plt.tight_layout()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Erro ao gerar gráficos: {e}")
    
    def _mostrar_aba_checklist(self):
        """Mostra checklist de decisão"""
        st.subheader("✅ Checklist de Decisão")
        
        try:
            # Calcular pontuação
            decisions = {
                "💰 Salário dentro da faixa ideal": True,
                "🚀 Potencial de crescimento ≥ 7": self.fatores.get('crescimento_carreira', 0) >= 7,
                "🏢 Estabilidade ≥ 6": self.fatores.get('estabilidade', 0) >= 6,
                "🏠 Até 3 dias presenciais": self.fatores.get('dias_presencial_novo', 0) <= 3,
                "⏰ Deslocamento ≤ 1h/dia": self.fatores.get('tempo_viagem_novo', 0) <= 1.0,
                "📈 Benefícios ≥ 7": self.fatores.get('beneficios_qualidade', 0) >= 7,
                "💸 Custo de vida suportável": self.fatores.get('custo_vida_nova', 0) <= 0.2
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
                    file_name=f"relatorio_proposta_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Erro no checklist: {e}")
    
    def _gerar_relatorio_texto(self):
        """Gera relatório completo em texto"""
        try:
            faixa = self.calcular_faixa_recomendada()
            comparacao = self.comparar_clt_pj(faixa['ideal'], self.calcular_equivalencia_pj_clt(faixa['ideal']))
            
            relatorio = f"""
    RELATÓRIO DE PROPOSTA SALARIAL - {datetime.now().strftime('%d/%m/%Y %H:%M')}
    
    SITUAÇÃO ATUAL:
    - Salário bruto: R$ {self.fatores.get('salario_atual', 0):,.2f}
    - Benefícios: R$ {self.fatores.get('beneficios_atual', 0):,.2f}
    - Total atual: R$ {self.fatores.get('salario_atual', 0) + self.fatores.get('beneficios_atual', 0):,.2f}
    - Tempo deslocamento: {self.fatores.get('tempo_viagem_atual', 0)}h/dia
    
    NOVA OPORTUNIDADE:
    - Custo de vida: {self.fatores.get('custo_vida_nova', 0)*100:.1f}%
    - Dias presenciais: {self.fatores.get('dias_presencial_novo', 0)}/semana
    - Novo deslocamento: {self.fatores.get('tempo_viagem_novo', 0)}h/dia
    
    VALORES RECOMENDADOS:
    - Mínimo aceitável: R$ {faixa['minimo']:,.2f}
    - Valor ideal CLT: R$ {faixa['ideal']:,.2f}
    - Equivalente PJ: R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
    - Máximo negociação: R$ {faixa['maximo_negociacao']:,.2f}
    
    COMPARAÇÃO CLT vs PJ:
    - CLT Bruto: R$ {comparacao['CLT'].get('salario_bruto', 0):,.2f}
    - CLT Líquido: R$ {comparacao['CLT'].get('salario_liquido', 0):,.2f}
    - PJ Líquido: R$ {comparacao['PJ'].get('renda_liquida', 0):,.2f}
    - Diferença: R$ {comparacao['PJ'].get('renda_liquida', 0) - comparacao['CLT'].get('salario_liquido', 0):,.2f}
    
    FATORES QUALITATIVOS:
    - Crescimento: {self.fatores.get('crescimento_carreira', 0)}/10
    - Estabilidade: {self.fatores.get('estabilidade', 0)}/10  
    - Benefícios: {self.fatores.get('beneficios_qualidade', 0)}/10
    
    RECOMENDAÇÕES:
    - Estratégia de negociação: Buscar R$ {faixa['ideal']:,.2f} (CLT)
    - Contraproposta mínima: R$ {faixa['minimo']:,.2f}
    - Considerar PJ se oferecerem acima de R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
            """
            return relatorio
        except Exception as e:
            return f"Erro ao gerar relatório: {e}"

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
    
    # Inicializar calculadora
    calculadora = CalculadoraPropostaCompleta()
    
    # Coletar dados
    with st.form("dados_principais"):
        calculadora.coletar_dados_atual()
        calculadora.coletar_expectativas()
        
        submitted = st.form_submit_button("🎯 Calcular Análise Completa", type="primary")
    
    # Mostrar resultados mesmo sem submit para dados persistidos
    if submitted or any(calculadora.fatores.values()):
        calculadora.gerar_dashboard()

if __name__ == "__main__":
    main()
