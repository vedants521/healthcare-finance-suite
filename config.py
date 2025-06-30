# Configuration file for the Healthcare Finance Innovation Suite

# OpenAI API Configuration (for AI narratives)
# Get your API key from https://platform.openai.com/api-keys
OPENAI_API_KEY = "your-api-key-here"  # Replace with actual key for production

# Application Settings
APP_TITLE = "Healthcare Finance Innovation Suite"
APP_SUBTITLE = "Integrated Financial Intelligence Platform"

# Feature Flags
ENABLE_AI_NARRATIVES = False  # Set to True when you add OpenAI API key
ENABLE_EMAIL_ALERTS = False   # Future enhancement

# Data Refresh Settings
DATA_REFRESH_INTERVAL = 24  # hours

# Department List
DEPARTMENTS = [
    "Cardiology",
    "Primary Care", 
    "Gastroenterology",
    "Orthopedics",
    "Pediatrics",
    "Emergency",
    "Surgery",
    "Radiology"
]

# KPI Thresholds
BUDGET_VARIANCE_THRESHOLD = 0.05  # 5%
OVERTIME_THRESHOLD = 0.10  # 10% of regular hours
NO_SHOW_THRESHOLD = 0.15  # 15%