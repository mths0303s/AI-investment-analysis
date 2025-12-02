# backend_api.py
"""
Sistema de Análise de Investimentos - Backend API
Equipe: Mateus Lima, Matheus Araújo, Udiel, Kauã Fernandes
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)

# Configuração de APIs
API_KEY = "31VV4Z306WMHPIKI"
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Sessão com retry
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

class MarketDataAPI:
    """Gerenciador de dados do mercado"""
    
    @staticmethod
    def get_stock_data(symbol, outputsize='compact'):
        """Busca dados históricos de ações"""
        cache_file = f"{CACHE_DIR}/{symbol}_{outputsize}.json"
        
        # Cache de 5 minutos
        if os.path.exists(cache_file):
            file_time = os.path.getmtime(cache_file)
            if datetime.now().timestamp() - file_time < 300:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize={outputsize}&datatype=json"
        
        try:
            response = session.get(url, timeout=10)
            data = response.json()
            
            # Cache dos dados
            with open(cache_file, 'w') as f:
                json.dump(data, f)
            
            return data
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_realtime_quote(symbol):
        """Cotação em tempo real"""
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        
        try:
            response = session.get(url, timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_technical_indicators(symbol, indicator='RSI', interval='daily'):
        """Indicadores técnicos"""
        url = f"https://www.alphavantage.co/query?function={indicator}&symbol={symbol}&interval={interval}&time_period=14&series_type=close&apikey={API_KEY}"
        
        try:
            response = session.get(url, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class AIRecommendationEngine:
    """Motor de recomendações baseado em IA"""
    
    @staticmethod
    def calculate_technical_indicators(df):
        """Calcula indicadores técnicos"""
        # SMA (Simple Moving Average)
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        
        # EMA (Exponential Moving Average)
        df['EMA_12'] = df['close'].ewm(span=12).mean()
        df['EMA_26'] = df['close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['Signal'] = df['MACD'].ewm(span=9).mean()
        
        # RSI (Relative Strength Index)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        
        # Volume médio
        df['Volume_MA'] = df['volume'].rolling(window=20).mean()
        
        return df
    
    @staticmethod
    def generate_recommendation(symbol):
        """Gera recomendação de compra/venda"""
        data = MarketDataAPI.get_stock_data(symbol, 'compact')
        
        if "Time Series (Daily)" not in data:
            return {"error": "Dados não disponíveis"}
        
        # Converte para DataFrame
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        # Calcula indicadores
        df = AIRecommendationEngine.calculate_technical_indicators(df)
        
        # Último registro
        latest = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Sistema de pontuação
        score = 0
        signals = []
        
        # Análise de tendência (SMA)
        if latest['close'] > latest['SMA_20'] > latest['SMA_50']:
            score += 2
            signals.append("Tendência de alta (SMA)")
        elif latest['close'] < latest['SMA_20'] < latest['SMA_50']:
            score -= 2
            signals.append("Tendência de baixa (SMA)")
        
        # MACD
        if latest['MACD'] > latest['Signal'] and previous['MACD'] <= previous['Signal']:
            score += 2
            signals.append("MACD cruzou para cima (Compra)")
        elif latest['MACD'] < latest['Signal'] and previous['MACD'] >= previous['Signal']:
            score -= 2
            signals.append("MACD cruzou para baixo (Venda)")
        
        # RSI
        if latest['RSI'] < 30:
            score += 1
            signals.append("RSI em sobrevenda")
        elif latest['RSI'] > 70:
            score -= 1
            signals.append("RSI em sobrecompra")
        
        # Bollinger Bands
        if latest['close'] < latest['BB_lower']:
            score += 1
            signals.append("Preço abaixo da banda inferior")
        elif latest['close'] > latest['BB_upper']:
            score -= 1
            signals.append("Preço acima da banda superior")
        
        # Volume
        if latest['volume'] > latest['Volume_MA'] * 1.5:
            signals.append("Volume acima da média")
        
        # Decisão final
        if score >= 3:
            recommendation = "COMPRA FORTE"
            confidence = min(90, 60 + score * 5)
        elif score >= 1:
            recommendation = "COMPRA"
            confidence = min(75, 55 + score * 5)
        elif score <= -3:
            recommendation = "VENDA FORTE"
            confidence = min(90, 60 + abs(score) * 5)
        elif score <= -1:
            recommendation = "VENDA"
            confidence = min(75, 55 + abs(score) * 5)
        else:
            recommendation = "MANTER"
            confidence = 50
        
        return {
            "symbol": symbol,
            "recommendation": recommendation,
            "confidence": confidence,
            "score": score,
            "signals": signals,
            "current_price": float(latest['close']),
            "rsi": float(latest['RSI']),
            "macd": float(latest['MACD']),
            "timestamp": datetime.now().isoformat()
        }

# ==================== ROTAS DA API ====================

@app.route('/api/status', methods=['GET'])
def status():
    """Status da API"""
    return jsonify({"status": "online", "version": "1.0.0"})

@app.route('/api/quote/<symbol>', methods=['GET'])
def get_quote(symbol):
    """RF001: Cotação em tempo real"""
    data = MarketDataAPI.get_realtime_quote(symbol)
    return jsonify(data)

@app.route('/api/historical/<symbol>', methods=['GET'])
def get_historical(symbol):
    """RF002: Dados históricos para gráficos"""
    outputsize = request.args.get('outputsize', 'compact')
    data = MarketDataAPI.get_stock_data(symbol, outputsize)
    return jsonify(data)

@app.route('/api/recommendation/<symbol>', methods=['GET'])
def get_recommendation(symbol):
    """RF003: Recomendação de IA"""
    recommendation = AIRecommendationEngine.generate_recommendation(symbol)
    return jsonify(recommendation)

@app.route('/api/batch-quotes', methods=['POST'])
def batch_quotes():
    """Múltiplas cotações de uma vez"""
    symbols = request.json.get('symbols', [])
    results = {}
    
    for symbol in symbols:
        data = MarketDataAPI.get_stock_data(symbol)
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            latest_date = sorted(time_series.keys(), reverse=True)[0]
            results[symbol] = {
                "price": float(time_series[latest_date]["4. close"]),
                "date": latest_date
            }
        else:
            results[symbol] = {"error": "Dados não disponíveis"}
    
    return jsonify(results)

@app.route('/api/indicators/<symbol>', methods=['GET'])
def get_indicators(symbol):
    """RF006: Indicadores técnicos"""
    indicator = request.args.get('indicator', 'RSI')
    data = MarketDataAPI.get_technical_indicators(symbol, indicator)
    return jsonify(data)

if __name__ == '__main__':
    print("🚀 Sistema de Análise de Investimentos iniciado")
    print("📊 API rodando em http://localhost:5001")
    app.run(debug=True, use_reloader=False, port=5001, host="127.0.0.1")

