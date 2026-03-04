# 🚀 Render Deployment Checklist

## ✅ Pre-Deployment (DONE)

- [x] Fixed requirements.txt (removed logzero, added selenium)
- [x] Created Procfile
- [x] Created render.yaml
- [x] Created build.sh
- [x] Verified all imports
- [x] Port configuration correct
- [x] Code pushed to GitHub

---

## 📋 Deployment Steps (DO THIS NOW)

### **Step 1: Go to Render Dashboard**
🔗 https://dashboard.render.com/

### **Step 2: Create New Web Service**
1. Click: **"New"** → **"Web Service"**
2. Connect repository: `nileshkumarburman1993-web/nif`
3. Click **"Connect"**

### **Step 3: Configure Service**

| Setting | Value |
|---------|-------|
| **Name** | `nif-trading-automation` |
| **Environment** | `Python 3` |
| **Branch** | `main` |
| **Root Directory** | (leave empty) |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && gunicorn --config gunicorn_config.py app:app` |
| **Instance Type** | Free |

### **Step 4: Add Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these **4 REQUIRED** variables:

```
ANGEL_API_KEY = your_actual_api_key_here
ANGEL_CLIENT_ID = your_actual_client_id_here  
ANGEL_PASSWORD = your_actual_password_here
ANGEL_TOTP_SECRET = your_actual_totp_secret_here
```

**Where to get these:**
- Login to Angel One
- Go to API settings
- Copy your API credentials

### **Step 5: Deploy!**

Click **"Create Web Service"**

Render will:
1. ✅ Clone your repo
2. ✅ Install dependencies (no logzero error!)
3. ✅ Start your app
4. ✅ Give you a URL

---

## ⏱️ Deployment Timeline

- **Build time**: ~2-3 minutes
- **First start**: ~30 seconds
- **URL**: `https://nif-trading-automation.onrender.com`

---

## 🧪 Testing After Deployment

### **1. Check Homepage**
Open: `https://your-app.onrender.com`

Should show: Trading dashboard with NIFTY data

### **2. Check API**
```bash
curl https://your-app.onrender.com/api/market-data
```

Should return:
```json
{
  "current_price": 24500,
  "pcr": 0.95,
  "signal": {
    "action": "BUY",
    "type": "CALL",
    "candle_prediction": {
      "pattern": "Bullish Candle",
      "direction": "BULLISH"
    }
  }
}
```

### **3. Check Logs**
In Render Dashboard → Logs

Look for:
```
✅ Angel One Login Success
🕯️ Fetching 15m candles for NIFTY
✅ Got 10 candles
🔮 Pattern: Bullish Candle
```

---

## ⚠️ Troubleshooting

### **If deployment fails:**

1. **Check Render Logs** - Look for exact error
2. **Verify Environment Variables** - All 4 Angel One variables set?
3. **Test locally first**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

### **Common Issues:**

| Error | Solution |
|-------|----------|
| "ModuleNotFoundError" | ✅ FIXED - Code pushed |
| "Angel One login failed" | Check TOTP secret is correct |
| "Port already in use" | ✅ Fixed - uses PORT env var |
| "App exits with status 1" | ✅ FIXED - logzero removed |

---

## 📊 What Will Work:

✅ Real-time NIFTY data  
✅ 15-minute candle analysis  
✅ Candlestick pattern recognition  
✅ Next candle prediction  
✅ BUY/SELL signals  
✅ Auto-refresh dashboard  
✅ Complete trading system  

---

## 🎯 After Successful Deployment:

1. ✅ Save your Render URL
2. ✅ Test the dashboard
3. ✅ Monitor for a few hours
4. ✅ Check Angel One API usage
5. ✅ Ready to trade!

---

**🚀 Your code is ready! Go deploy on Render now!**
