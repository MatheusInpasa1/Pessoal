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
        if 'beneficios_detalhados' not in st.session_state:
            st.session_state.beneficios_detalhados = {}
        
    @property
    def fatores(self):
        return st.session_state.fatores
    
    @fatores.setter
    def fatores(self, value):
        st.session_state.fatores = value
        
    @property
    def beneficios_detalhados(self):
        return st.session_state.beneficios_detalhados
    
    @beneficios_detalhados.setter
    def beneficios_detalhados(self, value):
        st.session_state.beneficios_detalhados = value
        
    def coletar_dados_atual(self):
        """Coleta informações sobre a situação atual"""
        st.header("📊 Situação Atual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.fatores['salario_atual'] = st.number_input(
                "Salário atual bruto mensal (R$)", 
                min_value=0.0, 
                value=float(self.fatores.get('salario_atual', 5000.0)), 
                step=100.0,
                key="salario_atual_input"
            )
            
            # Benefícios detalhados
            st.subheader("💼 Benefícios Atuais (Mensais)")
            
            self.beneficios_detalhados['va_vr'] = st.number_input(
                "VA/VR (R$)", 
                min_value=0.0, 
                value=float(self.beneficios_detalhados.get('va_vr', 600.0)), 
                step=50.0,
                key="va_vr_input"
            )
            
            self.beneficios_detalhados['vt'] = st.number_input(
                "Vale Transporte (R$)", 
                min_value=0.0, 
                value=float(self.beneficios_detalhados.get('vt', 300.0)), 
                step=50.0,
                key="vt_input"
            )
            
            self.beneficios_detalhados['plano_saude'] = st.checkbox(
                "Plano de Saúde",
                value=bool(self.beneficios_detalhados.get('plano_saude', True)),
                key="plano_saude_check"
            )
            
            if self.beneficios_detalhados['plano_saude']:
                self.beneficios_detalhados['coparticipacao'] = st.number_input(
                    "Coparticipação mensal (R$)", 
                    min_value=0.0, 
                    value=float(self.beneficios_detalhados.get('coparticipacao', 200.0)), 
                    step=50.0,
                    key="coparticipacao_input"
                )
            else:
                self.beneficios_detalhados['coparticipacao'] = 0
            
            self.beneficios_detalhados['outros_beneficios'] = st.number_input(
                "Outros benefícios (R$)", 
                min_value=0.0, 
                value=float(self.beneficios_detalhados.get('outros_beneficios', 0.0)), 
                step=50.0,
                key="outros_beneficios_input"
            )
            
            # Calcular total de benefícios
            total_beneficios = (self.beneficios_detalhados['va_vr'] + 
                              self.beneficios_detalhados['vt'] + 
                              self.beneficios_detalhados['coparticipacao'] + 
                              self.beneficios_detalhados['outros_beneficios'])
            
            self.fatores['beneficios_atual'] = total_beneficios
            st.info(f"**Total benefícios:** R$ {total_beneficios:,.2f}")
            
        with col2:
            self.fatores['bonus_atual'] = st.number_input(
                "Bônus/PLR anual (R$)", 
                min_value=0.0, 
                value=float(self.fatores.get('bonus_atual', 5000.0)), 
                step=500.0,
                key="bonus_atual_input"
            )
            
            self.fatores['ferias_atual'] = st.number_input(
                "Dias de férias atuais", 
                min_value=10, 
                max_value=40, 
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
                min_value=0.0, 
                max_value=4.0, 
                value=float(self.fatores.get('tempo_viagem_atual', 1.5)), 
                step=0.5,
                key="tempo_viagem_atual_input"
            )
            
            # Resumo da situação atual
            st.subheader("📋 Resumo Atual")
            salario_total = self.fatores['salario_atual'] + self.fatores['beneficios_atual']
            st.metric("Remuneração Total Mensal", f"R$ {salario_total:,.2f}")
    
    def coletar_expectativas(self):
        """Coleta expectativas e informações da nova empresa"""
        st.header("🚀 Nova Oportunidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            custo_vida_temp = st.slider(
                "Variação no custo de vida (%)", 
                min_value=-50.0, 
                max_value=100.0, 
                value=float(self.fatores.get('custo_vida_nova', 10.0) * 100), 
                step=5.0,
                key="custo_vida_input"
            )
            self.fatores['custo_vida_nova'] = custo_vida_temp / 100
            
            self.fatores['dias_presencial_novo'] = st.slider(
                "Dias de trabalho presencial na nova empresa (por semana)", 
                min_value=0, 
                max_value=5, 
                value=int(self.fatores.get('dias_presencial_novo', 3)),
                key="dias_presencial_input"
            )
            
            self.fatores['tempo_viagem_novo'] = st.slider(
                "Tempo de deslocamento novo (horas/dia)", 
                min_value=0.0, 
                max_value=4.0, 
                value=float(self.fatores.get('tempo_viagem_novo', 0.5)), 
                step=0.5,
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
                min_value=1, 
                max_value=10, 
                value=int(self.fatores.get('crescimento_carreira', 7)),
                key="crescimento_input"
            )
            self.fatores['estabilidade'] = st.slider(
                "Estabilidade da nova empresa", 
                min_value=1, 
                max_value=10, 
                value=int(self.fatores.get('estabilidade', 6)),
                key="estabilidade_input"
            )
            self.fatores['beneficios_qualidade'] = st.slider(
                "Qualidade dos benefícios", 
                min_value=1, 
                max_value=10, 
                value=int(self.fatores.get('beneficios_qualidade', 7)),
                key="beneficios_qualidade_input"
            )
            
            # Modalidade de contratação
            st.subheader("📝 Modalidade")
            self.fatores['modalidade'] = st.selectbox(
                "Tipo de contratação",
                ["CLT", "PJ"],
                index=0 if self.fatores.get('modalidade', 'CLT') == 'CLT' else 1,
                key="modalidade_input"
            )
    
    def calcular_impostos_clt(self, salario_bruto):
        """Calcula impostos CLT conforme legislação 2024 - CORRIGIDO"""
        try:
            # INSS 2024 - Faixas atualizadas e cálculo correto
            if salario_bruto <= 1412.00:
                inss = salario_bruto * 0.075
            elif salario_bruto <= 2666.68:
                inss = 105.90 + ((salario_bruto - 1412.00) * 0.09)
            elif salario_bruto <= 4000.03:
                inss = 105.90 + 113.09 + ((salario_bruto - 2666.68) * 0.12)
            elif salario_bruto <= 7786.02:
                inss = 105.90 + 113.09 + 160.00 + ((salario_bruto - 4000.03) * 0.14)
            else:
                inss = 908.85  # Teto do INSS
            
            # IRRF 2024 - Cálculo correto
            base_irrf = salario_bruto - inss
            
            # Tabela IRRF 2024
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
            
            # Garantir que IRRF não seja negativo
            irrf = max(0, irrf)
            
            salario_liquido = salario_bruto - inss - irrf
            
            return {
                'salario_bruto': salario_bruto,
                'inss': inss,
                'irrf': irrf,
                'salario_liquido': salario_liquido,
                'descontos_totais': inss + irrf,
                'aliquota_efetiva': ((inss + irrf) / salario_bruto) * 100 if salario_bruto > 0 else 0
            }
        except Exception as e:
            st.error(f"Erro cálculo CLT: {e}")
            return {
                'salario_bruto': salario_bruto,
                'inss': 0,
                'irrf': 0,
                'salario_liquido': salario_bruto,
                'descontos_totais': 0,
                'aliquota_efetiva': 0
            }
    
    def calcular_impostos_pj(self, valor_pj_total):
        """Calcula impostos para PJ (Simples Nacional) - CORRIGIDO"""
        try:
            # Para PJ, consideramos que 40% é pro-labore e 60% é lucro/empresa
            pro_labore = valor_pj_total * 0.4
            faturamento_empresa = valor_pj_total * 0.6
            
            # Impostos sobre pro-labore (como CLT)
            impostos_pro_labore = self.calcular_impostos_clt(pro_labore)
            
            # Simples Nacional sobre faturamento da empresa
            # Anexo III - Serviços (aproximação)
            faturamento_anual = faturamento_empresa * 12
            
            if faturamento_anual <= 180000:
                aliquota_simples = 0.06  # 6% para serviços
            elif faturamento_anual <= 360000:
                aliquota_simples = 0.112
            elif faturamento_anual <= 720000:
                aliquota_simples = 0.135
            elif faturamento_anual <= 1800000:
                aliquota_simples = 0.16
            else:
                aliquota_simples = 0.21
            
            imposto_simples = faturamento_empresa * aliquota_simples
            
            # Custo contábil mensal
            custo_contabilidade = 200.0
            
            # Outros custos PJ
            custo_administrativo = 100.0
            
            total_impostos_pj = (impostos_pro_labore['descontos_totais'] + 
                               imposto_simples + 
                               custo_contabilidade + 
                               custo_administrativo)
            
            renda_liquida_pj = valor_pj_total - total_impostos_pj
            
            return {
                'valor_total': valor_pj_total,
                'pro_labore': pro_labore,
                'faturamento_empresa': faturamento_empresa,
                'imposto_pro_labore': impostos_pro_labore['descontos_totais'],
                'imposto_simples': imposto_simples,
                'custo_contabilidade': custo_contabilidade,
                'custo_administrativo': custo_administrativo,
                'total_impostos': total_impostos_pj,
                'renda_liquida': renda_liquida_pj,
                'aliquota_efetiva': (total_impostos_pj / valor_pj_total) * 100 if valor_pj_total > 0 else 0
            }
        except Exception as e:
            st.error(f"Erro cálculo PJ: {e}")
            return {
                'valor_total': valor_pj_total,
                'pro_labore': 0,
                'faturamento_empresa': 0,
                'imposto_pro_labore': 0,
                'imposto_simples': 0,
                'custo_contabilidade': 0,
                'custo_administrativo': 0,
                'total_impostos': 0,
                'renda_liquida': valor_pj_total,
                'aliquota_efetiva': 0
            }
    
    def comparar_clt_pj(self, valor_clt_bruto, valor_pj_total):
        """Compara CLT vs PJ considerando todos os fatores - CORRIGIDO"""
        try:
            # CLT
            clt = self.calcular_impostos_clt(valor_clt_bruto)
            
            # Benefícios CLT (13º, férias, FGTS)
            decimo_terceiro = valor_clt_bruto
            ferias = valor_clt_bruto + (valor_clt_bruto / 3)  # Férias + 1/3
            fgts_anual = valor_clt_bruto * 0.08 * 12
            
            clt['total_anual'] = (clt['salario_liquido'] * 13) + ferias + fgts_anual
            clt['decimo_terceiro'] = decimo_terceiro
            clt['ferias'] = ferias
            clt['fgts_anual'] = fgts_anual
            
            # PJ
            pj = self.calcular_impostos_pj(valor_pj_total)
            pj['total_anual'] = pj['renda_liquida'] * 12
            
            return {'CLT': clt, 'PJ': pj}
        except Exception as e:
            st.error(f"Erro comparação CLT/PJ: {e}")
            return {'CLT': {}, 'PJ': {}}
    
    def calcular_valor_hora_atual(self):
        """Calcula o valor real por hora considerando tempo de deslocamento"""
        try:
            salario_mensal = self.fatores.get('salario_atual', 0)
            beneficios = self.fatores.get('beneficios_atual', 0)
            tempo_viagem = self.fatores.get('tempo_viagem_atual', 0)
            
            # 44 horas semanais = 220 horas mensais (44 * 5)
            horas_trabalho = 220
            horas_deslocamento = tempo_viagem * 2 * 22  # Ida e volta, 22 dias úteis
            
            horas_totais = horas_trabalho + horas_deslocamento
            
            if horas_totais > 0:
                return (salario_mensal + beneficios) / horas_totais
            else:
                return 0
        except:
            return 0
    
    def calcular_compensacao_minima(self):
        """Calcula a compensação mínima aceitável - CORRIGIDO"""
        try:
            # Salário atual total MENSAL (não anual)
            salario_atual = self.fatores.get('salario_atual', 0)
            beneficios_atual = self.fatores.get('beneficios_atual', 0)
            bonus_atual = self.fatores.get('bonus_atual', 0)
            custo_vida = self.fatores.get('custo_vida_nova', 0)
            tempo_viagem_atual = self.fatores.get('tempo_viagem_atual', 0)
            tempo_viagem_novo = self.fatores.get('tempo_viagem_novo', 0)
            dias_presencial = self.fatores.get('dias_presencial_novo', 0)
            
            # Remuneração total atual mensal
            remuneracao_atual_mensal = salario_atual + beneficios_atual
            
            # Ajuste pelo custo de vida (sobre a remuneração atual)
            remuneracao_ajustada = remuneracao_atual_mensal * (1 + custo_vida)
            
            # Ajuste por qualidade de vida (tempo de deslocamento)
            # Considerando valor de R$ 30/hora para tempo livre
            horas_economizadas_mes = (tempo_viagem_atual - tempo_viagem_novo) * 2 * dias_presencial * 4.33
            valor_tempo_economizado = horas_economizadas_mes * 30
            
            # Bônus convertido para mensal
            bonus_mensal = bonus_atual / 12
            
            compensacao_minima_mensal = remuneracao_ajustada + valor_tempo_economizado + bonus_mensal
            
            return max(compensacao_minima_mensal, remuneracao_atual_mensal)
            
        except Exception as e:
            st.error(f"Erro cálculo compensação mínima: {e}")
            return self.fatores.get('salario_atual', 5000) + self.fatores.get('beneficios_atual', 1000)
    
    def calcular_valor_ideal(self):
        """Calcula o valor ideal a ser pedido - CORRIGIDO"""
        try:
            compensacao_minima = self.calcular_compensacao_minima()
            
            crescimento = self.fatores.get('crescimento_carreira', 5)
            estabilidade = self.fatores.get('estabilidade', 5)
            beneficios_qualidade = self.fatores.get('beneficios_qualidade', 5)
            
            # Fator base de crescimento (20-40% acima do mínimo)
            fator_base = 1.3
            
            # Ajustes por fatores qualitativos
            ajuste_crescimento = crescimento * 0.02  # 2% por ponto
            ajuste_estabilidade = estabilidade * 0.015  # 1.5% por ponto
            ajuste_beneficios = beneficios_qualidade * 0.015  # 1.5% por ponto
            
            fator_total = (fator_base + 
                         ajuste_crescimento + 
                         ajuste_estabilidade + 
                         ajuste_beneficios)
            
            valor_ideal_mensal = compensacao_minima * fator_total
            
            return valor_ideal_mensal
            
        except Exception as e:
            st.error(f"Erro cálculo valor ideal: {e}")
            return self.calcular_compensacao_minima() * 1.3
    
    def calcular_faixa_recomendada(self):
        """Calcula uma faixa de valores recomendados"""
        try:
            minimo = self.calcular_compensacao_minima()
            ideal = self.calcular_valor_ideal()
            
            # Faixa: mínimo até 25% acima do ideal para negociação
            maximo = ideal * 1.25
            
            return {
                'minimo': minimo,
                'ideal': ideal,
                'maximo_negociacao': maximo
            }
        except Exception as e:
            st.error(f"Erro cálculo faixa: {e}")
            salario_base = self.fatores.get('salario_atual', 5000) + self.fatores.get('beneficios_atual', 1000)
            return {
                'minimo': salario_base,
                'ideal': salario_base * 1.3,
                'maximo_negociacao': salario_base * 1.5
            }
    
    def calcular_equivalencia_pj_clt(self, valor_clt):
        """Calcula valor PJ equivalente ao CLT considerando benefícios"""
        # CLT tem 13º, férias, FGTS, etc. PJ precisa ser ~40-50% maior
        fator_equivalencia = 1.45
        return valor_clt * fator_equivalencia
    
    def gerar_dashboard(self):
        """Gera dashboard completo com Streamlit"""
        try:
            faixa = self.calcular_faixa_recomendada()
            salario_total_atual = self.fatores.get('salario_atual', 0) + self.fatores.get('beneficios_atual', 0)
            valor_hora_atual = self.calcular_valor_hora_atual()
            
            # Comparação CLT vs PJ baseada na modalidade selecionada
            if self.fatores.get('modalidade', 'CLT') == 'CLT':
                comparacao_clt_pj = self.comparar_clt_pj(faixa['ideal'], self.calcular_equivalencia_pj_clt(faixa['ideal']))
            else:
                comparacao_clt_pj = self.comparar_clt_pj(faixa['ideal'] / 1.45, faixa['ideal'])
            
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
                modalidade = self.fatores.get('modalidade', 'CLT')
                if modalidade == 'CLT':
                    liquido = comparacao_clt_pj['CLT'].get('salario_liquido', 0)
                else:
                    liquido = comparacao_clt_pj['PJ'].get('renda_liquida', 0)
                st.metric(f"Líquido {modalidade} Ideal", f"R$ {liquido:,.0f}")
            
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
            modalidade = self.fatores.get('modalidade', 'CLT')
            
            if modalidade == 'CLT':
                st.info(f"**Mínimo Aceitável:** R$ {faixa['minimo']:,.2f}")
                st.info(f"**Valor Ideal CLT:** R$ {faixa['ideal']:,.2f}")
                st.info(f"**Máximo Negociação:** R$ {faixa['maximo_negociacao']:,.2f}")
                st.info(f"**Equivalente PJ:** R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}")
            else:
                st.info(f"**Mínimo Aceitável:** R$ {self.calcular_equivalencia_pj_clt(faixa['minimo']):,.2f}")
                st.info(f"**Valor Ideal PJ:** R$ {self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}")
                st.info(f"**Máximo Negociação:** R$ {self.calcular_equivalencia_pj_clt(faixa['maximo_negociacao']):,.2f}")
                st.info(f"**Equivalente CLT:** R$ {faixa['ideal']:,.2f}")
        
        with col2:
            st.metric("Salário Atual Total", f"R$ {salario_total_atual:,.2f}")
            
            # Mostrar líquidos
            liquido_clt = comparacao_clt_pj['CLT'].get('salario_liquido', 0)
            liquido_pj = comparacao_clt_pj['PJ'].get('renda_liquida', 0)
            
            st.metric("Líquido CLT Ideal", f"R$ {liquido_clt:,.2f}")
            st.metric("Líquido PJ Ideal", f"R$ {liquido_pj:,.2f}")
            
            # Simulador de negociação
            st.subheader("💼 Simulador de Negociação")
            
            if 'proposta_empresa' not in st.session_state:
                modalidade = self.fatores.get('modalidade', 'CLT')
                if modalidade == 'CLT':
                    st.session_state.proposta_empresa = float(faixa['minimo'])
                else:
                    st.session_state.proposta_empresa = float(self.calcular_equivalencia_pj_clt(faixa['minimo']))
            
            proposta_empresa = st.number_input(
                "Proposta recebida (R$)", 
                value=st.session_state.proposta_empresa,
                step=500.0,
                key="proposta_empresa_input"
            )
            
            st.session_state.proposta_empresa = proposta_empresa
            
            if proposta_empresa:
                modalidade = self.fatores.get('modalidade', 'CLT')
                if modalidade == 'CLT':
                    minimo = faixa['minimo']
                    ideal = faixa['ideal']
                else:
                    minimo = self.calcular_equivalencia_pj_clt(faixa['minimo'])
                    ideal = self.calcular_equivalencia_pj_clt(faixa['ideal'])
                
                if proposta_empresa < minimo:
                    st.error("❌ Abaixo do mínimo aceitável")
                    st.info(f"**Contraproposta mínima:** R$ {minimo:,.2f}")
                elif proposta_empresa < ideal:
                    st.warning("⚠️ Dentro da faixa, mas abaixo do ideal")
                    contraproposta = max(proposta_empresa * 1.10, ideal)
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
                st.write(f"**13º + Férias:** R$ {clt.get('decimo_terceiro', 0) + clt.get('ferias', 0):,.2f}")
                st.write(f"**FGTS/ano:** R$ {clt.get('fgts_anual', 0):,.2f}")
                st.write(f"**Total Anual:** R$ {clt.get('total_anual', 0):,.2f}")
            else:
                st.warning("Dados CLT não disponíveis")
        
        with col2:
            st.markdown("#### 🏢 PJ - Detalhamento")
            pj = comparacao['PJ']
            if pj:
                st.write(f"**Valor Total:** R$ {pj.get('valor_total', 0):,.2f}")
                st.write(f"**Pro-labore:** R$ {pj.get('pro_labore', 0):,.2f}")
                st.write(f"**Faturamento Empresa:** R$ {pj.get('faturamento_empresa', 0):,.2f}")
                st.write(f"**Impostos Pro-labore:** R$ {pj.get('imposto_pro_labore', 0):,.2f}")
                st.write(f"**Impostos Empresa:** R$ {pj.get('imposto_simples', 0):,.2f}")
                st.write(f"**Custos:** R$ {pj.get('custo_contabilidade', 0) + pj.get('custo_administrativo', 0):,.2f}")
                st.write(f"**Alíquota Efetiva:** {pj.get('aliquota_efetiva', 0):.1f}%")
                st.write(f"**Líquido:** R$ {pj.get('renda_liquida', 0):,.2f}")
                st.write(f"**Total Anual:** R$ {pj.get('total_anual', 0):,.2f}")
            else:
                st.warning("Dados PJ não disponíveis")
        
        # Recomendação
        st.markdown("---")
        if pj and clt:
            diferenca = pj.get('renda_liquida', 0) - clt.get('salario_liquido', 0)
            if diferenca > 500:
                st.success(f"**🎯 Recomendação:** PJ é {diferenca:,.0f} mais vantajoso mensalmente")
            elif diferenca < -500:
                st.info(f"**🎯 Recomendação:** CLT é {abs(diferenca):,.0f} mais vantajoso mensalmente")
            else:
                st.info("**🎯 Recomendação:** Ambas as modalidades são equivalentes financeiramente")
    
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
                comparacao_clt_pj['PJ'].get('custo_contabilidade', 0) + comparacao_clt_pj['PJ'].get('custo_administrativo', 0)
            ]
            
            ax4.pie(impostos_clt + impostos_pj, 
                    labels=['INSS', 'IRRF', 'Pro-labore', 'Simples', 'Custos PJ'],
                    autopct='%1.1f%%')
            ax4.set_title('Distribuição de Impostos e Custos')
            
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
            modalidade = self.fatores.get('modalidade', 'CLT')
            
            relatorio = f"""
RELATÓRIO DE PROPOSTA SALARIAL - {datetime.now().strftime('%d/%m/%Y %H:%M')}

SITUAÇÃO ATUAL:
- Salário bruto: R$ {self.fatores.get('salario_atual', 0):,.2f}
- Benefícios totais: R$ {self.fatores.get('beneficios_atual', 0):,.2f}
- VA/VR: R$ {self.beneficios_detalhados.get('va_vr', 0):,.2f}
- VT: R$ {self.beneficios_detalhados.get('vt', 0):,.2f}
- Plano saúde: {'Sim' if self.beneficios_detalhados.get('plano_saude', False) else 'Não'}
- Coparticipação: R$ {self.beneficios_detalhados.get('coparticipacao', 0):,.2f}
- Outros: R$ {self.beneficios_detalhados.get('outros_beneficios', 0):,.2f}
- Total atual: R$ {self.fatores.get('salario_atual', 0) + self.fatores.get('beneficios_atual', 0):,.2f}
- Tempo deslocamento: {self.fatores.get('tempo_viagem_atual', 0)}h/dia

NOVA OPORTUNIDADE:
- Modalidade: {modalidade}
- Custo de vida: {self.fatores.get('custo_vida_nova', 0)*100:.1f}%
- Dias presenciais: {self.fatores.get('dias_presencial_novo', 0)}/semana
- Novo deslocamento: {self.fatores.get('tempo_viagem_novo', 0)}h/dia

VALORES RECOMENDADOS - {modalidade}:
- Mínimo aceitável: R$ {faixa['minimo'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['minimo']):,.2f}
- Valor ideal: R$ {faixa['ideal'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
- Máximo negociação: R$ {faixa['maximo_negociacao'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['maximo_negociacao']):,.2f}

COMPARAÇÃO CLT vs PJ:
- CLT Líquido: R$ {comparacao['CLT'].get('salario_liquido', 0):,.2f}
- PJ Líquido: R$ {comparacao['PJ'].get('renda_liquida', 0):,.2f}
- Diferença: R$ {comparacao['PJ'].get('renda_liquida', 0) - comparacao['CLT'].get('salario_liquido', 0):,.2f}

FATORES QUALITATIVOS:
- Crescimento: {self.fatores.get('crescimento_carreira', 0)}/10
- Estabilidade: {self.fatores.get('estabilidade', 0)}/10  
- Benefícios: {self.fatores.get('beneficios_qualidade', 0)}/10

RECOMENDAÇÕES:
- Estratégia de negociação: Buscar R$ {faixa['ideal'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
- Contraproposta mínima: R$ {faixa['minimo'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['minimo']):,.2f}
- {'Considerar CLT se oferecerem benefícios equivalentes' if modalidade == 'PJ' else 'Considerar PJ se oferecerem valor equivalente'}
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
