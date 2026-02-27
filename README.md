# Trading Automation System

A comprehensive trading automation system for options trading with Angel One integration, featuring a 70% profit target strategy.

## 🚀 Features

- **Angel One API Integration**: Seamless connection with Angel One trading platform
- **NSE Option Chain Scraper**: Real-time option chain data from NSE
- **70% Strategy**: Automated trading with 70% profit target and 30% stop loss
- **Live Dashboard**: Real-time updates via WebSocket
- **Trade History**: Complete trade logging with SQLite database
- **Performance Metrics**: Track P&L, win rate, and trading statistics

## 📁 Project Structure

```
trading-automation/
│
├── backend/
│   ├── app.py                 # Main Flask app
│   ├── angel_api.py           # Angel One API integration
│   ├── option_chain.py        # NSE Option Chain scraper
│   ├── strategy.py            # 70% strategy logic
│   ├── requirements.txt       # Dependencies
│   └── config.py              # API keys
│
├── frontend/
│   ├── index.html             # Dashboard
│   ├── style.css              # Styling
│   └── script.js              # Live updates
│
└── database/
    └── trades.db              # Trade history (auto-created)
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Angel One trading account
- Angel One API credentials

### Step 1: Clone or Download

```bash
cd trading-automation
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Configure Environment

1. Copy `.env.example` to `.env`:
```bash
cp ../.env.example .env
```

2. Edit `.env` and add your Angel One credentials:
```
ANGEL_API_KEY=your_api_key_here
ANGEL_CLIENT_CODE=your_client_code_here
ANGEL_PASSWORD=your_password_here
ANGEL_TOTP_TOKEN=your_totp_token_here
```

### Step 4: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📊 Usage

### 1. Login
- Open `http://localhost:5000` in your browser
- Enter your Angel One credentials
- Click "Login"

### 2. Start Trading
- Select the symbol (NIFTY/BANKNIFTY/FINNIFTY)
- Click "Start Trading"
- The system will automatically monitor and execute trades

### 3. Monitor Performance
- View real-time positions
- Check option chain data
- Track trade history and P&L

### 4. Stop Trading
- Click "Stop Trading" to halt automated trading
- Existing positions will remain open

## ⚙️ Strategy Configuration

The 70% strategy can be configured in `config.py`:

```python
PROFIT_TARGET = 0.70  # 70% profit target
STOP_LOSS = 0.30      # 30% stop loss
DEFAULT_QUANTITY = 25 # Lot size
MAX_POSITIONS = 5     # Maximum concurrent positions
```

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- Keep your API credentials secure
- Use strong passwords
- Enable 2FA on your Angel One account

## 📝 API Endpoints

### Authentication
- `POST /api/login` - Login to Angel One

### Trading
- `POST /api/start-trading` - Start automated trading
- `POST /api/stop-trading` - Stop automated trading
- `GET /api/positions` - Get current positions

### Data
- `GET /api/option-chain/<symbol>` - Fetch option chain
- `GET /api/trade-history` - Get trade history

## 🔧 Customization

### Modify Strategy Logic

Edit `backend/strategy.py` to customize:
- Entry signals
- Exit conditions
- Risk management rules
- Position sizing

### Adjust UI

Edit `frontend/style.css` to customize the dashboard appearance.

## 📈 Performance Tracking

All trades are automatically saved to SQLite database with:
- Entry/exit prices
- P&L calculations
- Timestamps
- Order IDs
- Exit reasons

## ⚠️ Disclaimer

**This is for educational purposes only. Trading involves significant risk of loss. Use at your own risk.**

- Always test in paper trading first
- Start with small position sizes
- Monitor the system actively
- Understand the risks involved

## 🐛 Troubleshooting

### Connection Issues
- Check internet connectivity
- Verify Angel One API credentials
- Ensure TOTP token is correct

### Login Failures
- Verify API key and client code
- Check if 2FA is enabled
- Ensure password is correct

### Data Not Loading
- Check NSE website accessibility
- Verify symbol names are correct
- Check browser console for errors

## 📚 Resources

- [Angel One API Documentation](https://smartapi.angelbroking.com/docs)
- [NSE India](https://www.nseindia.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review Angel One API documentation
- Open an issue on GitHub

---

**Happy Trading! 🚀📈**
