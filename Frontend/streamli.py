import streamlit as st
import requests
import re

# Configuration de la page
st.set_page_config(
    page_title="Assistant Fiscal Sénégalais",
    page_icon="💼",
    layout="centered"
)
def clean_markdown(text):
    """ Nettoie les balises HTML et supprime le texte indésirable """
    text = re.sub(r'<[^>]*>', '', text)  # Supprime tout HTML
    text = re.sub(r'&nbsp;', ' ', text)  # Remplace les espaces non sécables
    text = re.sub(r'\s+', ' ', text).strip()  # Nettoyage des espaces inutiles
    return text

# Appel API
def call_api(question):
    """ Envoie la question à l'API et récupère la réponse nettoyée """
    try:
        response = requests.get("http://127.0.0.1:8000/fiscalite", params={"question": question})
        if response.status_code == 200:
            raw_message = response.json().get("message", "❌ Réponse non trouvée.")
            return clean_markdown(raw_message)  
        else:
            return f"❌ Erreur API : {response.status_code}"
    except Exception as e:
        return f"❌ Erreur de connexion à l'API : {e}"

# Initialiser l'historique si nécessaire
if 'history' not in st.session_state:
    st.session_state.history = [
        ("assistant", 
         "💎 **ASSISTANT FISCAL PREMIUM** 💎\n\n"
         "💼 Bonjour ! Assistant fiscal sénégalais à votre service. "
         "Posez-moi vos questions sur les impôts et taxes.")
    ]


from bs4 import BeautifulSoup

def clean_response(text):
    # Suppression HTML
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()
    
    # Formatage Markdown
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_text)
    clean_text = re.sub(r'📌', '📌 ', clean_text)
    
    return clean_text

# Style CSS personnalisé
st.markdown("""
<style>
    .header {
        background-color: #2c3e50;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .chat-container {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        max-height: 60vh;
        overflow-y: auto;
    }
    .user-message {
        padding: 1rem;
        border-radius: 10px 10px 0 10px;
        margin-bottom: 1rem;
        margin-left: 15%;
        background-color: #3B3B3B;
        color: white;
    }
    .assistant-message {
        padding: 1rem;
        border-radius: 10px 10px 10px 0;
        margin-bottom: 1rem;
        margin-right: 15%;
        border-left: 4px solid #3498db;
        background-color: #2B2B2B;
    }
    .markdown-content {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #E0E0E0;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 10px 15px;
        background-color: #3B3B3B;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div class="header">
    <h1>💼 Assistant Fiscal Sénégalais</h1>
    <p>Direction Générale des Impôts</p>
</div>
""", unsafe_allow_html=True)

# Chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, message in st.session_state.history:
    if role == "user":
        st.markdown(f'''
        <div class="user-message">
            <strong>Vous :</strong><br>{message}
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="assistant-message">
            <div class="markdown-content">
                <strong>Assistant :</strong><br>{clean_response(message)}
            </div>
        </div>
        ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Saisie utilisateur
user_input = st.text_input("", placeholder="Posez votre question fiscale...")

if st.button("Envoyer") and user_input:
    st.session_state.history.append(("user", user_input))
    
    if user_input.lower() in ['au revoir', 'quit', 'q']:
        st.session_state.history.append(("assistant", "Merci pour votre confiance. À bientôt !"))
    else:
        with st.spinner("Consultation en cours..."):
            response = call_api(user_input)
        st.session_state.history.append(("assistant", response))
        

    st.rerun()

# Bouton pour vider l'historique
if st.button("🧹 Nouvelle discussion"):
    st.session_state.history = [
        ("assistant", 
         "💎 **ASSISTANT FISCAL PREMIUM** 💎\n\n"
         "💼 Bonjour ! Assistant fiscal sénégalais à votre service. "
         "Posez-moi vos questions sur les impôts et taxes.")
    ]
    st.rerun()
