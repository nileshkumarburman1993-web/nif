# Gunicorn configuration for production deployment
import os

# Bind to PORT provided by cloud platform (Render, Heroku, etc.)
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Worker processes
workers = 2

# Worker class
worker_class = "sync"

# Timeout
timeout = 120

# Access log
accesslog = "-"

# Error log
errorlog = "-"

# Log level
loglevel = "info"
