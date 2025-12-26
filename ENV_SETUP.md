# AI Platform Interview - Environment Setup Guide

This project consists of three main components: **Frontend**, **Backend**, and **Python Modules**. Each requires specific environment variables to function properly.

## 📋 Quick Setup

### 1. Backend Setup
```bash
cd backend
cp sample.env .env
# Edit .env and add your actual values
npm install
npm start
```

**Required Environment Variables:**
- `PORT` - Server port (default: 3000)
- `MONGODB_URI` - MongoDB connection string
- `GOOGLE_GENAI_API_KEY` - Google Generative AI API key

### 2. Frontend Setup
```bash
cd frontend
cp sample.env .env
# Edit .env and add your actual values
npm install
npm run dev
```

**Required Environment Variables:**
- `VITE_VAPI_API_KEY` - Vapi AI API key
- `VITE_VAPI_ASSISTANT_ID` - Vapi AI Assistant ID
- `VITE_GROQ_API` - Groq API key

### 3. Python Modules Setup
```bash
cd pythonModules
cp sample.env .env
# Edit .env and add your actual values
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Required Environment Variables:**
- `GROQ_API_KEY` - Groq API key for document parsing

## 🔑 Getting API Keys

### MongoDB
- Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster and get your connection string

### Google Generative AI
- Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Vapi AI
- Sign up at [Vapi.ai](https://vapi.ai/)
- Get your API key and Assistant ID from the dashboard

### Groq
- Sign up at [Groq Console](https://console.groq.com/)
- Generate an API key from the keys section

## ⚠️ Important Notes

- **Never commit `.env` files** - They contain sensitive information
- Use `sample.env` files as templates
- Each component has its own `sample.env` file
- Make sure to activate the Python virtual environment before running Python modules

## 📁 Project Structure

```
aiPlatformInterview/
├── backend/
│   ├── sample.env          # Backend environment template
│   └── .env               # Your actual backend config (git-ignored)
├── frontend/
│   ├── sample.env          # Frontend environment template
│   └── .env               # Your actual frontend config (git-ignored)
└── pythonModules/
    ├── sample.env          # Python environment template
    └── .env               # Your actual Python config (git-ignored)
```
