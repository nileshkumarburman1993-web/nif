// Global variables
let isLoggedIn = false;
let isTradingActive = false;

// API Base URL
const API_BASE = 'http://localhost:5000';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Setup event listeners
    setupEventListeners();
    
    // Start periodic updates
    startPeriodicUpdates();
    
    // Update connection status
    updateConnectionStatus(true);
}

// Event listeners setup
function setupEventListeners() {
    // Login button
    document.getElementById('login-btn').addEventListener('click', handleLogin);
    
    // Trading controls
    document.getElementById('start-trading-btn').addEventListener('click', startTrading);
    document.getElementById('stop-trading-btn').addEventListener('click', stopTrading);
    
    // Symbol change
    document.getElementById('symbol-select').addEventListener('change', handleSymbolChange);
}

// Login handler
async function handleLogin() {
    // Disable login button during login attempt
    const loginBtn = document.getElementById('login-btn');
    loginBtn.disabled = true;
    loginBtn.textContent = 'Logging in...';
    
    try {
        const response = await fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            isLoggedIn = true;
            showTradingSection();
            showNotification('✅ Login successful!', 'success');
        } else {
            showNotification(data.message || 'Login failed', 'error');
            loginBtn.disabled = false;
            loginBtn.textContent = 'Login to Angel One';
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('❌ Login failed: ' + error.message, 'error');
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login to Angel One';
    }
}

// Start trading
async function startTrading() {
    const symbol = document.getElementById('symbol-select').value;
    
    try {
        const response = await fetch(`${API_BASE}/api/start-trading`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol })
        });
        
        const data = await response.json();
        
        if (data.success) {
            isTradingActive = true;
            updateTradingStatus(true);
            showNotification('Trading started for ' + symbol, 'success');
            
            // Enable/disable buttons
            document.getElementById('start-trading-btn').disabled = true;
            document.getElementById('stop-trading-btn').disabled = false;
        } else {
            showNotification(data.message || 'Failed to start trading', 'error');
        }
    } catch (error) {
        console.error('Start trading error:', error);
        showNotification('Failed to start trading: ' + error.message, 'error');
    }
}

// Stop trading
async function stopTrading() {
    try {
        const response = await fetch(`${API_BASE}/api/stop-trading`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            isTradingActive = false;
            updateTradingStatus(false);
            showNotification('Trading stopped', 'info');
            
            // Enable/disable buttons
            document.getElementById('start-trading-btn').disabled = false;
            document.getElementById('stop-trading-btn').disabled = true;
        } else {
            showNotification(data.message || 'Failed to stop trading', 'error');
        }
    } catch (error) {
        console.error('Stop trading error:', error);
        showNotification('Failed to stop trading: ' + error.message, 'error');
    }
}

// Handle symbol change
function handleSymbolChange() {
    if (isLoggedIn) {
        const symbol = document.getElementById('symbol-select').value;
        updateOptionChain(symbol);
    }
}

// Update positions
async function updatePositions() {
    try {
        const response = await fetch(`${API_BASE}/api/positions`);
        const data = await response.json();
        
        if (data.success && data.positions) {
            renderPositions(data.positions);
        }
    } catch (error) {
        console.error('Error updating positions:', error);
    }
}

// Render positions
function renderPositions(positions) {
    const container = document.getElementById('positions-container');
    
    if (!positions || positions.length === 0) {
        container.innerHTML = '<p class="no-data">No open positions</p>';
        return;
    }
    
    container.innerHTML = positions.map(pos => `
        <div class="position-item">
            <div class="position-header">
                <span>${pos.tradingsymbol}</span>
                <span class="${parseFloat(pos.pnl) >= 0 ? 'profit' : 'loss'}">
                    ₹${parseFloat(pos.pnl || 0).toFixed(2)}
                </span>
            </div>
            <div class="position-details">
                <div>Qty: ${pos.netqty}</div>
                <div>Avg: ₹${parseFloat(pos.averageprice || 0).toFixed(2)}</div>
                <div>LTP: ₹${parseFloat(pos.ltp || 0).toFixed(2)}</div>
            </div>
        </div>
    `).join('');
}

// Update option chain
async function updateOptionChain(symbol) {
    try {
        const response = await fetch(`${API_BASE}/api/option-chain/${symbol}`);
        const data = await response.json();
        
        if (data.success && data.data) {
            renderOptionChain(data.data);
            updateMarketOverview(data.data);
        }
    } catch (error) {
        console.error('Error updating option chain:', error);
    }
}

// Render option chain
function renderOptionChain(chainData) {
    const tbody = document.getElementById('option-chain-body');
    
    if (!chainData.options || chainData.options.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="no-data">No option data available</td></tr>';
        return;
    }
    
    tbody.innerHTML = chainData.options.slice(0, 20).map(opt => `
        <tr class="${opt.atm ? 'atm-row' : ''}">
            <td>${formatNumber(opt.ce.oi)}</td>
            <td>${formatNumber(opt.ce.volume)}</td>
            <td>₹${opt.ce.ltp.toFixed(2)}</td>
            <td>${opt.ce.iv.toFixed(2)}%</td>
            <td><strong>${opt.strike}</strong></td>
            <td>${opt.pe.iv.toFixed(2)}%</td>
            <td>₹${opt.pe.ltp.toFixed(2)}</td>
            <td>${formatNumber(opt.pe.volume)}</td>
            <td>${formatNumber(opt.pe.oi)}</td>
        </tr>
    `).join('');
}

// Update market overview
function updateMarketOverview(chainData) {
    document.getElementById('underlying-value').textContent = chainData.underlying_value.toFixed(2);
    
    // Find ATM strike
    const atmOption = chainData.options.find(opt => opt.atm);
    if (atmOption) {
        document.getElementById('atm-strike').textContent = atmOption.strike;
        document.getElementById('pcr-value').textContent = atmOption.pcr.toFixed(2);
    }
    
    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
}

// Update trade history
async function updateTradeHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/trade-history`);
        const data = await response.json();
        
        if (data.success && data.trades) {
            renderTradeHistory(data.trades);
            updatePerformanceMetrics(data.trades);
        }
    } catch (error) {
        console.error('Error updating trade history:', error);
    }
}

// Render trade history
function renderTradeHistory(trades) {
    const tbody = document.getElementById('trade-history-body');
    
    if (!trades || trades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="11" class="no-data">No trades yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = trades.map(trade => `
        <tr>
            <td>${new Date(trade.timestamp).toLocaleTimeString()}</td>
            <td>${trade.symbol}</td>
            <td>${trade.strike}</td>
            <td>${trade.option_type}</td>
            <td>${trade.side}</td>
            <td>₹${parseFloat(trade.entry_price).toFixed(2)}</td>
            <td>${trade.exit_price ? '₹' + parseFloat(trade.exit_price).toFixed(2) : '--'}</td>
            <td>${trade.quantity}</td>
            <td class="${parseFloat(trade.pnl || 0) >= 0 ? 'profit' : 'loss'}">
                ₹${parseFloat(trade.pnl || 0).toFixed(2)}
            </td>
            <td class="${parseFloat(trade.pnl_percentage || 0) >= 0 ? 'profit' : 'loss'}">
                ${parseFloat(trade.pnl_percentage || 0).toFixed(2)}%
            </td>
            <td>${trade.status}</td>
        </tr>
    `).join('');
}

// Update performance metrics
function updatePerformanceMetrics(trades) {
    if (!trades || trades.length === 0) return;
    
    const completedTrades = trades.filter(t => t.status === 'CLOSED');
    const totalPnL = completedTrades.reduce((sum, t) => sum + parseFloat(t.pnl || 0), 0);
    const winningTrades = completedTrades.filter(t => parseFloat(t.pnl || 0) > 0).length;
    const winRate = completedTrades.length > 0 ? (winningTrades / completedTrades.length) * 100 : 0;
    const avgPnL = completedTrades.length > 0 ? totalPnL / completedTrades.length : 0;
    
    document.getElementById('total-pnl').textContent = `₹${totalPnL.toFixed(2)}`;
    document.getElementById('total-pnl').className = `metric-value ${totalPnL >= 0 ? 'profit' : 'loss'}`;
    document.getElementById('win-rate').textContent = `${winRate.toFixed(1)}%`;
    document.getElementById('total-trades').textContent = completedTrades.length;
    document.getElementById('avg-pnl').textContent = `₹${avgPnL.toFixed(2)}`;
}

// Update market data from background updater
async function updateMarketData() {
    if (!isTradingActive) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/market-data`);
        const data = await response.json();
        
        if (data && !data.error) {
            // Update market overview
            if (data.current_price) {
                document.getElementById('underlying-value').textContent = data.current_price.toFixed(2);
            }
            if (data.pcr) {
                document.getElementById('pcr-value').textContent = data.pcr;
            }
            if (data.max_pain) {
                document.getElementById('atm-strike').textContent = data.max_pain;
            }
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
            
            // Update signal display (you can add a signal section in HTML)
            console.log('Signal:', data.signal);
        }
    } catch (error) {
        console.error('Error fetching market data:', error);
    }
}

// Periodic updates
function startPeriodicUpdates() {
    // Update positions and option chain every 5 seconds
    setInterval(() => {
        if (isLoggedIn) {
            updatePositions();
            
            if (isTradingActive) {
                const symbol = document.getElementById('symbol-select').value;
                updateOptionChain(symbol);
                updateMarketData(); // Get latest from background thread
            }
        }
    }, 5000);
    
    // Update trade history every 10 seconds
    setInterval(() => {
        if (isLoggedIn) {
            updateTradeHistory();
        }
    }, 10000);
}

// UI Helper functions
function showTradingSection() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('trading-section').style.display = 'block';
    document.getElementById('dashboard-grid').style.display = 'grid';
    
    // Initial data load
    updatePositions();
    updateTradeHistory();
    const symbol = document.getElementById('symbol-select').value;
    updateOptionChain(symbol);
}

function updateConnectionStatus(connected) {
    const statusBadge = document.getElementById('connection-status');
    statusBadge.textContent = connected ? 'Connected' : 'Disconnected';
    statusBadge.className = `status-badge ${connected ? 'connected' : 'disconnected'}`;
}

function updateTradingStatus(active) {
    const statusBadge = document.getElementById('trading-status');
    statusBadge.textContent = active ? 'Trading Active' : 'Trading Inactive';
    statusBadge.className = `status-badge ${active ? 'active' : 'inactive'}`;
}

function showNotification(message, type = 'info') {
    // Simple alert for now - can be enhanced with a toast library
    const prefix = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    alert(`${prefix} ${message}`);
}

function formatNumber(num) {
    if (num >= 10000000) {
        return (num / 10000000).toFixed(2) + 'Cr';
    } else if (num >= 100000) {
        return (num / 100000).toFixed(2) + 'L';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(2) + 'K';
    }
    return num.toString();
}
