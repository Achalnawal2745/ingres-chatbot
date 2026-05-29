from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import json
import os

load_dotenv()

extractor_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)

EXTRACT_PROMPT = """You are an entity extractor for a groundwater information system.

Extract the following from the user query and return ONLY valid JSON, nothing else:
- district: district name mentioned (or null)
- state: state name mentioned (or null)
- category: one of [Safe, Semi-Critical, Critical, Over-Exploited] if mentioned (or null)
- year: year mentioned like 2022, 2020 (or null)
- intent: one of [recharge, extraction, category_status, comparison, general_info, show_chart, show_map]

Examples:
Query: "What is the groundwater status of Jalgaon district?"
Output: {"district": "Jalgaon", "state": null, "category": null, "year": null, "intent": "category_status"}

Query: "Show recharge trend for Punjab in 2022"
Output: {"district": null, "state": "Punjab", "category": null, "year": "2022", "intent": "recharge"}

Query: "Which districts are over-exploited in Rajasthan?"
Output: {"district": null, "state": "Rajasthan", "category": "Over-Exploited", "year": null, "intent": "category_status"}

Query: "Show me a chart of extraction levels"
Output: {"district": null, "state": null, "category": null, "year": null, "intent": "show_chart"}

Query: "Show groundwater map of India"
Output: {"district": null, "state": null, "category": null, "year": null, "intent": "show_map"}

Now extract from this query:
"""

def extract_entities(query):
    try:
        result = extractor_llm.invoke([HumanMessage(content=EXTRACT_PROMPT + query)])
        text = result.content.strip()
        # Clean any markdown code fences if present
        text = text.replace("```json", "").replace("```", "").strip()
        entities = json.loads(text)
        print(f"[ENTITIES] {entities}")
        return entities
    except Exception as e:
        print(f"[ENTITY ERROR] {e}")
        return {
            "district": None,
            "state": None,
            "category": None,
            "year": None,
            "intent": "general_info"
        }