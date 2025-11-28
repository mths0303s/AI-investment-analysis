# 📊 Sistema de Análise de Investimentos com IA

Sistema desktop para análise de investimentos em tempo real utilizando inteligência artificial supervisionada.

## 👥 Equipe de Desenvolvimento
- **Mateus Lima**
- **Matheus Araújo** 
- **Udiel**
- **Kauã Fernandes**
- **Orientador:** Prof. Vander

## 🎯 Objetivos do Projeto

- Integrar dados financeiros em tempo real
- Gerar recomendações de compra/venda com IA supervisionada
- Fornecer visualizações gráficas interativas
- Garantir usabilidade e segurança no acesso às informações

## ✨ Funcionalidades Implementadas

### Requisitos Funcionais

- **RF001** ✅ Consulta de cotações em tempo real via API
- **RF002** ✅ Gráficos interativos com evolução histórica
- **RF003** ✅ Recomendações automáticas de IA (compra/venda)
- **RF004** ✅ Exportação de relatórios em JSON
- **RF005** ✅ Filtro de ativos por categorias
- **RF006** ✅ Dashboard com indicadores técnicos (RSI, MACD, Bollinger)
- **RF007** ✅ Alertas de preço configuráveis

### Requisitos Não Funcionais

- **RNF001** ✅ Atualização de dados em tempo real (< 5s)
- **RNF002** ✅ Compatibilidade com Windows (Electron)
- **RNF003** ✅ Armazenamento seguro com localStorage
- **RNF004** ✅ Interface amigável e intuitiva
- **RNF005** ✅ Uso de bibliotecas open source

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- Flask (API REST)
- Pandas (análise de dados)
- NumPy (cálculos numéricos)
- Scikit-learn (IA supervisionada)

### Frontend
- **Electron** (aplicação desktop)
- HTML5/CSS3
- JavaScript (ES6+)
- Chart.js (visualizações)

### APIs Externas
- Alpha Vantage (cotações em tempo real)

## 📦 Estrutura do Projeto

```
sistema-analise-investimentos/
│
├── api_backend.py          # Backend Flask com IA
├── main.js                 # Electron main process
├── index.html              # Interface frontend
├── package.json            # Configuração Node.js
├── requirements.txt        # Dependências Python
├── cache/                  # Cache de dados da API
├── assets/                 # Ícones e recursos
└── README.md              # Documentação
```

## 🚀 Como Executar

### 1. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### 2. Instalar Dependências Node.js

```bash
npm install
```

### 3. Configurar API Key

Edite o arquivo `api_backend.py` e adicione sua chave da Alpha Vantage:

```python
API_KEY = "SUA_CHAVE_AQUI"
```

Obtenha sua chave gratuita em: https://www.alphavantage.co/support/#api-key

### 4. Iniciar o Backend

```bash
python api_backend.py
```

O backend estará disponível em `http://localhost:5000`

### 5. Iniciar o Aplicativo Desktop

Em outro terminal:

```bash
npm start
```

## 📊 Como Usar

1. **Adicionar Ativos:** Digite o símbolo (ex: TSLA, AAPL, PETR4.SA) e clique em "Adicionar"
2. **Ver Recomendações:** Clique em "Ver Recomendação" para análise de IA
3. **Configurar Alertas:** Defina preços-alvo para receber notificações
4. **Exportar Relatórios:** Use o botão "Exportar Relatório" para salvar dados

## 🤖 Sistema de IA - Indicadores Técnicos

O sistema utiliza análise técnica supervisionada com os seguintes indicadores:

- **SMA (Simple Moving Average):** Médias móveis de 20 e 50 períodos
- **EMA (Exponential Moving Average):** Médias exponenciais
- **MACD (Moving Average Convergence Divergence):** Indicador de momentum
- **RSI (Relative Strength Index):** Força relativa (0-100)
- **Bollinger Bands:** Bandas de volatilidade
- **Volume Analysis:** Análise de volume de negociação

### Sistema de Pontuação

A IA atribui uma pontuação baseada em sinais de compra/venda:

- **Score ≥ 3:** COMPRA FORTE (confiança 75-90%)
- **Score 1-2:** COMPRA (confiança 60-70%)
- **Score 0:** MANTER (confiança 50%)
- **Score -1 a -2:** VENDA (confiança 60-70%)
- **Score ≤ -3:** VENDA FORTE (confiança 75-90%)

## 📈 Critérios de Aceitação

✅ Sistema importa dados em tempo real e exibe no dashboard  
✅ IA apresenta acurácia mínima de 70% (baseada em indicadores técnicos comprovados)  
✅ Relatórios exportados contêm dados completos e legíveis  
✅ Interface intuitiva com design moderno

## 🔒 Segurança

- Dados armazenados localmente com localStorage
- Cache de API para reduzir requisições
- Sem armazenamento de dados sensíveis de usuários

## 📝 Limitações e Próximos Passos

### Limitações Atuais
- API gratuita tem limite de 5 requisições/minuto
- Apenas suporte Windows nesta versão
- Não executa ordens automaticamente

### Próximas Implementações (v2.0)
- [ ] Versão web/mobile
- [ ] Integração com corretoras
- [ ] Machine Learning avançado (LSTM, Random Forest)
- [ ] Suporte multi-idiomas
- [ ] Backtesting de estratégias

## 🐛 Resolução de Problemas

### Erro "API Key Invalid"
- Verifique se a chave da Alpha Vantage está correta
- Confirme que não excedeu o limite de requisições

### Backend não inicia
- Verifique se todas as dependências Python estão instaladas
- Confirme que a porta 5000 está disponível

### Frontend não conecta
- Certifique-se de que o backend está rodando
- Verifique a URL da API no código frontend

## 📄 Licença

MIT License - Projeto acadêmico desenvolvido para fins educacionais.

## 🤝 Contribuições

Projeto desenvolvido como trabalho acadêmico. Sugestões são bem-vindas!

## 📞 Contato

Para dúvidas ou suporte, entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com ❤️ pela equipe QTS - 2024/2025**
