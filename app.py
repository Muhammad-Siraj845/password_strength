import streamlit as st
import re

st.set_page_config(page_title="Password Strength Checker", page_icon="🔒")

# Custom CSS for better styling
st.markdown("""
    <style>
    .feedback-box {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .good { background-color: #90EE90; }
    .weak { background-color: #FFB6C1; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔒 Password Strength Checker")
st.markdown("### Check how strong your password is")

# Password input
password = st.text_input("Enter your password", type="password")

# Initialize feedback dictionary
feedback = {}
score = 0
min_length = 8

if password:
    # Length check
    if len(password) >= min_length:
        feedback["Length (min 8 characters)"] = ("Good", f"Length: {len(password)} characters")
        score += 1
    else:
        feedback["Length (min 8 characters)"] = ("Weak", f"Add {min_length - len(password)} more characters")

    # Uppercase check
    uppercase_count = len(re.findall(r'[A-Z]', password))
    if uppercase_count > 0:
        feedback["Uppercase letters"] = ("Good", f"Contains {uppercase_count} uppercase letters")
        score += 1
    else:
        feedback["Uppercase letters"] = ("Weak", "Add at least one uppercase letter")

    # Number check
    number_count = len(re.findall(r'[0-9]', password))
    if number_count > 0:
        feedback["Numbers"] = ("Good", f"Contains {number_count} numbers")
        score += 1
    else:
        feedback["Numbers"] = ("Weak", "Add at least one number")

    # Special character check
    special_chars = len(re.findall(r'[!@#$%^&*?]', password))
    if special_chars > 0:
        feedback["Special characters"] = ("Good", f"Contains {special_chars} special characters")
        score += 1
    else:
        feedback["Special characters"] = ("Weak", "Add at least one special character (!@#$%^&*?)")

    # Common patterns check
    common_patterns = [
        r'12345',
        r'qwerty',
        r'password',
        r'admin',
        r'abc123'
    ]
    
    has_common_pattern = any(re.search(pattern.lower(), password.lower()) for pattern in common_patterns)
    if has_common_pattern:
        score = max(0, score - 1)
        st.warning("⚠️ Your password contains common patterns that make it easier to guess")

    # Display overall strength
    strength_percentage = (score / 4) * 100
    st.progress(strength_percentage / 100)
    
    if score == 4:
        st.success("🎉 Your password is strong!")
    elif score == 3:
        st.warning("⚠️ Your password is medium strength")
    else:
        st.error("❌ Your password is weak")

    # Display detailed feedback
    if feedback:
        st.markdown("### Password Analysis")
        for criterion, (status, message) in feedback.items():
            color = "good" if status == "Good" else "weak"
            st.markdown(
                f"""<div class="feedback-box {color}">
                    <strong>{criterion}:</strong> {message}
                </div>""",
                unsafe_allow_html=True
            )

    # Password length indicator
    if password:
        st.markdown(f"Current password length: {len(password)} characters")

else:
    st.info("👆 Please enter a password to check its strength")
    st.markdown("""
    #### Tips for a strong password:
    - Use at least 8 characters
    - Include uppercase letters
    - Include numbers
    - Include special characters (!@#$%^&*?)
    - Avoid common patterns and words
    """)
        
