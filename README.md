💧 INGRES AI ChatBot — Groundwater Assistant
An AI-powered virtual assistant for the India Ground Water Resource Estimation System (INGRES), built with Google Gemini, RAG pipeline, Flask, and real CGWB assessment data.

📌 Table of Contents

Overview
Features
Tech Stack
Project Structure
Installation
Usage
Pages
How RAG Works
Screenshots
Future Work
Credits


🌊 Overview
INGRES (India Ground Water Resource Estimation System) is a GIS-based web application maintained by the Central Ground Water Board (CGWB) and developed in collaboration with IIT Hyderabad. It estimates annual groundwater recharge, extractable resources, total extraction, and the stage of groundwater extraction for each assessment unit (Block/Mandal/Taluk).
This project adds an AI-driven ChatBot layer on top of INGRES that allows users to:

Query groundwater data in plain English (or regional languages)
Get instant answers from official CGWB documents via RAG
View interactive charts and maps of groundwater status
Access assessment data, reports, and GIS maps through a professional portal


✨ Features
FeatureDescription🤖 AI ChatGemini 2.5 Flash powered conversational assistant📄 RAG PipelineAnswers grounded in real CGWB PDF documents🌐 MultilingualSupports Hindi, Telugu, Tamil, Kannada, Marathi, Gujarati, Bengali, Punjabi📊 Smart ChartsBar, line, and pie charts auto-generated based on query intent🗺️ Interactive MapsLeaflet.js maps with state-level groundwater status markers🧠 Entity ExtractionAI extracts district, state, category, year, and intent from queries💬 Chat MemoryRemembers last 6 messages for contextual conversation📋 Assessment TableFilterable block/district level assessment data📑 Reports LibrarySearchable CGWB reports and publicationsℹ️ About PageTech stack, timeline, and project information

🛠️ Tech Stack
LayerTechnologyBackendPython 3.10, FlaskLLMGoogle Gemini 2.5 FlashRAGLangChain, ChromaDB, SentenceTransformersEmbeddingsall-MiniLM-L6-v2 (local, free)PDF IngestionPyPDF, LangChain Document LoadersTranslationDeep Translator, LangDetectFrontendHTML, CSS, Vanilla JavaScriptChartsChart.jsMapsLeaflet.js + OpenStreetMapEnv Managementpython-dotenv

📁 Project Structure
ingres-chatbot/
├── backend/
│   ├── app.py                  ← Main Flask application
│   ├── rag_pipeline.py         ← PDF ingestion + ChromaDB retriever
│   ├── entity_extractor.py     ← AI-based entity extraction (state, district, intent)
│   ├── chart_data.py           ← Chart data logic based on intent
│   ├── map_data.py             ← State-level groundwater map markers
│   ├── translator.py           ← Multilingual detect + translate
│   ├── check_models.py         ← Utility to list available Gemini models
│   ├── .env                    ← API keys (never commit this)
│   ├── requirements.txt        ← Python dependencies
│   ├── data/                   ← CGWB PDF documents go here
│   │   └── GWRA2022_1_HIDO.pdf
│   ├── chroma_store/           ← Auto-generated vector database
│   ├── templates/
│   │   ├── index.html          ← Dashboard + Chat UI
│   │   ├── assessment.html     ← Assessment data table
│   │   ├── reports.html        ← Reports library
│   │   ├── gis_maps.html       ← Full-screen GIS map
│   │   └── about.html          ← Project info page
│   └── static/
│       └── style.css           ← Global styles
└── frontend/                   ← (unused — replaced by Flask templates)

⚙️ Installation
Prerequisites

Python 3.10+
Google Gemini API key (free at aistudio.google.com)
Git (optional)

Step 1 — Clone or download the project
bashgit clone https://github.com/yourusername/ingres-chatbot.git
cd ingres-chatbot/backend
Step 2 — Create virtual environment
bashpython -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
Step 3 — Install dependencies
bashpip install -r requirements.txt
Step 4 — Set up environment variables
Create a .env file inside backend/:
envGEMINI_API_KEY=your_gemini_api_key_here

⚠️ Never commit your .env file. It is already in .gitignore.

Step 5 — Add CGWB PDF documents
Download official CGWB assessment reports and place them inside backend/data/:

Dynamic Ground Water Resources of India 2022
Any state-level groundwater assessment PDF

Step 6 — Run document ingestion (one time only)
bashpython -c "from rag_pipeline import ingest_documents; ingest_documents()"
You will see output like:
Found 1 PDF(s): ['GWRA2022_1_HIDO.pdf']
Loading GWRA2022_1_HIDO.pdf...
  → 420 pages loaded
Total chunks created: 1240
Done! 1240 chunks stored in ChromaDB.
Step 7 — Run the application
bashpython app.py
Open your browser at:
http://127.0.0.1:5000

🚀 Usage
Chat queries to try
QueryWhat happensWhat is the total groundwater recharge in India?RAG answers from CGWB PDFShow recharge by stateBlue bar chart renderedShow extraction trend for PunjabRed line chart renderedCompare recharge vs extraction trendTwo-line comparison chartShow groundwater map of IndiaInteractive Leaflet mapShow groundwater category statisticsPie chart of Safe/Critical/etc.Which states are over-exploited?AI answer with sourcesभारत में भूजल स्तर क्या है?Auto-detects Hindi, replies in HindiHello / NamasteFriendly greeting with feature list

📄 Pages
URLPageDescription/DashboardAI chat with sidebar stats and quick queries/assessmentAssessmentFilterable block/district data table/reportsReportsSearchable CGWB publications library/gis-mapsGIS MapsFull-screen interactive groundwater map/aboutAboutTech stack, timeline, project info

🧠 How RAG Works
User Query
    ↓
Language Detection (LangDetect)
    ↓
Translate to English (Deep Translator)
    ↓
Entity Extraction (Gemini) → district, state, category, intent
    ↓
Semantic Search (ChromaDB) → Top 4 relevant PDF chunks
    ↓
Build Prompt = System + Context + History + Question
    ↓
Gemini 2.5 Flash generates answer
    ↓
Translate response back to user language
    ↓
Return response + sources + chart + map flag

🔮 Future Work

 Connect to live INGRES portal API for real-time data
 Add block/mandal level data from CGWB database
 Voice input support (Web Speech API)
 User authentication and query history
 Export chat as PDF report
 Add more regional language support
 Docker containerization for easy deployment
 Deploy on cloud (Render / Railway / AWS)
 Add more CGWB state-level PDF documents


📦 Requirements
flask
python-dotenv
langchain
langchain-google-genai
langchain-community
langchain-text-splitters
langchain-core
langchain-huggingface
chromadb
sentence-transformers
pypdf
deep-translator
langdetect
google-generativeai
gunicorn
Install all at once:
bashpip install -r requirements.txt

🙏 Credits
OrganizationRoleCentral Ground Water Board (CGWB)Data source and assessment methodologyIIT HyderabadINGRES portal developmentGoogle DeepMindGemini 2.5 Flash LLMLangChainRAG frameworkChromaDBVector databaseLeaflet.jsInteractive mapsOpenStreetMapMap tiles

📜 License
This project is built for educational and research purposes as part of the INGRES AI ChatBot initiative under the Ministry of Jal Shakti, Government of India.

Built with ❤️ for better groundwater data accessibility in India
