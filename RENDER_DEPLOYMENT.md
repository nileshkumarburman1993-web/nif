# 🚀 Deploy to Render - Configuration Guide

## ✅ Render Configuration Settings

Based on your screenshot, here's what to configure:

---

### **1. Source Code** ✅
```
Repository: nileshkumarburman1993-web/nif
Branch: main
```
✅ Already configured correctly!

---

### **2. Name**
```
nif
```
✅ Already set!

---

### **3. Language**
```
Python 3
```
✅ Already selected!

---

### **4. Branch**
```
main
```
✅ Already set!

---

### **5. Region**
```
Singapore (Southeast Asia)
```
✅ Good choice for low latency!

---

### **6. Root Directory** ⚠️ IMPORTANT
```
backend
```
**Change from:** (empty)  
**Change to:** `backend`

This tells Render to run commands from the backend folder.

---

### **7. Build Command** ⚠️ IMPORTANT
```
pip install -r requirements.txt
```
✅ Already correct!

---

### **8. Start Command** ⚠️ CRITICAL
**Current (Wrong):**
```
gunicorn your_application_wsgi
```

**Change to:**
```
gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
```

Or simpler:
```
python app.py
```

---

## 🔧 Complete Configuration

| Setting | Value |
|---------|-------|
| **Name** | `nif` |
| **Language** | `Python 3` |
| **Branch** | `main` |
| **Region** | `Singapore (Southeast Asia)` |
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app` |

---

## 🔐 Environment Variables

After creating the service, add these environment variables:

Click "Environment" tab and add:

```
ANGEL_API_KEY=your_actual_api_key
ANGEL_CLIENT_ID=your_actual_client_id
ANGEL_PASSWORD=your_actual_password
ANGEL_TOTP_SECRET=your_actual_totp_secret

PCR_BULLISH=0.65
PCR_BEARISH=1.35
MAX_PAIN_THRESHOLD=100
CAPITAL_PER_TRADE=50000
RISK_PERCENT=2
PROFIT_TARGET=0.70
STOP_LOSS=0.30
MAX_POSITIONS=5
MAX_LOSS_PER_DAY=5000
DEFAULT_QUANTITY=25
DEFAULT_SYMBOL=BANKNIFTY
```

---

## 📝 Step-by-Step Deployment

### Step 1: Update Root Directory
Change **Root Directory** from empty to:
```
backend
```

### Step 2: Update Start Command
Change **Start Command** to:
```
python app.py
```

### Step 3: Click "Create Web Service"

### Step 4: Wait for Build
- Render will install dependencies
- Should take 2-3 minutes

### Step 5: Add Environment Variables
- Go to "Environment" tab
- Add all the variables listed above
- Click "Save Changes"

### Step 6: Service Restarts
- App will automatically restart with new variables

---

## 🎯 After Deployment

Your app will be available at:
```
https://nif.onrender.com
```

Or similar Render URL.

---

## ⚠️ Important Notes

### **Port Binding**
Render provides `$PORT` environment variable. Update `app.py` to use it:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

### **Production Mode**
Set `debug=False` for production.

---

## 🔧 Troubleshooting

### Issue: "Module not found"
- Check Root Directory is set to `backend`
- Verify requirements.txt is in backend folder

### Issue: "Port binding failed"
- Make sure Start Command includes `--bind 0.0.0.0:$PORT`
- Or use `port = int(os.environ.get('PORT', 5000))`

### Issue: "Login failed"
- Check Environment Variables are set correctly
- Verify TOTP secret is correct

---

## 📊 Expected Deployment Flow

```
1. Push to GitHub ✅
2. Render detects push ✅
3. Runs build command ✅
4. Installs dependencies ✅
5. Runs start command ✅
6. App is live! ✅
```

---

## 🚀 Quick Summary

**Change these settings:**

1. **Root Directory:** `backend`
2. **Start Command:** `python app.py`
3. Click **"Create Web Service"**
4. Add **Environment Variables**
5. Done! 🎉

---

## ✅ Checklist Before Deploy

- [ ] Root Directory = `backend`
- [ ] Start Command = `python app.py`
- [ ] All environment variables ready
- [ ] Code pushed to GitHub
- [ ] Ready to click "Create Web Service"

---

**Ready to deploy? Update those settings and click Create! 🚀**
