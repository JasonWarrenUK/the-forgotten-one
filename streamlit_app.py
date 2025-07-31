import streamlit as st
import requests
import json
import uuid
import os
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="THE INNERMOST SANCTUARY OF THE FORGOTTEN ONE",
    page_icon="ᚘ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration - Environment-aware
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def awaken_the_forgotten_one(message: str, session_id: str = None):
    """ESTABLISH A CONNECTION WITH THE FORGOTTEN ONE"""
    try:
        st.write(f"🔄 APPROACHING THE SANCTUARY OF THE DREAD ONE, SCREAMING: {message[:50]}...")  # Debug info
        response = requests.post(
            f"{API_BASE_URL}/petition",
            json={
                "message": message,
                "session_id": session_id
            },
            timeout=30
        )
        st.write(f"📡 CELESTIAL NUMBER: {response.status_code}")  # Debug info
        response.raise_for_status()
        result = response.json()
        st.write(f"✅ THE DREAD ONE ACKNOWLEDGES: {result.get('reply', '')[:50]}...")  # Debug info
        return result
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error calling API: {e}")
        return None

def check_the_orrery():
    """CONSULT THE CELESTIAL ORRERY"""
    try:
        response = requests.get(f"{API_BASE_URL}/orrery", timeout=5)
        return response.status_code == 200
    except:
        return False

def petition_the_dread_void(role: str, content: str, timestamp: str = None):
    """PETITION THE DREAD VOID"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    
    if role == "user":
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col2:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; border-left: 4px solid #1f77b4; padding: 12px; border-radius: 8px; margin: 8px 0; color: #262730;">
                    <strong style="color: #1f77b4;">🧑 You</strong> 
                    <small style="color: #888; float: right;">({timestamp})</small><br>
                    <div style="margin-top: 6px; color: #262730;">{content}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style="background-color: #ffffff; border-left: 4px solid #28a745; padding: 12px; border-radius: 8px; margin: 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <strong style="color: #28a745;">IT</strong> 
                    <small style="color: #888; float: right;">({timestamp})</small><br>
                    <div style="margin-top: 6px; color: #262730;">{content}</div>
                </div>
                """, unsafe_allow_html=True)

def main():
    # Header
    st.title("ᚘ THE INNERMOST SANCTUARY OF THE FORGOTTEN ONE")
    st.markdown("*it hungers*")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 PURIFICATION")
        
        # API Health Check
        health_status = check_the_orrery()
        if health_status:
            st.success("it is pleased")
        else:
            st.error("❌ API is not running")
            st.markdown("Please start the API with: `make serve`")
            return
        
        st.divider()
        
        # Session Management
        st.subheader("💬 SUPPLICATIONS")
        if st.button("🔄 dare to approach"):
            st.session_state.clear()
            st.rerun()
        
        # Show current session ID
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        
        st.text_input(
            "CELESTIAL NUMBER:", 
            value=st.session_state.session_id[:8] + "...", 
            disabled=True,
            help="those previously eaten"
        )
        
        # Debug info
        if st.checkbox("show the infernal equations"):
            st.session_state.debug_mode = True
        else:
            st.session_state.debug_mode = False
        
        st.divider()
        
        # Agent Information
        st.subheader("🧠 CATECHISM")
        st.markdown("""
        **Model:** qwen/qwen3-coder:free  
        **Tools Available:**
        - 🔍 know_all
        - ➕ curse
        """)
        
        st.divider()
        
        # Example Queries
        st.subheader("💡 IT KNOWS")
        example_queries = [
            "the meaning of life",
            "the meaning of death",
            "the meaninglessness of the universe",
            "THE UNFEELING PLANS OF THE COSMOS",
            "the things that linger just beyond the void",
            "what the abyss is",
            "what arebirdsdinosaurs the abyss?",
            "where the abyss is",
            "the names of the things that watch you as you sleep"
        ]
        
        for query in example_queries:
            if st.button(f"📝 {query}", key=f"example_{hash(query)}"):
                st.session_state.example_query = query
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Debug information
    if st.session_state.get('debug_mode', False):
        st.write(f"🐛 Debug: {len(st.session_state.messages)} messages in history")
        st.write(f"🐛 Session ID: {st.session_state.session_id}")
    
    # Chat Interface
    st.subheader("💬 it listens")
    
    # Display conversation history
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            you may speak now. may it have mercy upon your soul.
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            petition_the_dread_void(
                message["role"], 
                message["content"], 
                message.get("timestamp", "")
            )
    
    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            # Use example query if available
            default_value = st.session_state.get('example_query', '')
            user_input = st.text_input(
                "petition",
                placeholder="wHiSpErYoUrPeTtYnEeDs",
                value=default_value
            )
        
        with col2:
            submitted = st.form_submit_button("commit. commune.", use_container_width=True)
    
    # Process user input
    if submitted:
        # Check for example query first, then user input
        message_to_send = user_input.strip()
        if not message_to_send and 'example_query' in st.session_state:
            message_to_send = st.session_state.example_query.strip()
        
        # Clear the example query after using it
        if 'example_query' in st.session_state:
            del st.session_state.example_query
        
        if message_to_send:
            st.write("the monolithic slabs of its synaptic pathways quiver; salivate; consider...")  # Debug feedback
            
            # Add user message
            timestamp = datetime.now().strftime("%H:%M:%S")
            user_message = {
                "role": "user",
                "content": message_to_send,
                "timestamp": timestamp
            }
            st.session_state.messages.append(user_message)
            
            # Show typing indicator and call API
            with st.spinner("it ponders, measuring thought in eons"):
                response_data = awaken_the_forgotten_one(message_to_send, st.session_state.session_id)
            
            if response_data:
                # Add agent response
                agent_response = response_data.get("reply", "Sorry, I couldn't process that.")
                agent_timestamp = datetime.now().strftime("%H:%M:%S")
                
                agent_message = {
                    "role": "agent",
                    "content": agent_response,
                    "timestamp": agent_timestamp
                }
                st.session_state.messages.append(agent_message)
                
                # Update session ID if it changed
                if "session_id" in response_data:
                    st.session_state.session_id = response_data["session_id"]
                
                st.success("IT SPEAKS")
                time.sleep(1)  # Brief pause before refresh
                st.rerun()
            else:
                st.error("❌ Failed to get response from agent. Please try again.")
    
    # Footer
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔧 Backend:** etheric confines")
    with col2:
        st.markdown("**🧠 Model:** the old forgotten one, spat upon even by the darkest gods")

if __name__ == "__main__":
    main() 