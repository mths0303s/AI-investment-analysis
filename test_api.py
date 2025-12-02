import requests

API_URL = "http://localhost:5001/api"

# Testa status
response = requests.get(f"{API_URL}/status")
print("Status:", response.json())

# Testa cotação em tempo real
symbol = "AAPL"
response = requests.get(f"{API_URL}/quote/{symbol}")
print(f"Cotação {symbol}:", response.json())

# Testa recomendação IA
response = requests.get(f"{API_URL}/recommendation/{symbol}")
print(f"Recomendação {symbol}:", response.json())
