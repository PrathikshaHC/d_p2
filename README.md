# Cyber Security Project 2: Basic Encryption & Decryption

**DecodeLabs Industrial Training Kit – Project 2**  
Implementation of a reversible text transformation application using the Caesar cipher with Python and Streamlit.

---

## 1. Project Overview & Objective

The primary objective of this project is to demonstrate core concepts of data confidentiality and reversible symmetric transformations. Users can enter a text message, set an integer shift key, encrypt the message into ciphertext, and decrypt it back to verify the exact original message.

### ⚠️ Educational Limitation Notice
> **Important Cryptographic Notice:** The Caesar cipher is an ancient monoalphabetic substitution cipher implemented here strictly for educational and conceptual demonstration. With only 25 unique non-trivial shift keys ($k \in [1, 25]$) and unchanged letter frequency distributions, the cipher is trivial to break using brute force or frequency analysis. It **does not** provide modern or production-grade security and must never be used to protect real, personal, or sensitive information.

---

## 2. Key Features

- **Reversible Transformation:** Encrypts plaintext to ciphertext and restores original text via inverse shift.
- **Robust Character Handling:**
  - Preserves uppercase and lowercase case sensitivity.
  - Automatically wraps around the alphabet ($Z \xrightarrow{+3} C$, $a \xrightarrow{-3} x$).
  - Leaves spaces, numbers, punctuation, and special symbols unchanged.
- **Key Normalization:** Accepts positive, zero, negative, or large integer shifts using modulo 26 arithmetic.
- **Interactive Streamlit Web UI:**
  - Multi-line text area for message input.
  - Numeric shift key selector with quick presets (Standard, Wraparound, Mixed case).
  - Dedicated **Encrypt**, **Decrypt**, and **Encrypt & Decrypt (Full Cycle)** actions.
  - Clear / Reset action to restore default state.
  - Native one-click copy-to-clipboard on output blocks.
  - Summary comparison table showing Original, Encrypted, and Decrypted stages.
- **Zero Data Retention:** Operations are performed purely in-memory in the local session; messages are never stored or transmitted.

---

## 3. Mathematical Specification

For each alphabetic character position $x \in \{0, 1, \dots, 25\}$:

- **Encryption Function:**  
  $$E(x) = (x + k) \pmod{26}$$

- **Decryption Function:**  
  $$D(x) = (x - k) \pmod{26}$$

### Example (Shift Key $k = 3$):
| Stage | Text |
| :--- | :--- |
| **Original** | `HELLO WORLD` |
| **Encrypted** | `KHOOR ZRUOG` |
| **Decrypted** | `HELLO WORLD` |

---

## 4. Project Directory Structure

```text
d:\decoding labs\project 2\
│
├── Codex_Project2_Encryption_Decryption_Brief.pdf
├── requirements.txt
├── README.md
│
└── encryption_decryption_app/
    ├── cipher.py            # Core cryptographic logic (encrypt, decrypt, normalize_shift)
    ├── app.py               # Streamlit web user interface
    ├── test_cipher.py       # Unit test suite covering all project requirements
    ├── requirements.txt     # Python dependencies
    └── README.md            # Project documentation and setup guide
```

---

## 5. Prerequisites

- **Python:** Python 3.8 or higher (tested with Python 3.12).
- **Package Manager:** `pip` (included with standard Python installations).
- **Web Browser:** Any modern browser (Chrome, Edge, Firefox, Safari).

---

## 6. Installation & Setup

1. **Open your terminal or command prompt** and navigate to the project directory:
   ```bash
   cd "d:/decoding labs/project 2/encryption_decryption_app"
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 7. Running the Application

Launch the Streamlit web application with:

```bash
streamlit run app.py
```
*(Or from the project root: `streamlit run encryption_decryption_app/app.py`)*

Once executed, Streamlit will automatically open the application in your default browser at:
```text
http://localhost:8501
```

---

## 8. Running the Automated Test Suite

To verify all cipher behavior against project requirements:

```bash
python -m unittest encryption_decryption_app/test_cipher.py -v
```

### Verified Test Cases:
1. `test_standard_spec_hello_world`: `HELLO WORLD` with key 3 $\rightarrow$ `KHOOR ZRUOG` $\rightarrow$ `HELLO WORLD`.
2. `test_lowercase_wraparound_xyz`: `xyz` with key 3 $\rightarrow$ `abc` $\rightarrow$ `xyz`.
3. `test_mixed_case_preservation`: `HeLLo` with key 2 preserves casing $\rightarrow$ `JgNNq`.
4. `test_spaces_punctuation_numbers_preserved`: Numbers, symbols, spaces, and punctuation remain unchanged.
5. `test_key_zero_identity`: Key 0 returns identical text.
6. `test_key_larger_than_26`: Keys $>26$ (e.g. 29, 107) normalize correctly via modulo 26.
7. `test_negative_key`: Negative shift keys (e.g. $-3$) behave consistently.
8. `test_empty_string`: Empty input returns empty string gracefully without error.
9. `test_shift_normalization_and_validation`: Shift key validation rejects decimals and non-integers.
10. `test_invalid_text_type`: Type checks reject non-string inputs safely.
