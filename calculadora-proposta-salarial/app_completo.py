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
        if 'valores_pessoais' not in st.session_state:  # NOVO: Valores pessoais
            st.session_state.valores_pessoais = {
                'estabilidade_financeira': 5,
                'flexibilidade_tempo': 5,
                'crescimento_carreira': 5,
                'equilibrio_vida_pessoal': 5,
                'impacto_social': 3,
                'inovacao_tecnologia': 5,
                'cultura_empresa': 5,
                'aprendizado_continuo': 5,
                'reconhecimento': 5,
                'autonomia': 5,
                'seguranca_juridica': 5,
                'beneficios_nao_monetarios': 5
            }
        
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
    
    @property  # NOVO: Propriedade para valores pessoais
    def valores_pessoais(self):
        return st.session_state.valores_pessoais
    
    @valores_pessoais.setter
    def valores_pessoais(self, value):
        st.session_state.valores_pessoais = value
    
    # NOVO: Método para coletar valores pessoais
    def coletar_valores_pessoais(self):
        """Coleta os valores e prioridades pessoais do funcionário"""
        st.header("🎯 Seus Valores e Prioridades")
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <p style='color: #1e40af; font-weight: bold;'>🔍 Avalie cada fator conforme sua importância pessoal:</p>
        <p><strong>1-3:</strong> Pouco importante | <strong>4-7:</strong> Importante | <strong>8-10:</strong> Muito importante</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("💰 Estabilidade Financeira")
            self.valores_pessoais['estabilidade_financeira'] = st.slider(
                "Valorizo segurança financeira a longo prazo",
                1, 10, value=self.valores_pessoais['estabilidade_financeira'],
                key="estabilidade_financeira_slider"
            )
            
            st.subheader("⏰ Flexibilidade de Tempo")
            self.valores_pessoais['flexibilidade_tempo'] = st.slider(
                "Valorizo horários flexíveis e autonomia",
                1, 10, value=self.valores_pessoais['flexibilidade_tempo'],
                key="flexibilidade_tempo_slider"
            )
            
            st.subheader("📈 Crescimento na Carreira")
            self.valores_pessoais['crescimento_carreira'] = st.slider(
                "Busco rápido crescimento profissional",
                1, 10, value=self.valores_pessoais['crescimento_carreira'],
                key="crescimento_carreira_slider"
            )
            
            st.subheader("⚖️ Equilíbrio Vida Pessoal")
            self.valores_pessoais['equilibrio_vida_pessoal'] = st.slider(
                "Valorizo tempo para família/hobbies",
                1, 10, value=self.valores_pessoais['equilibrio_vida_pessoal'],
                key="equilibrio_vida_slider"
            )
        
        with col2:
            st.subheader("🌍 Impacto Social")
            self.valores_pessoais['impacto_social'] = st.slider(
                "Importante contribuir para sociedade",
                1, 10, value=self.valores_pessoais['impacto_social'],
                key="impacto_social_slider"
            )
            
            st.subheader("💻 Inovação Tecnológica")
            self.valores_pessoais['inovacao_tecnologia'] = st.slider(
                "Valorizo trabalhar com tecnologias novas",
                1, 10, value=self.valores_pessoais['inovacao_tecnologia'],
                key="inovacao_tecnologia_slider"
            )
            
            st.subheader("🏢 Cultura da Empresa")
            self.valores_pessoais['cultura_empresa'] = st.slider(
                "Importante ambiente colaborativo",
                1, 10, value=self.valores_pessoais['cultura_empresa'],
                key="cultura_empresa_slider"
            )
            
            st.subheader("🎓 Aprendizado Contínuo")
            self.valores_pessoais['aprendizado_continuo'] = st.slider(
                "Valorizo oportunidades de aprendizado",
                1, 10, value=self.valores_pessoais['aprendizado_continuo'],
                key="aprendizado_continuo_slider"
            )
        
        with col3:
            st.subheader("🏆 Reconhecimento")
            self.valores_pessoais['reconhecimento'] = st.slider(
                "Valorizo feedback e reconhecimento",
                1, 10, value=self.valores_pessoais['reconhecimento'],
                key="reconhecimento_slider"
            )
            
            st.subheader("🎯 Autonomia e Poder de Decisão")
            self.valores_pessoais['autonomia'] = st.slider(
                "Valorizo independência nas decisões",
                1, 10, value=self.valores_pessoais['autonomia'],
                key="autonomia_slider"
            )
            
            st.subheader("⚖️ Segurança Jurídica")
            self.valores_pessoais['seguranca_juridica'] = st.slider(
                "Importante estabilidade legal (CLT)",
                1, 10, value=self.valores_pessoais['seguranca_juridica'],
                key="seguranca_juridica_slider"
            )
            
            st.subheader("🎁 Benefícios Não-Monetários")
            self.valores_pessoais['beneficios_nao_monetarios'] = st.slider(
                "Valorizo bens/serviços além do salário",
                1, 10, value=self.valores_pessoais['beneficios_nao_monetarios'],
                key="beneficios_nao_monetarios_slider"
            )
        
        # NOVO: Prioridades principais (escolher top 3)
        st.markdown("---")
        st.subheader("🏆 Suas 3 Prioridades Principais")
        
        opcoes_prioridades = [
            "Estabilidade Financeira",
            "Flexibilidade de Tempo", 
            "Crescimento na Carreira",
            "Equilíbrio Vida Pessoal",
            "Impacto Social",
            "Inovação Tecnológica",
            "Cultura da Empresa",
            "Aprendizado Contínuo",
            "Reconhecimento",
            "Autonomia",
            "Segurança Jurídica",
            "Benefícios Não-Monetários"
        ]
        
        col_pri1, col_pri2, col_pri3 = st.columns(3)
        
        with col_pri1:
            self.valores_pessoais['prioridade_1'] = st.selectbox(
                "1ª Prioridade",
                opcoes_prioridades,
                index=0,
                key="prioridade_1_select"
            )
        
        with col_pri2:
            # Remove a prioridade já selecionada
            opcoes_restantes = [op for op in opcoes_prioridades if op != self.valores_pessoais.get('prioridade_1', '')]
            self.valores_pessoais['prioridade_2'] = st.selectbox(
                "2ª Prioridade",
                opcoes_restantes,
                index=min(1, len(opcoes_restantes)-1),
                key="prioridade_2_select"
            )
        
        with col_pri3:
            # Remove as duas prioridades já selecionadas
            opcoes_restantes = [op for op in opcoes_prioridades 
                              if op not in [self.valores_pessoais.get('prioridade_1', ''), 
                                          self.valores_pessoais.get('prioridade_2', '')]]
            self.valores_pessoais['prioridade_3'] = st.selectbox(
                "3ª Prioridade",
                opcoes_restantes,
                index=min(2, len(opcoes_restantes)-1),
                key="prioridade_3_select"
            )
        
        # NOVO: Visualizar perfil de valores
        st.markdown("---")
        if st.button("📊 Visualizar Meu Perfil de Valores", key="visualizar_perfil_btn"):
            self._mostrar_perfil_valores()
    
    # NOVO: Método para mostrar perfil de valores
    def _mostrar_perfil_valores(self):
        """Mostra visualização do perfil de valores"""
        st.subheader("📊 Seu Perfil de Valores")
        
        # Criar DataFrame para visualização
        valores_df = pd.DataFrame({
            'Valor': list(self.valores_pessoais.keys())[:12],  # Exclui prioridades
            'Importância': list(self.valores_pessoais.values())[:12]
        })
        
        # Ordenar por importância
        valores_df = valores_df.sort_values('Importância', ascending=False)
        
        # Gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(valores_df['Valor'], valores_df['Importância'], 
                      color=plt.cm.viridis(valores_df['Importância']/10))
        
        ax.set_xlabel('Importância (1-10)')
        ax.set_title('Seu Perfil de Valores Pessoais')
        ax.set_xlim(0, 10)
        
        # Adicionar valores nas barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{width:.1f}', va='center')
        
        st.pyplot(fig)
        
        # Análise do perfil
        st.markdown("#### 📝 Análise do Seu Perfil")
        
        top_3 = valores_df.nlargest(3, 'Importância')
        st.write(f"**🎯 Seus 3 valores mais importantes:**")
        for idx, (valor, importancia) in enumerate(zip(top_3['Valor'], top_3['Importância']), 1):
            st.write(f"{idx}. {self._traduzir_valor(valor)}: **{importancia}/10**")
        
        # Recomendação baseada no perfil
        perfil_tipo = self._identificar_perfil_tipo(valores_df)
        st.info(f"**🔍 Seu perfil predominante:** {perfil_tipo}")
        
        if perfil_tipo == "Estabilidade":
            st.write("Você valoriza segurança e previsibilidade. Busque empresas estabelecidas e contratos CLT.")
        elif perfil_tipo == "Crescimento":
            st.write("Você prioriza desenvolvimento profissional. Empresas em expansão podem oferecer mais oportunidades.")
        elif perfil_tipo == "Equilíbrio":
            st.write("Qualidade de vida é fundamental. Considere empresas com políticas de flexibilidade.")
        elif perfil_tipo == "Inovação":
            st.write("Você busca desafios e novidades. Startups e empresas de tecnologia podem ser ideais.")
    
    # NOVO: Método auxiliar para traduzir nomes dos valores
    def _traduzir_valor(self, valor_key):
        traducoes = {
            'estabilidade_financeira': 'Estabilidade Financeira',
            'flexibilidade_tempo': 'Flexibilidade de Tempo',
            'crescimento_carreira': 'Crescimento na Carreira',
            'equilibrio_vida_pessoal': 'Equilíbrio Vida Pessoal',
            'impacto_social': 'Impacto Social',
            'inovacao_tecnologia': 'Inovação Tecnológica',
            'cultura_empresa': 'Cultura da Empresa',
            'aprendizado_continuo': 'Aprendizado Contínuo',
            'reconhecimento': 'Reconhecimento',
            'autonomia': 'Autonomia',
            'seguranca_juridica': 'Segurança Jurídica',
            'beneficios_nao_monetarios': 'Benefícios Não-Monetários'
        }
        return traducoes.get(valor_key, valor_key)
    
    # NOVO: Método para identificar tipo de perfil
    def _identificar_perfil_tipo(self, valores_df):
        """Identifica o tipo de perfil predominante"""
        # Calcular médias por categoria
        categorias = {
            'Estabilidade': ['estabilidade_financeira', 'seguranca_juridica'],
            'Crescimento': ['crescimento_carreira', 'aprendizado_continuo', 'reconhecimento'],
            'Equilíbrio': ['flexibilidade_tempo', 'equilibrio_vida_pessoal'],
            'Inovação': ['inovacao_tecnologia', 'autonomia'],
            'Social': ['impacto_social', 'cultura_empresa', 'beneficios_nao_monetarios']
        }
        
        medias = {}
        for categoria, chaves in categorias.items():
            # Filtrar valores que existem no DataFrame
            valores_categoria = valores_df[valores_df['Valor'].isin(chaves)]['Importância'].mean()
            medias[categoria] = valores_categoria if not np.isnan(valores_categoria) else 0
        
        return max(medias.items(), key=lambda x: x[1])[0]
    
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
            st.subheader("Avaliação Qualitativa da Empresa (1-10)")
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
            
            # NOVO: Fatores qualitativos da empresa
            self.fatores['cultura_empresa_nova'] = st.slider(
                "Cultura e ambiente de trabalho", 
                1, 10, value=int(self.fatores.get('cultura_empresa_nova', 7)),
                key="cultura_empresa_nova_slider"
            )
            self.fatores['inovacao_tecnologia_nova'] = st.slider(
                "Inovação e tecnologia utilizada", 
                1, 10, value=int(self.fatores.get('inovacao_tecnologia_nova', 7)),
                key="inovacao_tecnologia_nova_slider"
            )
            
            # Modalidade de contratação
            st.subheader("📝 Modalidade")
            self.fatores['modalidade'] = st.selectbox(
                "Tipo de contratação",
                ["CLT", "PJ"],
                index=0 if self.fatores.get('modalidade', 'CLT') == 'CLT' else 1,
                key="modalidade_input"
            )
    
    # NOVO: Método para calcular compatibilidade com valores pessoais
    def calcular_compatibilidade_valores(self):
        """Calcula compatibilidade entre valores pessoais e nova oportunidade"""
        compatibilidade = {
            'estabilidade_financeira': min(
                self.valores_pessoais['estabilidade_financeira'],
                self.fatores.get('estabilidade', 5)
            ) / 10 * 100,
            'crescimento_carreira': min(
                self.valores_pessoais['crescimento_carreira'],
                self.fatores.get('crescimento_carreira', 5)
            ) / 10 * 100,
            'flexibilidade_tempo': self._calcular_compatibilidade_flexibilidade(),
            'equilibrio_vida_pessoal': self._calcular_compatibilidade_equilibrio(),
            'inovacao_tecnologia': min(
                self.valores_pessoais['inovacao_tecnologia'],
                self.fatores.get('inovacao_tecnologia_nova', 5)
            ) / 10 * 100,
            'cultura_empresa': min(
                self.valores_pessoais['cultura_empresa'],
                self.fatores.get('cultura_empresa_nova', 5)
            ) / 10 * 100
        }
        
        # Média ponderada pelas prioridades
        pesos = {
            'estabilidade_financeira': 1.5 if 'Estabilidade Financeira' in [
                self.valores_pessoais.get('prioridade_1', ''),
                self.valores_pessoais.get('prioridade_2', ''),
                self.valores_pessoais.get('prioridade_3', '')
            ] else 1.0,
            'crescimento_carreira': 1.5 if 'Crescimento na Carreira' in [
                self.valores_pessoais.get('prioridade_1', ''),
                self.valores_pessoais.get('prioridade_2', ''),
                self.valores_pessoais.get('prioridade_3', '')
            ] else 1.0
        }
        
        total_compatibilidade = 0
        total_pesos = 0
        
        for chave, valor in compatibilidade.items():
            peso = pesos.get(chave, 1.0)
            total_compatibilidade += valor * peso
            total_pesos += peso
        
        return {
            'compatibilidade_geral': total_compatibilidade / total_pesos if total_pesos > 0 else 0,
            'detalhado': compatibilidade
        }
    
    # NOVO: Métodos auxiliares para cálculo de compatibilidade
    def _calcular_compatibilidade_flexibilidade(self):
        """Calcula compatibilidade para flexibilidade de tempo"""
        dias_presencial = self.fatores.get('dias_presencial_novo', 3)
        valor_pessoal = self.valores_pessoais['flexibilidade_tempo']
        
        # Quanto mais presencial, menor a compatibilidade para quem valoriza flexibilidade
        if dias_presencial <= 1:
            compatibilidade = 100
        elif dias_presencial == 2:
            compatibilidade = 80
        elif dias_presencial == 3:
            compatibilidade = 60
        elif dias_presencial == 4:
            compatibilidade = 40
        else:
            compatibilidade = 20
        
        # Ajustar pelo valor pessoal
        return min(valor_pessoal * 10, compatibilidade)
    
    def _calcular_compatibilidade_equilibrio(self):
        """Calcula compatibilidade para equilíbrio vida-trabalho"""
        tempo_deslocamento = self.fatores.get('tempo_viagem_novo', 0.5)
        valor_pessoal = self.valores_pessoais['equilibrio_vida_pessoal']
        
        if tempo_deslocamento <= 0.5:
            compatibilidade = 100
        elif tempo_deslocamento <= 1.0:
            compatibilidade = 80
        elif tempo_deslocamento <= 1.5:
            compatibilidade = 60
        elif tempo_deslocamento <= 2.0:
            compatibilidade = 40
        else:
            compatibilidade = 20
        
        return min(valor_pessoal * 10, compatibilidade)
    
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
            
            # NOVO: Ajuste por compatibilidade de valores pessoais
            compatibilidade = self.calcular_compatibilidade_valores()
            fator_valores_pessoais = compatibilidade['compatibilidade_geral'] / 100
            
            # Se compatibilidade alta (>80%), pode aceitar um pouco menos
            if fator_valores_pessoais > 0.8:
                valor_ideal_mensal = valor_ideal_mensal * 0.95  # 5% menos
            # Se compatibilidade baixa (<50%), exige mais compensação
            elif fator_valores_pessoais < 0.5:
                valor_ideal_mensal = valor_ideal_mensal * 1.10  # 10% mais
            
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
            
            # NOVO: Calcular compatibilidade de valores
            compatibilidade = self.calcular_compatibilidade_valores()
            
            # Layout do dashboard
            st.markdown("---")
            st.header("📈 Dashboard de Análise")
            
            # Métricas principais
            col1, col2, col3, col4, col5 = st.columns(5)  # NOVO: Adicionada coluna extra
            
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
            
            with col5:  # NOVO: Métrica de compatibilidade
                compatibilidade_geral = compatibilidade['compatibilidade_geral']
                st.metric("Compatibilidade Valores", f"{compatibilidade_geral:.1f}%")
            
            # Abas para diferentes análises
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Valores", "⚖️ CLT vs PJ", "🎯 Valores Pessoais", "📊 Gráficos", "✅ Checklist"])  # NOVO: Adicionada aba Valores Pessoais
            
            with tab1:
                self._mostrar_aba_valores(faixa, salario_total_atual, comparacao_clt_pj)
            
            with tab2:
                self._mostrar_aba_clt_pj(comparacao_clt_pj, faixa)
            
            with tab3:  # NOVO: Aba de valores pessoais
                self._mostrar_aba_valores_pessoais(compatibilidade)
            
            with tab4:
                self._mostrar_aba_graficos(faixa, salario_total_atual, comparacao_clt_pj, compatibilidade)  # NOVO: Passar compatibilidade
            
            with tab5:
                self._mostrar_aba_checklist(compatibilidade)  # NOVO: Passar compatibilidade
                
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
    
    # NOVO: Aba para mostrar análise de valores pessoais
    def _mostrar_aba_valores_pessoais(self, compatibilidade):
        """Mostra análise de compatibilidade com valores pessoais"""
        st.subheader("🎯 Compatibilidade com Seus Valores")
        
        # Mostrar compatibilidade geral
        st.metric("Compatibilidade Geral", f"{compatibilidade['compatibilidade_geral']:.1f}%")
        
        # Gráfico de compatibilidade por fator
        st.subheader("📊 Compatibilidade por Fator")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        fatores = list(compatibilidade['detalhado'].keys())
        valores = list(compatibilidade['detalhado'].values())
        
        # Ordenar por valor
        sorted_indices = np.argsort(valores)
        fatores = [fatores[i] for i in sorted_indices]
        valores = [valores[i] for i in sorted_indices]
        
        bars = ax.barh(fatores, valores, 
                      color=['red' if v < 50 else 'orange' if v < 70 else 'green' for v in valores])
        
        ax.set_xlabel('Compatibilidade (%)')
        ax.set_title('Compatibilidade com Seus Valores Pessoais')
        ax.set_xlim(0, 100)
        
        # Adicionar valores
        for bar, valor in zip(bars, valores):
            ax.text(valor + 1, bar.get_y() + bar.get_height()/2, 
                   f'{valor:.1f}%', va='center')
        
        st.pyplot(fig)
        
        # Análise detalhada
        st.subheader("📝 Análise Detalhada")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎯 Suas 3 Prioridades Principais:**")
            st.write(f"1. {self.valores_pessoais.get('prioridade_1', 'Não definida')}")
            st.write(f"2. {self.valores_pessoais.get('prioridade_2', 'Não definida')}")
            st.write(f"3. {self.valores_pessoais.get('prioridade_3', 'Não definida')}")
        
        with col2:
            st.write("**🔍 Pontos Fortes desta Oportunidade:**")
            
            # Identificar pontos fortes (compatibilidade > 80%)
            pontos_fortes = []
            for fator, valor in compatibilidade['detalhado'].items():
                if valor > 80:
                    pontos_fortes.append(self._traduzir_valor(fator))
            
            if pontos_fortes:
                for ponto in pontos_fortes[:3]:  # Mostrar até 3
                    st.write(f"✅ {ponto}")
            else:
                st.write("Nenhum ponto forte significativo identificado")
            
            st.write("**⚠️ Pontos de Atenção:**")
            
            # Identificar pontos fracos (compatibilidade < 50%)
            pontos_fracos = []
            for fator, valor in compatibilidade['detalhado'].items():
                if valor < 50:
                    pontos_fracos.append(self._traduzir_valor(fator))
            
            if pontos_fracos:
                for ponto in pontos_fracos[:3]:  # Mostrar até 3
                    st.write(f"❌ {ponto}")
            else:
                st.write("Nenhum ponto fraco crítico identificado")
        
        # Recomendação baseada em valores
        st.markdown("---")
        st.subheader("💡 Recomendação Baseada em Valores")
        
        if compatibilidade['compatibilidade_geral'] >= 80:
            st.success("""
            **🎉 Excelente Compatibilidade!**
            
            Esta oportunidade alinha-se muito bem com seus valores pessoais.
            Mesmo que a oferta salarial não seja a ideal, considere aceitar por:
            - Maior satisfação pessoal e profissional
            - Melhor qualidade de vida
            - Alinhamento com suas prioridades
            """)
        elif compatibilidade['compatibilidade_geral'] >= 60:
            st.warning("""
            **⚠️ Compatibilidade Moderada**
            
            Esta oportunidade tem pontos positivos e negativos em relação aos seus valores.
            Considere:
            - Negociar melhorias nos pontos fracos
            - Avaliar trade-offs entre dinheiro e satisfação
            - Pedir período experimental antes de decidir
            """)
        else:
            st.error("""
            **❌ Baixa Compatibilidade**
            
            Esta oportunidade não atende bem aos seus valores pessoais.
            Só aceite se:
            - A compensação financeira for excepcionalmente boa
            - For uma posição temporária para ganhar experiência
            - Não houver outras opções no momento
            """)
    
    def _mostrar_aba_graficos(self, faixa, salario_total_atual, comparacao_clt_pj, compatibilidade):
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
            fatores = ['Crescimento', 'Estabilidade', 'Benefícios', 'Cultura', 'Inovação']
            valores_fatores = [
                self.fatores.get('crescimento_carreira', 5), 
                self.fatores.get('estabilidade', 5), 
                self.fatores.get('beneficios_qualidade', 5),
                self.fatores.get('cultura_empresa_nova', 5),
                self.fatores.get('inovacao_tecnologia_nova', 5)
            ]
            
            bars2 = ax2.bar(fatores, valores_fatores, color=['purple', 'red', 'blue', 'green', 'orange'])
            ax2.set_ylim(0, 10)
            ax2.set_ylabel('Avaliação (1-10)')
            ax2.set_title('Fatores Qualitativos da Empresa')
            
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
            
            # Gráfico 4: Compatibilidade com valores pessoais
            fatores_compat = ['Estabilidade', 'Crescimento', 'Flexibilidade', 'Equilíbrio', 'Cultura']
            valores_compat = [
                compatibilidade['detalhado'].get('estabilidade_financeira', 0),
                compatibilidade['detalhado'].get('crescimento_carreira', 0),
                compatibilidade['detalhado'].get('flexibilidade_tempo', 0),
                compatibilidade['detalhado'].get('equilibrio_vida_pessoal', 0),
                compatibilidade['detalhado'].get('cultura_empresa', 0)
            ]
            
            ax4.bar(fatores_compat, valores_compat, 
                   color=['blue', 'green', 'orange', 'purple', 'red'])
            ax4.set_ylim(0, 100)
            ax4.set_ylabel('Compatibilidade (%)')
            ax4.set_title('Compatibilidade com Valores Pessoais')
            
            plt.tight_layout()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Erro ao gerar gráficos: {e}")
    
    def _mostrar_aba_checklist(self, compatibilidade):
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
                "💸 Custo de vida suportável": self.fatores.get('custo_vida_nova', 0) <= 0.2,
                "🎯 Compatibilidade valores ≥ 70%": compatibilidade['compatibilidade_geral'] >= 70,  # NOVO
                "🏆 Alinha com prioridades pessoais": self._verificar_prioridades()  # NOVO
            }
            
            pontuacao = sum(decisions.values())
            total = len(decisions)
            
            for item, atendido in decisions.items():
                emoji = "✅" if atendido else "❌"
                st.write(f"{emoji} {item}")
            
            st.metric("Pontuação da Oportunidade", f"{pontuacao}/{total}")
            
            if pontuacao >= 7:
                st.success("🎉 Esta oportunidade parece excelente em todos os aspectos!")
            elif pontuacao >= 5:
                st.warning("⚠️ Avalie cuidadosamente os trade-offs")
            else:
                st.error("❌ Considere outras oportunidades")
            
            # NOVO: Análise baseada em valores
            st.markdown("---")
            st.subheader("💭 Reflexão Baseada em Valores")
            
            st.write("**Perguntas para reflexão:**")
            st.write("1. Esta oportunidade me aproxima dos meus objetivos de longo prazo?")
            st.write("2. Estou disposto a abrir mão de algum valor pessoal por mais dinheiro?")
            st.write("3. Como me sentirei trabalhando aqui daqui a 1 ano?")
            st.write("4. Esta escolha me deixaria mais realizado pessoal e profissionalmente?")
            
            # Exportar relatório
            st.markdown("---")
            st.subheader("📤 Exportar Relatório")
            
            if st.button("💾 Gerar Relatório Completo"):
                relatorio = self._gerar_relatorio_texto(compatibilidade)
                st.download_button(
                    label="📥 Baixar Relatório (.txt)",
                    data=relatorio,
                    file_name=f"relatorio_proposta_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Erro no checklist: {e}")
    
    # NOVO: Método para verificar alinhamento com prioridades
    def _verificar_prioridades(self):
        """Verifica se a oportunidade atende às prioridades pessoais"""
        prioridades = [
            self.valores_pessoais.get('prioridade_1', ''),
            self.valores_pessoais.get('prioridade_2', ''),
            self.valores_pessoais.get('prioridade_3', '')
        ]
        
        # Verificar cada prioridade
        atendidas = 0
        
        for prioridade in prioridades:
            if prioridade == 'Estabilidade Financeira':
                if self.fatores.get('estabilidade', 0) >= 7:
                    atendidas += 1
            elif prioridade == 'Flexibilidade de Tempo':
                if self.fatores.get('dias_presencial_novo', 0) <= 2:
                    atendidas += 1
            elif prioridade == 'Crescimento na Carreira':
                if self.fatores.get('crescimento_carreira', 0) >= 7:
                    atendidas += 1
            elif prioridade == 'Equilíbrio Vida Pessoal':
                if self.fatores.get('tempo_viagem_novo', 0) <= 1.0:
                    atendidas += 1
            # Adicionar outras condições conforme necessário
            
        return atendidas >= 2  # Atende pelo menos 2 das 3 prioridades
    
    def _gerar_relatorio_texto(self, compatibilidade):
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

SEU PERFIL DE VALORES:
- Prioridade 1: {self.valores_pessoais.get('prioridade_1', 'Não definida')}
- Prioridade 2: {self.valores_pessoais.get('prioridade_2', 'Não definida')}
- Prioridade 3: {self.valores_pessoais.get('prioridade_3', 'Não definida')}
- Compatibilidade geral: {compatibilidade['compatibilidade_geral']:.1f}%

NOVA OPORTUNIDADE:
- Modalidade: {modalidade}
- Custo de vida: {self.fatores.get('custo_vida_nova', 0)*100:.1f}%
- Dias presenciais: {self.fatores.get('dias_presencial_novo', 0)}/semana
- Novo deslocamento: {self.fatores.get('tempo_viagem_novo', 0)}h/dia
- Avaliação crescimento: {self.fatores.get('crescimento_carreira', 0)}/10
- Avaliação estabilidade: {self.fatores.get('estabilidade', 0)}/10
- Avaliação cultura: {self.fatores.get('cultura_empresa_nova', 0)}/10

VALORES RECOMENDADOS - {modalidade}:
- Mínimo aceitável: R$ {faixa['minimo'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['minimo']):,.2f}
- Valor ideal: R$ {faixa['ideal'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
- Máximo negociação: R$ {faixa['maximo_negociacao'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['maximo_negociacao']):,.2f}

COMPARAÇÃO CLT vs PJ:
- CLT Líquido: R$ {comparacao['CLT'].get('salario_liquido', 0):,.2f}
- PJ Líquido: R$ {comparacao['PJ'].get('renda_liquida', 0):,.2f}
- Diferença: R$ {comparacao['PJ'].get('renda_liquida', 0) - comparacao['CLT'].get('salario_liquido', 0):,.2f}

ANÁLISE DE COMPATIBILIDADE:
- Compatibilidade geral: {compatibilidade['compatibilidade_geral']:.1f}%
- Estabilidade financeira: {compatibilidade['detalhado'].get('estabilidade_financeira', 0):.1f}%
- Crescimento carreira: {compatibilidade['detalhado'].get('crescimento_carreira', 0):.1f}%
- Flexibilidade tempo: {compatibilidade['detalhado'].get('flexibilidade_tempo', 0):.1f}%
- Equilíbrio vida: {compatibilidade['detalhado'].get('equilibrio_vida_pessoal', 0):.1f}%

RECOMENDAÇÕES:
- Estratégia de negociação: Buscar R$ {faixa['ideal'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['ideal']):,.2f}
- Contraproposta mínima: R$ {faixa['minimo'] if modalidade == 'CLT' else self.calcular_equivalencia_pj_clt(faixa['minimo']):,.2f}
- {'Considerar CLT se oferecerem benefícios equivalentes' if modalidade == 'PJ' else 'Considerar PJ se oferecerem valor equivalente'}
- {'Aceitar com menor salário se compatibilidade for alta' if compatibilidade['compatibilidade_geral'] > 80 else 'Exigir compensação maior se compatibilidade for baixa'}
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
    .valores-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 Calculadora de Proposta Salarial - Completa")
    st.markdown("### Análise completa com valores pessoais, comparação CLT/PJ e cálculos fiscais")
    
    # NOVO: Seção de introdução sobre valores
    st.markdown("""
    <div class="valores-section">
    <h3>🎯 Conheça Seus Valores para Tomar Melhores Decisões</h3>
    <p>Esta calculadora agora inclui uma análise dos seus <strong>valores pessoais</strong> para ajudar a encontrar oportunidades que realmente façam sentido para você, além do aspecto financeiro.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar calculadora
    calculadora = CalculadoraPropostaCompleta()
    
    # Coletar dados em abas
    tab1, tab2, tab3 = st.tabs(["📊 Situação Atual", "🚀 Nova Oportunidade", "🎯 Meus Valores"])
    
    with tab1:
        calculadora.coletar_dados_atual()
    
    with tab2:
        calculadora.coletar_expectativas()
    
    with tab3:
        calculadora.coletar_valores_pessoais()
    
    # Botão para calcular
    st.markdown("---")
    if st.button("🎯 Calcular Análise Completa", type="primary", use_container_width=True):
        with st.spinner("Analisando dados e calculando recomendações..."):
            calculadora.gerar_dashboard()
    
    # Mostrar resultados mesmo sem submit para dados persistidos
    if any(calculadora.fatores.values()) or any(calculadora.valores_pessoais.values()):
        if st.button("📈 Ver Dashboard Existente", key="ver_dashboard_existente"):
            calculadora.gerar_dashboard()

if __name__ == "__main__":
    main()
