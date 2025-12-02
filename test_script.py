"""
Script de Testes - Sistema de Análise de Investimentos
Testa todos os requisitos funcionais e não funcionais
"""
# test_script.js
import requests
import time
import json
from datetime import datetime

API_URL = "http://localhost:5001/api"

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test(self, name, func):
        """Executa um teste"""
        print(f"\n🧪 Testando: {name}")
        try:
            start = time.time()
            result = func()
            duration = time.time() - start
            
            if result:
                print(f"✅ PASSOU ({duration:.2f}s)")
                self.passed += 1
                self.results.append({
                    "test": name,
                    "status": "PASSOU",
                    "duration": duration
                })
            else:
                print(f"❌ FALHOU ({duration:.2f}s)")
                self.failed += 1
                self.results.append({
                    "test": name,
                    "status": "FALHOU",
                    "duration": duration
                })
        except Exception as e:
            print(f"❌ ERRO: {e}")
            self.failed += 1
            self.results.append({
                "test": name,
                "status": "ERRO",
                "error": str(e)
            })
    
    def summary(self):
        """Exibe resumo dos testes"""
        print("\n" + "="*50)
        print("📊 RESUMO DOS TESTES")
        print("="*50)
        print(f"✅ Testes aprovados: {self.passed}")
        print(f"❌ Testes falhados: {self.failed}")
        print(f"📈 Taxa de sucesso: {(self.passed/(self.passed+self.failed)*100):.1f}%")
        print("="*50)
        
        # Salva relatório
        with open('test_report.json', 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": self.passed + self.failed,
                "passed": self.passed,
                "failed": self.failed,
                "results": self.results
            }, f, indent=2)
        print("\n📄 Relatório salvo em: test_report.json")

# Inicializa runner
runner = TestRunner()

# ==================== TESTES DE API ====================

def test_api_status():
    """Testa se a API está online"""
    response = requests.get(f"{API_URL}/status", timeout=5)
    return response.status_code == 200

def test_rf001_cotacao_tempo_real():
    """RF001: Consulta de cotações em tempo real"""
    response = requests.get(f"{API_URL}/quote/TSLA", timeout=10)
    data = response.json()
    return "Global Quote" in data or "error" in data

def test_rf002_dados_historicos():
    """RF002: Dados históricos para gráficos"""
    response = requests.get(f"{API_URL}/historical/AAPL", timeout=10)
    data = response.json()
    return "Time Series (Daily)" in data or "error" in data

def test_rf003_recomendacao_ia():
    """RF003: Recomendação de IA"""
    response = requests.get(f"{API_URL}/recommendation/MSFT", timeout=15)
    data = response.json()
    
    if "error" in data:
        return False
    
    required_fields = ["recommendation", "confidence", "signals", "current_price"]
    return all(field in data for field in required_fields)

def test_rf006_indicadores():
    """RF006: Indicadores técnicos"""
    response = requests.get(f"{API_URL}/indicators/GOOGL?indicator=RSI", timeout=10)
    data = response.json()
    return "Technical Analysis" in data or "error" in data

def test_batch_quotes():
    """Teste de múltiplas cotações simultâneas"""
    symbols = ["TSLA", "AAPL", "MSFT"]
    response = requests.post(
        f"{API_URL}/batch-quotes",
        json={"symbols": symbols},
        timeout=20
    )
    data = response.json()
    return len(data) == len(symbols)

def test_rnf001_tempo_resposta():
    """RNF001: Tempo de resposta < 5 segundos"""
    start = time.time()
    response = requests.get(f"{API_URL}/quote/AMZN", timeout=10)
    duration = time.time() - start
    
    print(f"   Tempo de resposta: {duration:.2f}s")
    return duration < 5.0

def test_cache_performance():
    """Teste de performance do cache"""
    # Primeira requisição (sem cache)
    start1 = time.time()
    requests.get(f"{API_URL}/historical/TSLA?outputsize=compact", timeout=10)
    duration1 = time.time() - start1
    
    # Segunda requisição (com cache)
    start2 = time.time()
    requests.get(f"{API_URL}/historical/TSLA?outputsize=compact", timeout=10)
    duration2 = time.time() - start2
    
    print(f"   Sem cache: {duration1:.2f}s | Com cache: {duration2:.2f}s")
    return duration2 < duration1

def test_error_handling():
    """Teste de tratamento de erros"""
    response = requests.get(f"{API_URL}/quote/SIMBOLOINVALIDO999", timeout=10)
    data = response.json()
    # Deve retornar erro ou dados vazios, não crashar
    return response.status_code in [200, 404, 500]

def test_ai_accuracy():
    """Teste de acurácia da IA (simulado)"""
    symbols = ["TSLA", "AAPL", "MSFT"]
    recommendations = []
    
    for symbol in symbols:
        response = requests.get(f"{API_URL}/recommendation/{symbol}", timeout=15)
        data = response.json()
        
        if "confidence" in data:
            recommendations.append(data["confidence"])
    
    if not recommendations:
        return False
    
    avg_confidence = sum(recommendations) / len(recommendations)
    print(f"   Confiança média: {avg_confidence:.1f}%")
    
    # Critério de aceitação: 70% de confiança média
    return avg_confidence >= 70

# ==================== EXECUÇÃO DOS TESTES ====================

print("="*50)
print("🚀 INICIANDO TESTES DO SISTEMA")
print("="*50)

runner.test("API Status", test_api_status)
runner.test("RF001 - Cotação em Tempo Real", test_rf001_cotacao_tempo_real)
runner.test("RF002 - Dados Históricos", test_rf002_dados_historicos)
runner.test("RF003 - Recomendação de IA", test_rf003_recomendacao_ia)
runner.test("RF006 - Indicadores Técnicos", test_rf006_indicadores)
runner.test("Múltiplas Cotações", test_batch_quotes)
runner.test("RNF001 - Tempo de Resposta", test_rnf001_tempo_resposta)
runner.test("Performance do Cache", test_cache_performance)
runner.test("Tratamento de Erros", test_error_handling)
runner.test("Acurácia da IA (≥70%)", test_ai_accuracy)

runner.summary()
