# app.py
import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import io
import requests
from googleapiclient.discovery import build
import database as db
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Marketing Suite",
    page_icon="🚀",
    layout="wide"
)

# --- API Configuration & Models ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # --- FINAL CHANGE: Using the best free-tier model for deployment ---
    text_model = genai.GenerativeModel("gemini-1.5-flash-latest") 
    GOOGLE_API_KEY = st.secrets["GOOGLE_CUSTOM_SEARCH_API_KEY"]
    SEARCH_ENGINE_ID = st.secrets["SEARCH_ENGINE_ID"]
except Exception as e:
    st.error(f"API Key Error: {e}. Check your Streamlit secrets.", icon="🔑")
    st.stop()


# --- HELPER FUNCTIONS ---

def fetch_web_image(query):
    """Fetches a relevant image URL from Google Custom Search."""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(
            q=f"{query} product marketing image",
            cx=SEARCH_ENGINE_ID,
            searchType='image',
            num=1,
            imgSize='LARGE',
            safe='high'
        ).execute()
        
        if 'items' in res and len(res['items']) > 0:
            return res['items'][0]['link']
    except Exception as e:
        st.warning(f"Could not fetch web image due to: {e}. Using default background.")
        return None

def prepare_web_image(image_url):
    """Downloads a web image and prepares it for display, preserving aspect ratio."""
    try:
        if image_url:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img = Image.open(response.raw)
        else:
            raise ValueError("No image URL provided")
    except (requests.exceptions.RequestException, ValueError, IOError):
        img = Image.new('RGB', (1200, 675), color=(20, 20, 40))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            font = ImageFont.load_default()
        draw.text((300, 300), "Image Not Available", font=font, fill="white")

    max_width = 1080
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    
    img = img.resize((new_width, new_height))

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# --- USER AUTHENTICATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['user_id'] = None

menu_choice = st.sidebar.selectbox("Menu", ["Login", "Register"])

if not st.session_state['logged_in']:
    if menu_choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = db.check_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = user['username']
                st.session_state['user_id'] = user['id']
                st.rerun()
            else:
                st.error("Incorrect username or password.")
    
    elif menu_choice == "Register":
        st.subheader("Create a New Account")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        if st.button("Register"):
            if db.add_user(new_username, new_password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists.")

# --- MAIN APPLICATION LOGIC (IF LOGGED IN) ---
if st.session_state['logged_in']:
    st.sidebar.success(f"Logged in as **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['user_id'] = None
        st.rerun()

    st.sidebar.header("Content Customization")
    tone = st.sidebar.selectbox("Select a Tone:", ("Professional & Authoritative", "Friendly & Inspiring", "Witty & Bold", "Minimalist & Modern"))
    audience = st.sidebar.text_input("Target Audience:", placeholder="e.g., 'Enterprise CTOs, developers'")
    cta = st.sidebar.text_input("Call to Action:", placeholder="e.g., 'Request a personalized demo'")

    app_mode = st.sidebar.selectbox("Choose a tool", ["Marketing Content Generator", "My Content History"])

    if app_mode == "Marketing Content Generator":
        st.title("🚀 AI Marketing Suite")
        st.markdown("Your strategic partner for generating in-depth, professional marketing content.")
        
        product_name = st.text_input("Product Name:", placeholder="e.g., 'Microsoft Copilot Studio'")
        product_desc = st.text_area("Product Description:", placeholder="e.g., 'A unified conversational AI platform for building custom copilots.'")
        uploaded_image = st.file_uploader("Upload Product Image (for context)", type=["jpg", "jpeg", "png"])

        if st.button("✨ Generate Full Marketing Kit", type="primary"):
            if not product_name:
                st.warning("Please provide a product name.")
            else:
                st.toast(f"Generating premium content for {product_name}...", icon="🧠")
                with st.spinner("AI is crafting your long-form content... This may take a moment. 🪄"):
                    # --- MASTER PROMPT V4.1: Optimized for Flash Model ---
                    prompt = f"""
                    **Persona:** You are a Senior Product Marketing Manager at a leading enterprise software company. You specialize in creating long-form, in-depth, and highly persuasive content for a sophisticated technical and business audience. Your goal is to educate, build trust, and drive consideration.

                    **Task:** Generate an extremely elaborate and detailed marketing kit. Each of the following sections must be **at least 500 words long**. You must invent a plausible, detailed case study for a fictional company (e.g., a global logistics firm named 'OmniCargo' or a retail bank named 'FinSecure Bank') and weave it throughout all content pieces as a concrete example. You must incorporate recent (late 2025) features and positive points.

                    **Product Details:**
                    - Name: {product_name}
                    - Description: {product_desc}

                    **Creative Brief:**
                    - Tone: {tone}
                    - Target Audience: {audience}
                    - Call to Action: {cta}

                    **Output Requirements:**
                    Generate two distinct components, separated by '--- MARKETING TEXT KIT ---'.

                    **Component 1: The Strategic Headline**
                    A short, powerful headline that frames the product's strategic importance.

                    **Component 2: The Elaborate Marketing Text Kit (Each section > 500 words)**
                    - `## 📢 Ad Copy & Talking Points`: This is not just ad copy. First, write two sophisticated ad variations (long-form for platforms like LinkedIn ads). Then, create a detailed list of "Key Talking Points" for a sales team, elaborating on each point with benefits and potential customer questions.
                    - `## 💼 LinkedIn Article`: This is a full-length LinkedIn article, not a post. It should have a compelling title. Structure it with an introduction that outlines a major industry problem, several body paragraphs that explain how Copilot Studio's specific features (e.g., plugin architecture, generative answers from enterprise data, multi-lingual support, process automation) solve this problem, a detailed section dedicated to the invented case study, and a concluding paragraph that summarizes the strategic value and includes the Call to Action.
                    - `## 📧 Executive Email Briefing`: This is a long-form email designed as an executive briefing.
                        - **Subject Line:** Must be highly professional and strategic.
                        - **Body:** Begin with an executive summary. Follow with sections titled "The Challenge," "The Strategic Solution," "In Practice: The [Fictional Company Name] Case Study," and "Next Steps." Each section must be detailed, using business-centric language and focusing on ROI, security, and scalability. Elaborate on governance and administration features that would appeal to a CTO or IT manager.
                    - `## 📱 Social Media Deep Dive`: This is a campaign outline for social media.
                        - **Platform:** Focus on a professional platform like Twitter/X or a corporate blog.
                        - **Format:** Outline a 5-part "deep dive" series. For each part, write a detailed post (200+ words each) that explores a specific facet of the product (e.g., Part 1: The Power of Plugins, Part 2: Generative Answers on Your Own Data, etc.). Include the case study details where relevant. Provide hashtags for the entire series.
                    """
                    
                    try:
                        image_context = Image.open(uploaded_image) if uploaded_image else None
                        model_input = [prompt, image_context] if image_context else [prompt]
                        response = text_model.generate_content(model_input)
                        
                        parts = response.text.split("--- MARKETING TEXT KIT ---")
                        quote = parts[0].strip().replace("*", "")
                        marketing_text = parts[1].strip() if len(parts) > 1 else "No marketing text generated."

                        st.subheader("Suggested Headline")
                        st.markdown(f"> ## *{quote}*")

                        st.subheader("Generated Social Media Image")
                        web_image_url = fetch_web_image(product_name)
                        prepared_image_buffer = prepare_web_image(web_image_url)
                        st.image(prepared_image_buffer)
                        
                        st.subheader("Generated Marketing Text Kit")
                        sections = re.split(r'(## .*\n)', marketing_text)
                        
                        if len(sections) > 1:
                            content_dict = {}
                            for i in range(1, len(sections), 2):
                                title = sections[i].replace('## ', '').strip()
                                content = sections[i+1].strip()
                                content_dict[title] = content

                            tab_titles = list(content_dict.keys())
                            tabs = st.tabs(tab_titles)

                            for i, title in enumerate(tab_titles):
                                with tabs[i]:
                                    st.markdown(content_dict[title])
                        
                        db.save_content(st.session_state['user_id'], product_name, marketing_text, quote)
                        st.success("Long-form content generated and saved to your history!")

                    except Exception as e:
                        st.error(f"An error occurred during generation: {e}")

    elif app_mode == "My Content History":
        st.title("📚 My Saved Content")
        history = db.get_user_content(st.session_state['user_id'])
        if not history:
            st.info("You haven't saved any content yet.")
        else:
            for item in history:
                with st.expander(f"**{item['product_name']}** - {item['timestamp']}"):
                    st.subheader("Generated Quote")
                    st.write(item['image_prompt'])
                    st.subheader("Marketing Text Kit")
                    st.markdown(item['generated_text'])