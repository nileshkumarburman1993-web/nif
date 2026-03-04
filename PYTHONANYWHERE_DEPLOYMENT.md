# 🚀 PythonAnywhere Deployment Guide

## ✅ Step-by-Step Instructions

### **Step 1: Open Bash Console**

1. PythonAnywhere Dashboard pe jao
2. **">>> Python"** dropdown pe click karo
3. **"$ Bash"** select karo
4. New bash console khulega

---

### **Step 2: Clone Your GitHub Repo**

Bash console me yeh commands run karo:

```bash
# Clone your repository
git clone https://github.com/nileshkumarburman1993-web/nif.git

# Go to project directory
cd nif

# Check if files are there
ls -la
```

**Expected Output:**
```
backend/
frontend/
requirements.txt
README.md
...
```

---

### **Step 3: Create Virtual Environment**

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 nif-trading

# Activate it (should auto-activate)
workon nif-trading

# Install dependencies
cd backend
pip install -r requirements.txt
```

**Wait 2-3 minutes for installation**

---

### **Step 4: Setup Web App**

1. Dashboard pe wapas jao (new tab me)
2. **"Web"** tab pe click karo
3. **"Add a new web app"** button pe click karo
4. Domain choose karo: `nileshkumarburman.pythonanywhere.com`
5. Framework: **"Manual configuration"** select karo
6. Python version: **"Python 3.10"** select karo
7. **Next** → **Finish**

---

### **Step 5: Configure WSGI File**

Web tab me:

1. **"WSGI configuration file"** link pe click karo (blue link)
2. Purana code **delete** karo
3. Yeh code paste karo:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/nileshkumarburman/nif/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['ANGEL_API_KEY'] = 'your_api_key_here'
os.environ['ANGEL_CLIENT_ID'] = 'your_client_id_here'
os.environ['ANGEL_PASSWORD'] = 'your_password_here'
os.environ['ANGEL_TOTP_SECRET'] = 'your_totp_secret_here'

# Import Flask app
from app import app as application
```

4. **Save** karo (Ctrl+S)

---

### **Step 6: Configure Virtual Environment**

Web tab me scroll karo:

1. **"Virtualenv"** section dhundo
2. Path enter karo: `/home/nileshkumarburman/.virtualenvs/nif-trading`
3. Checkmark confirm karo

---

### **Step 7: Configure Static Files**

Web tab me **"Static files"** section me:

| URL | Directory |
|-----|-----------|
| `/` | `/home/nileshkumarburman/nif/frontend` |

Add karo.

---

### **Step 8: Reload Web App**

1. Web tab ke top pe **green "Reload"** button pe click karo
2. Wait 10 seconds
3. **"nileshkumarburman.pythonanywhere.com"** link pe click karo

---

## 🎯 **Expected Result:**

Your trading dashboard should open with:
- ✅ Real-time NIFTY data
- ✅ Candle pattern prediction
- ✅ BUY/SELL signals
- ✅ All features working!

---

## ⚠️ **Important Notes:**

### **Environment Variables:**

WSGI file me apne **real Angel One credentials** dalo:
- `ANGEL_API_KEY`
- `ANGEL_CLIENT_ID`  
- `ANGEL_PASSWORD`
- `ANGEL_TOTP_SECRET`

### **Free Tier Limitations:**

- ✅ Always-on web app
- ✅ No spin-down issues (unlike Render)
- ⚠️ CPU limited to 100 seconds/day
- ⚠️ Background tasks not allowed on free tier

### **For Background Updates:**

Free tier pe background threads nahi chalenge. Iske liye:
1. Upgrade to Hacker plan ($5/month)
2. Ya manual refresh use karo

---

## 🐛 **Troubleshooting:**

### **Error: "Internal Server Error"**

1. Web tab → **Error log** dekho
2. Common issues:
   - Wrong paths in WSGI
   - Missing dependencies
   - Wrong Python version

### **Error: "Module not found"**

```bash
# Bash console me
workon nif-trading
cd /home/nileshkumarburman/nif/backend
pip install -r requirements.txt
```

### **Angel One Login Fails:**

- WSGI file me credentials check karo
- TOTP secret sahi hai confirm karo

---

## 📝 **Quick Commands:**

```bash
# Check if virtual environment is active
which python

# List installed packages
pip list

# View app logs
tail -f /var/log/nileshkumarburman.pythonanywhere.com.error.log

# Restart web app
# Go to Web tab → Reload button
```

---

## ✅ **Success Checklist:**

- [ ] Git clone successful
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] WSGI file configured
- [ ] Environment variables added
- [ ] Static files configured
- [ ] Web app reloaded
- [ ] Dashboard opens in browser
- [ ] Angel One login working
- [ ] Data showing on dashboard

---

**Your app will be live at:** `https://nileshkumarburman.pythonanywhere.com`

No caching issues, no deployment delays! 🚀
