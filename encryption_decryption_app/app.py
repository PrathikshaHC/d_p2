"""
Streamlit Web Application for Caesar Cipher
Cyber Security Project 2 - Basic Encryption & Decryption
DecodeLabs Industrial Training Kit
"""

import sys
from pathlib import Path

# Ensure the directory containing cipher.py is in sys.path regardless of execution working directory
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
import cipher

# Page configuration
st.set_page_config(
    page_title="Caesar Cipher - Encryption & Decryption",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .output-box {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 12px 16px;
        font-family: monospace;
        font-size: 1.1rem;
        word-break: break-all;
    }
    .banner-warning {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 4px;
        color: #92400E;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-header">🔐 Caesar Cipher: Basic Encryption & Decryption</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">DecodeLabs Cyber Security Project 2 • Confidentiality & Reversible Transformations</div>', unsafe_allow_html=True)

# Educational Disclaimer Banner
st.markdown("""
<div class="banner-warning">
    <strong>⚠️ Educational & Demonstration Notice:</strong> The Caesar cipher is an ancient substitution cipher used here solely for foundational learning. 
    Because it has only 25 unique shift keys and preserves letter frequency patterns, it provides <strong>no security</strong> against modern cryptanalysis 
    and must never be used to protect sensitive or production data.
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "message_input" not in st.session_state:
    st.session_state["message_input"] = "HELLO WORLD"
if "shift_input" not in st.session_state:
    st.session_state["shift_input"] = 3
if "last_action" not in st.session_state:
    st.session_state["last_action"] = "both"  # "encrypt", "decrypt", or "both"
if "result_encrypted" not in st.session_state:
    st.session_state["result_encrypted"] = ""
if "result_decrypted" not in st.session_state:
    st.session_state["result_decrypted"] = ""

# Sidebar: Educational Reference & Project Details
with st.sidebar:
    st.header("📘 About This Project")
    st.markdown("""
    **DecodeLabs Industrial Training Kit**  
    *Cyber Security Project 2*
    
    ### How It Works:
    For each alphabetic letter, shift its position by $k$ places modulo 26 while preserving case:
    
    - **Encryption:**  
      $E(x) = (x + k) \\pmod{26}$
    - **Decryption:**  
      $D(x) = (x - k) \\pmod{26}$
      
    ### Key Properties:
    - **Case Preservation:** Uppercase and lowercase status is maintained.
    - **Wraparound:** End-of-alphabet wraps to the beginning (e.g., $Z \\xrightarrow{+3} C$).
    - **Punctuation & Spaces:** Numbers, spaces, and punctuation remain unchanged.
    - **Key Normalization:** Any integer shift (negative, 0, or $>26$) is automatically normalized using $\\text{shift} \\pmod{26}$.
    """)
    st.divider()
    st.caption("🔒 Privacy: All operations run locally in your browser session. Messages are never stored or transmitted.")

# Main Interface Layout
col_input, col_config = st.columns([2, 1])

with col_input:
    # Text input area
    message_text = st.text_area(
        label="Message Text",
        value=st.session_state["message_input"],
        height=140,
        placeholder="Type or paste your text message here...",
        help="Enter the plaintext to encrypt, or ciphertext to decrypt."
    )

with col_config:
    # Shift Key input
    shift_val = st.number_input(
        label="Shift Key (Integer)",
        value=st.session_state["shift_input"],
        step=1,
        format="%d",
        help="Integer number of positions to shift characters (can be positive, negative, or zero)."
    )
    
    try:
        norm_key = cipher.normalize_shift(shift_val)
        st.info(f"Normalized key: **{norm_key}** (mod 26)")
    except Exception as e:
        st.error(f"Invalid shift: {e}")
        norm_key = None

    # Quick Presets
    st.markdown("**Quick Presets:**")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    if btn_col1.button("Standard (3)"):
        st.session_state["message_input"] = "HELLO WORLD"
        st.session_state["shift_input"] = 3
        st.rerun()
    if btn_col2.button("Wrap (xyz)"):
        st.session_state["message_input"] = "xyz"
        st.session_state["shift_input"] = 3
        st.rerun()
    if btn_col3.button("Mixed Case"):
        st.session_state["message_input"] = "HeLLo, World! 123"
        st.session_state["shift_input"] = 2
        st.rerun()

# Action Buttons
st.markdown("### Actions")
btn_action_col1, btn_action_col2, btn_action_col3, btn_action_col4 = st.columns([1, 1, 1.5, 1])

with btn_action_col1:
    encrypt_clicked = st.button("🔒 Encrypt Message", use_container_width=True, type="primary")

with btn_action_col2:
    decrypt_clicked = st.button("🔓 Decrypt Ciphertext", use_container_width=True)

with btn_action_col3:
    demo_clicked = st.button("🔄 Encrypt & Decrypt (Full Cycle)", use_container_width=True)

with btn_action_col4:
    clear_clicked = st.button("🗑️ Clear / Reset", use_container_width=True)

# Process Button Actions
if clear_clicked:
    st.session_state["message_input"] = ""
    st.session_state["shift_input"] = 3
    st.session_state["result_encrypted"] = ""
    st.session_state["result_decrypted"] = ""
    st.session_state["last_action"] = "cleared"
    st.rerun()

# Perform Cipher Transformations
if encrypt_clicked:
    if not message_text.strip():
        st.warning("⚠️ Please enter a text message to encrypt.")
    else:
        try:
            encrypted = cipher.encrypt(message_text, shift_val)
            st.session_state["message_input"] = message_text
            st.session_state["shift_input"] = shift_val
            st.session_state["result_encrypted"] = encrypted
            st.session_state["result_decrypted"] = ""
            st.session_state["last_action"] = "encrypt"
        except Exception as err:
            st.error(f"❌ Encryption Error: {err}")

elif decrypt_clicked:
    if not message_text.strip():
        st.warning("⚠️ Please enter a ciphertext message to decrypt.")
    else:
        try:
            decrypted = cipher.decrypt(message_text, shift_val)
            st.session_state["message_input"] = message_text
            st.session_state["shift_input"] = shift_val
            st.session_state["result_decrypted"] = decrypted
            st.session_state["result_encrypted"] = ""
            st.session_state["last_action"] = "decrypt"
        except Exception as err:
            st.error(f"❌ Decryption Error: {err}")

elif demo_clicked:
    if not message_text.strip():
        st.warning("⚠️ Please enter a message for the full demonstration.")
    else:
        try:
            encrypted = cipher.encrypt(message_text, shift_val)
            decrypted = cipher.decrypt(encrypted, shift_val)
            st.session_state["message_input"] = message_text
            st.session_state["shift_input"] = shift_val
            st.session_state["result_encrypted"] = encrypted
            st.session_state["result_decrypted"] = decrypted
            st.session_state["last_action"] = "both"
        except Exception as err:
            st.error(f"❌ Transformation Error: {err}")

# Automatic initial calculation if both results are empty but message exists
if not st.session_state["result_encrypted"] and not st.session_state["result_decrypted"] and message_text and st.session_state["last_action"] != "cleared":
    try:
        st.session_state["result_encrypted"] = cipher.encrypt(message_text, shift_val)
        st.session_state["result_decrypted"] = cipher.decrypt(st.session_state["result_encrypted"], shift_val)
        st.session_state["last_action"] = "both"
    except Exception:
        pass

# Display Output Results
st.divider()
st.markdown("### Output Results & Verification")

if st.session_state["last_action"] == "both" and st.session_state["result_encrypted"]:
    # 3-Stage Pipeline Display: Original -> Encrypted -> Decrypted
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown("#### 1. Original Text")
        st.code(message_text, language="text")
        st.caption("Initial plaintext provided by user")

    with col_res2:
        st.markdown(f"#### 2. Encrypted (Shift +{shift_val})")
        st.code(st.session_state["result_encrypted"], language="text")
        st.caption("Hover code block and click copy icon to copy")

    with col_res3:
        st.markdown(f"#### 3. Decrypted (Shift -{shift_val})")
        st.code(st.session_state["result_decrypted"], language="text")
        if st.session_state["result_decrypted"] == message_text:
            st.success("✅ Exact match! Confidentiality & reversibility verified.")
        else:
            st.error("Mismatch detected.")

elif st.session_state["last_action"] == "encrypt" and st.session_state["result_encrypted"]:
    st.markdown(f"#### Encrypted Ciphertext (Shift Key = {shift_val}):")
    st.code(st.session_state["result_encrypted"], language="text")
    st.info("Tip: You can copy this ciphertext and click 'Decrypt Ciphertext' to test reversal.")

elif st.session_state["last_action"] == "decrypt" and st.session_state["result_decrypted"]:
    st.markdown(f"#### Decrypted Plaintext (Shift Key = {shift_val}):")
    st.code(st.session_state["result_decrypted"], language="text")
    st.success("Reversed shift transformation successfully applied.")

elif st.session_state["last_action"] == "cleared":
    st.info("Inputs and outputs have been cleared. Enter a message and shift key to begin.")

# Verification Summary Table (as requested in Section 4 of spec)
with st.expander("📊 View Transformation Summary Table"):
    st.markdown(f"""
    | Stage | Text |
    | :--- | :--- |
    | **Original** | `{message_text}` |
    | **Encrypted** | `{st.session_state.get('result_encrypted', '') or '—'}` |
    | **Decrypted** | `{st.session_state.get('result_decrypted', '') or '—'}` |
    | **Active Key** | `{shift_val}` (Normalized: `{cipher.normalize_shift(shift_val) if norm_key is not None else 'N/A'}`) |
    """)
