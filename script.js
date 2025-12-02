// Script.js
const API_URL = 'http://localhost:5001/api';
let stocks = [];
let chart = null;
let alerts = [];

// Inicializa o sistema
async function init() {
    loadStocks();
    loadAlerts();
    setInterval(updateStockPrices, 10000); // Atualiza a cada 10s (RF001)
}

// Adiciona ativo
async function addStock() {
    const symbol = document.getElementById('stock-symbol').value.trim().toUpperCase();
    if (!symbol) return;

    if (stocks.includes(symbol)) {
        showError('Ativo já adicionado!');
        return;
    }

    stocks.push(symbol);
    saveStocks();
    document.getElementById('stock-symbol').value = '';
    await updateStockPrices();
    await loadRecommendations(symbol);
    await loadChart(symbol);
}

// Atualiza preços
async function updateStockPrices() {
    if (stocks.length === 0) return;

    const listDiv = document.getElementById('stock-list');
    listDiv.innerHTML = '<div class="loading">Atualizando...</div>';

    try {
        const response = await fetch(`${API_URL}/batch-quotes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbols: stocks })
        });

        const data = await response.json();

        listDiv.innerHTML = '';
        for (const symbol of stocks) {
            const stockData = data[symbol];
            if (stockData && !stockData.error) {
                const item = document.createElement('div');
                item.className = 'stock-item';
                item.innerHTML = `
                            <div class="stock-info">
                                <div class="stock-symbol">${symbol}</div>
                                <div class="stock-price">$${stockData.price.toFixed(2)}</div>
                                <button onclick="loadRecommendations('${symbol}')">Ver Recomendação</button>
                            </div>
                            <button class="btn-danger" onclick="removeStock('${symbol}')">Remover</button>
                        `;
                listDiv.appendChild(item);

                checkAlerts(symbol, stockData.price);
            }
        }
    } catch (error) {
        showError('Erro ao atualizar preços: ' + error.message);
    }
}

// Carrega recomendações (RF003)
async function loadRecommendations(symbol) {
    const recDiv = document.getElementById('recommendations');
    recDiv.innerHTML = '<div class="loading">Analisando...</div>';

    try {
        const response = await fetch(`${API_URL}/recommendation/${symbol}`);
        const data = await response.json();

        if (data.error) {
            recDiv.innerHTML = `<div class="error">${data.error}</div>`;
            return;
        }

        const recClass = data.recommendation.toLowerCase().replace(/\s+/g, '-');
        recDiv.innerHTML = `
                    <div style="text-align: center;">
                        <h2>${symbol}</h2>
                        <div class="recommendation rec-${recClass}">${data.recommendation}</div>
                        <p style="margin-top: 10px; font-size: 18px;">Confiança: ${data.confidence}%</p>
                        <p style="margin-top: 5px;">Preço: $${data.current_price.toFixed(2)}</p>
                    </div>
                    <div style="margin-top: 20px;">
                        <h4>Sinais Detectados:</h4>
                        <ul style="list-style: none; padding: 0;">
                            ${data.signals.map(s => `<li style="padding: 5px 0;">• ${s}</li>`).join('')}
                        </ul>
                    </div>
                `;

        loadIndicators(data);
        await loadChart(symbol);
    } catch (error) {
        showError('Erro ao carregar recomendações: ' + error.message);
    }
}

// Carrega indicadores (RF006)
function loadIndicators(data) {
    const indDiv = document.getElementById('indicators');
    indDiv.innerHTML = `
                <div class="indicators">
                    <div class="indicator">
                        <div class="indicator-label">RSI</div>
                        <div class="indicator-value ${data.rsi < 30 ? 'positive' : data.rsi > 70 ? 'negative' : ''}">${data.rsi.toFixed(2)}</div>
                    </div>
                    <div class="indicator">
                        <div class="indicator-label">MACD</div>
                        <div class="indicator-value">${data.macd.toFixed(4)}</div>
                    </div>
                    <div class="indicator">
                        <div class="indicator-label">Score</div>
                        <div class="indicator-value ${data.score > 0 ? 'positive' : data.score < 0 ? 'negative' : ''}">${data.score}</div>
                    </div>
                </div>
            `;
}

// Carrega gráfico (RF002)
async function loadChart(symbol) {
    try {
        const response = await fetch(`${API_URL}/historical/${symbol}?outputsize=compact`);
        const data = await response.json();

        const timeSeries = data['Time Series (Daily)'];
        if (!timeSeries) return;

        const dates = Object.keys(timeSeries).reverse().slice(-30);
        const prices = dates.map(date => parseFloat(timeSeries[date]['4. close']));

        const ctx = document.getElementById('price-chart').getContext('2d');

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: `${symbol} - Preço de Fechamento`,
                    data: prices,
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true, labels: { color: '#fff' } }
                },
                scales: {
                    x: { ticks: { color: '#fff' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    y: { ticks: { color: '#fff' }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
    } catch (error) {
        showError('Erro ao carregar gráfico: ' + error.message);
    }
}

// Alertas (RF007)
function setAlert() {
    const symbol = document.getElementById('alert-symbol').value.trim().toUpperCase();
    const price = parseFloat(document.getElementById('alert-price').value);

    if (!symbol || !price) {
        showError('Preencha todos os campos do alerta!');
        return;
    }

    alerts.push({ symbol, price, active: true });
    saveAlerts();
    renderAlerts();

    document.getElementById('alert-symbol').value = '';
    document.getElementById('alert-price').value = '';
}

function checkAlerts(symbol, currentPrice) {
    alerts.forEach(alert => {
        if (alert.active && alert.symbol === symbol) {
            if (currentPrice >= alert.price) {
                alert.active = false;
                showAlert(`🔔 Alerta: ${symbol} atingiu $${alert.price}! Preço atual: $${currentPrice.toFixed(2)}`);
                saveAlerts();
                renderAlerts();
            }
        }
    });
}

function renderAlerts() {
    const alertsDiv = document.getElementById('alerts');
    if (alerts.length === 0) {
        alertsDiv.innerHTML = '<div style="opacity: 0.5; padding: 10px;">Nenhum alerta configurado</div>';
        return;
    }

    alertsDiv.innerHTML = alerts.map((alert, i) => `
                <div class="alert-item">
                    <strong>${alert.symbol}</strong> - Alvo: $${alert.price.toFixed(2)}
                    <span style="float: right;">${alert.active ? '🟢 Ativo' : '🔴 Disparado'}</span>
                </div>
            `).join('');
}

// Exportar relatório (RF004)
function exportReport() {
    const report = {
        timestamp: new Date().toISOString(),
        stocks: stocks,
        alerts: alerts,
        generated_by: 'Sistema de Análise de Investimentos v1.0'
    };

    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `relatorio_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
}

// Persistência local
function saveStocks() {
    localStorage.setItem('stocks', JSON.stringify(stocks));
}

function loadStocks() {
    const saved = localStorage.getItem('stocks');
    if (saved) {
        stocks = JSON.parse(saved);
        updateStockPrices();
        // Carregar recomendação do primeiro ativo automaticamente
        if (stocks.length > 0) loadRecommendations(stocks[0]);
    }
}


function removeStock(symbol) {
    stocks = stocks.filter(s => s !== symbol);
    saveStocks();
    updateStockPrices();
}

function saveAlerts() {
    localStorage.setItem('alerts', JSON.stringify(alerts));
}

function loadAlerts() {
    const saved = localStorage.getItem('alerts');
    if (saved) {
        alerts = JSON.parse(saved);
        renderAlerts();
    }
}

function showError(message) {
    const errorDiv = document.getElementById('error-container');
    errorDiv.innerHTML = `<div class="error">${message}</div>`;
    setTimeout(() => errorDiv.innerHTML = '', 5000);
}

function showAlert(message) {
    alert(message);
}

// Inicia o sistema
init();