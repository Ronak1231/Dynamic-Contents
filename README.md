# 🚀 AI Marketing Suite – Dynamic Contents  

An advanced AI-powered **Streamlit application** that generates a complete, long-form **marketing kit** for any product. The suite integrates **Google Gemini Pro** for AI content generation and **Google Custom Search API** for high-quality product imagery. It includes **secure user authentication**, **persistent content history**, and a clean **tabbed interface** to manage and view your marketing content.  

---

## ✨ Features  

- 🔑 **User Authentication** – Secure login & registration system with SQLite.  
- 📝 **Long-Form AI Content Generation** – Creates 500+ word professional marketing copy.  
- 🖼️ **Dynamic Image Search** – Fetches product-relevant images using Google Custom Search API.  
- 📂 **Persistent History** – Save and manage generated content per user.  
- 🎨 **Customizable Content** – Control tone, audience, and CTA through the sidebar.  
- 📑 **Tabbed UI** – Clean layout for organized viewing of marketing kits.  

---

## 🛠️ Tech Stack  

- **Frontend:** Streamlit  
- **AI Model:** Google Gemini 1.5 Pro  
- **Image Search:** Google Custom Search API  
- **Database:** SQLite  
- **Language:** Python  

---

## 📂 Project Structure  

```
/AI-Marketing-Suite
│
├── .streamlit/
│   └── secrets.toml         # Stores API keys (ignored by Git)
│
├── .gitignore               # Ignore secrets & DB from repo
├── app.py                   # Main Streamlit app
├── database.py              # SQLite DB handling
├── marketing_content.db      # SQLite DB file (auto-created on first run)
├── requirements.txt         # Dependencies
├── README.md                # Documentation
└── venv/                    # Virtual environment (ignored by Git)
```

---

## ⚙️ Setup & Installation  

### 1️⃣ Clone Repository  
```bash
git clone https://github.com/Ronak1231/Dynamic-Contents.git
cd Dynamic-Contents
```

### 2️⃣ Create Virtual Environment  
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys (**Important**)  
Create `.streamlit/secrets.toml` and add:  

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
GOOGLE_CUSTOM_SEARCH_API_KEY = "YOUR_GOOGLE_SEARCH_API_KEY_HERE"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID_HERE"
```

---

## 🔑 Getting API Keys  

### A. Gemini API Key  
1. Go to [Google AI Studio](https://aistudio.google.com/).  
2. Sign in → **Get API Key** → Create a new key.  
3. Copy & paste it into `secrets.toml`.  

### B. Google Custom Search API Key & Search Engine ID  
1. Go to [Google Cloud Console](https://console.cloud.google.com/).  
2. Create/select a project → Enable **Custom Search API**.  
3. Go to **APIs & Services > Credentials** → Create API key.  
4. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/).  
5. Create a search engine → Enable **Image Search** → Copy **Search Engine ID**.  

---

## ▶️ Running the Application  

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).  

---

## 📖 Usage  

1. **Register** for a new account in the sidebar.  
2. **Login** with your credentials.  
3. Enter **product details** and customize tone, target audience, and CTA.  
4. Click **Generate Full Marketing Kit**.  
5. View generated **content & images** in a tabbed interface.  
6. Access all past work in **My Content History**.  

---

## 🔒 Security Notes  

- `.gitignore` ensures `.streamlit/` and `marketing_content.db` are **never pushed to GitHub**.  
- Keep your API keys private – never commit `secrets.toml`.  

---

## 📜 License  

This project is licensed under the **MIT License** – feel free to modify and distribute.  
