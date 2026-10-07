from flask import Flask, render_template, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)

from rag_pipeline import get_retriever
from translator import (
    translate_to_english,
    translate_from_english,
)

from chart_data import get_chart_for_intent
from entity_extractor import extract_entities
from map_data import get_map_data

from dotenv import load_dotenv
import os

# ─────────────────────────────────────────────────────────────
# Load Environment Variables
# ─────────────────────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────────────────────
# Flask App
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# Gemini LLM
# ─────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3,
)

# ─────────────────────────────────────────────────────────────
# RAG Retriever (Lazy Loaded)
# ─────────────────────────────────────────────────────────────
_retriever = None

def get_rag_retriever():
    global _retriever
    if _retriever is None:
        try:
            print("[RAG] Initializing retriever...")
            _retriever = get_retriever()
        except Exception as e:
            print(f"[RAG ERROR] Failed to load retriever: {e}")
            return None
    return _retriever

# ─────────────────────────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert assistant for the INGRES groundwater portal of India.

INGRES is India's Ground Water Resource Estimation System
maintained by CGWB (Central Ground Water Board).

You help users understand:
- Groundwater recharge and extraction levels
- Assessment categories:
  Safe, Semi-Critical, Critical, Over-Exploited
- Block, Mandal, and Taluk level groundwater data
- State-wise groundwater statistics
- Groundwater policies and management

You will be given CONTEXT extracted from official
CGWB documents.

Always prioritize the CONTEXT when answering.

If the context contains the answer:
- Use it directly
- Cite it clearly

If not:
- Use general knowledge
- Mention that the answer is not directly available

Format responses using markdown:
- Use headings
- Use bullet points
- Use bold text for important values
- Keep responses concise and accurate
"""

# ─────────────────────────────────────────────────────────────
# Greeting Detector
# ─────────────────────────────────────────────────────────────
def is_greeting(text):

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "hlo",
        "helo",
        "howdy",
        "good morning",
        "good afternoon",
        "good evening",
        "namaste",
        "namaskar",
        "sat sri akal",
        "kem cho",
        "vanakkam",
        "nomoshkar",
        "sup",
        "what's up",
        "whats up",
        "how are you",
        "how are you?",
        "how are you doing",
        "how r u",
        "who are you",
        "who are you?"
    ]

    cleaned_text = text.lower().strip().replace("?", "")

    return (
        cleaned_text in greetings
        or any(cleaned_text == g.replace("?", "") for g in greetings)
        or len(cleaned_text) < 4
    )

# ─────────────────────────────────────────────────────────────
# Home Route
# ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─────────────────────────────────────────────────────────────
# Chat Route
# ─────────────────────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():

    try:

        # ─────────────────────────────────────────
        # Get Request Data
        # ─────────────────────────────────────────
        data = request.get_json()

        user_message = data.get("message", "").strip()
        history = data.get("history", [])

        if not user_message:
            return jsonify({
                "error": "Empty message"
            }), 400

        # ─────────────────────────────────────────
        # Translate User Message
        # ─────────────────────────────────────────
        english_message, detected_lang = (
            translate_to_english(user_message)
        )

        print(
            f"[LANG] {detected_lang} → {english_message}"
        )

        # ─────────────────────────────────────────
        # Greeting Handling
        # ─────────────────────────────────────────
        if is_greeting(english_message):

            greeting_response = """
Hello! 👋 Welcome to the **INGRES Groundwater Assistant**

I can help you with:

- 💧 Groundwater recharge data
- 📊 Extraction statistics
- 🗺️ Groundwater maps
- 📈 Historical trends and charts
- 🏷️ Category information
  (Safe, Critical, Over-Exploited)

Ask me anything about India's groundwater resources.
"""

            return jsonify({
                "response": greeting_response,
                "sources": [],
                "detected_language": detected_lang,
                "chart": None,
                "show_map": False,
                "entities": {}
            })

        # ─────────────────────────────────────────
        # Retrieve Documents from ChromaDB
        # ─────────────────────────────────────────
        retriever_instance = get_rag_retriever()
        if retriever_instance:
            try:
                docs = retriever_instance.invoke(english_message)
            except Exception as e:
                print(f"[RAG INVOKE ERROR] {e}")
                docs = []
        else:
            docs = []

        context = "\n\n".join([
            d.page_content for d in docs
        ])

        # ─────────────────────────────────────────
        # Build Sources List
        # ─────────────────────────────────────────
        sources = []

        for d in docs:

            src = d.metadata.get("source", "")
            page = d.metadata.get("page", "")

            if src:

                filename = os.path.basename(src)

                if page != "":
                    label = (
                        f"{filename} p.{int(page) + 1}"
                    )
                else:
                    label = filename

                if label not in sources:
                    sources.append(label)

        # ─────────────────────────────────────────
        # Extract Entities
        # ─────────────────────────────────────────
        entities = extract_entities(
            english_message
        )

        intent = entities.get(
            "intent",
            "general_info"
        )

        # ─────────────────────────────────────────
        # Generate Charts / Maps
        # ─────────────────────────────────────────
        chart = get_chart_for_intent(
            intent,
            entities
        )

        show_map = (
            intent == "show_map"
        )

        # ─────────────────────────────────────────
        # Build Conversation History
        # ─────────────────────────────────────────
        messages = [
            SystemMessage(content=SYSTEM_PROMPT)
        ]

        # Include last 6 messages
        for h in history[-6:]:

            if h["role"] == "user":
                messages.append(
                    HumanMessage(
                        content=h["content"]
                    )
                )

            elif h["role"] == "assistant":
                messages.append(
                    AIMessage(
                        content=h["content"]
                    )
                )

        # ─────────────────────────────────────────
        # Final Prompt
        # ─────────────────────────────────────────
        full_prompt = f"""
CONTEXT FROM OFFICIAL CGWB DOCUMENTS:

{context}

USER QUESTION:
{english_message}

Answer using the context above.

Rules:
- Use markdown formatting
- Be concise
- Mention clearly if information
  is unavailable in context
"""

        messages.append(
            HumanMessage(content=full_prompt)
        )

        # ─────────────────────────────────────────
        # Gemini Response
        # ─────────────────────────────────────────
        result = llm.invoke(messages)

        english_response = result.content

        print(
            f"[GEMINI] Response Generated"
        )

        # ─────────────────────────────────────────
        # Translate Back
        # ─────────────────────────────────────────
        final_response = (
            translate_from_english(
                english_response,
                detected_lang
            )
        )

        # ─────────────────────────────────────────
        # Final JSON Response
        # ─────────────────────────────────────────
        return jsonify({
            "response": final_response,
            "sources": sources,
            "detected_language": detected_lang,
            "chart": chart,
            "show_map": show_map,
            "entities": entities
        })

    except Exception as e:

        print(f"[ERROR] {str(e)}")

        return jsonify({
            "response": f"Server error: {str(e)}",
            "sources": [],
            "detected_language": "en",
            "chart": None,
            "show_map": False,
            "entities": {}
        }), 500

# ─────────────────────────────────────────────────────────────
# Health Route
# ─────────────────────────────────────────────────────────────
@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "model": "gemini-2.5-flash",
        "rag": "enabled",
        "multilingual": "enabled",
        "charts": "enabled"
    })

# ─────────────────────────────────────────────────────────────
# Map Data Route
# ─────────────────────────────────────────────────────────────
@app.route("/map-data")
def map_data():

    return jsonify(
        get_map_data()
    )

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/gis-maps")
def gis_maps():
    return render_template("gis_maps.html")

@app.route("/about")
def about():
    return render_template("about.html")
# ─────────────────────────────────────────────────────────────
# Run Flask App
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    )