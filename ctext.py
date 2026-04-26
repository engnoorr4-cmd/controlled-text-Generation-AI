import streamlit as st
import pandas as pd
import random
import re

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AI Controlled Product Description Generator",
    page_icon="🤖",
    layout="wide"
)

# =========================
# Custom Design
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 900;
    color: #00c8ff;
    text-align: center;
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #d9edf7;
}
.owner {
    text-align: center;
    font-size: 15px;
    color: #ffd166;
    margin-top: 8px;
}
.card {
    padding: 20px;
    border-radius: 18px;
    background: linear-gradient(135deg, #132238, #1b2f4a);
    border: 1px solid #00c8ff;
    margin-bottom: 18px;
}
.best-card {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(135deg, #123524, #1f6f43);
    border: 2px solid #00ff88;
    margin-bottom: 20px;
}
.green-word {
    color: #00ff88;
    font-weight: bold;
}
.red-word {
    color: #ff4d4d;
    font-weight: bold;
}
.footer {
    text-align: center;
    margin-top: 40px;
    color: #aaa;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown('<div class="main-title">🤖 Controlled Text Generation for Product Descriptions</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A lightweight AI-style system for generating product descriptions under user-defined constraints.</div>', unsafe_allow_html=True)
st.markdown('<div class="owner">Developed by: Noor Al-Hussein Hatim | Al-Farabi University</div>', unsafe_allow_html=True)

st.divider()

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("⚙️ Control Panel")
    number_of_outputs = st.slider("Number of generated descriptions", 1, 5, 3)
    tone = st.selectbox("Writing Tone", ["Professional", "Marketing", "Luxury", "Simple", "Academic"])
    length_style = st.selectbox("Description Length", ["Short", "Medium", "Long"])

    st.info("This system generates descriptions, checks constraints, selects the best output, and evaluates quality.")

# =========================
# Inputs
# =========================
st.subheader("📝 Product Information")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Product Name", "Smart Watch")
    category = st.text_input("Product Category", "Wearable Technology")
    target_audience = st.text_input("Target Audience", "athletes and fitness lovers")

with col2:
    must_include = st.text_input("Required Words", "accurate, tracking, performance")
    forbidden_words = st.text_input("Forbidden Words", "cheap, low, basic")
    main_feature = st.text_input("Main Feature", "improves daily fitness tracking")

st.divider()

# =========================
# Functions
# =========================
def clean_words(text):
    return [w.strip().lower() for w in text.split(",") if w.strip()]

def sentence_bank(tone):
    banks = {
        "Professional": [
            "The {product} is designed as a reliable {category} for {audience}.",
            "It provides {required} while maintaining a professional user experience.",
            "This product focuses on {feature}, making it suitable for modern users."
        ],
        "Marketing": [
            "Discover the power of {product}, a modern {category} created for {audience}.",
            "With {required}, it delivers an attractive and useful experience.",
            "It is the perfect choice for anyone looking for {feature}."
        ],
        "Luxury": [
            "{product} introduces a premium {category} experience for {audience}.",
            "Crafted with attention to quality, it highlights {required} in an elegant way.",
            "Its refined identity makes it ideal for customers who value {feature}."
        ],
        "Simple": [
            "{product} is a simple and useful {category} for {audience}.",
            "It includes {required} and is easy to use.",
            "It helps users enjoy {feature}."
        ],
        "Academic": [
            "This system describes {product} as a {category} intended for {audience}.",
            "The generated description emphasizes {required} as core product attributes.",
            "The product value is represented through its ability to support {feature}."
        ]
    }
    return banks[tone]

def generate_description(product, category, audience, required_words, feature, tone, length_style):
    required_text = ", ".join(required_words)
    templates = sentence_bank(tone)

    if length_style == "Short":
        selected = templates[:2]
    elif length_style == "Medium":
        selected = templates
    else:
        selected = templates + [
            "The description is generated according to controlled rules to ensure clarity and consistency.",
            "This makes the output suitable for e-commerce, catalog writing, and business presentation."
        ]

    random.shuffle(selected)

    description = " ".join(selected).format(
        product=product,
        category=category,
        audience=audience,
        required=required_text,
        feature=feature
    )

    return description

def evaluate_text(text, required_words, forbidden_words):
    text_lower = text.lower()

    included = [w for w in required_words if w in text_lower]
    missing = [w for w in required_words if w not in text_lower]
    violations = [w for w in forbidden_words if w in text_lower]

    score = 100
    score -= len(missing) * 15
    score -= len(violations) * 30
    score = max(score, 0)

    if score >= 90:
        quality = "Excellent"
    elif score >= 70:
        quality = "Good"
    else:
        quality = "Needs Improvement"

    return included, missing, violations, score, quality

def remove_forbidden_words(text, forbidden_words):
    cleaned = text
    for word in forbidden_words:
        cleaned = re.sub(rf"\b{re.escape(word)}\b", "[REMOVED]", cleaned, flags=re.IGNORECASE)
    return cleaned

def highlight_text(text, required_words, forbidden_words):
    highlighted = text

    for word in required_words:
        highlighted = re.sub(
            rf"\b{re.escape(word)}\b",
            f"<span class='green-word'>{word}</span>",
            highlighted,
            flags=re.IGNORECASE
        )

    for word in forbidden_words:
        highlighted = re.sub(
            rf"\b{re.escape(word)}\b",
            f"<span class='red-word'>{word}</span>",
            highlighted,
            flags=re.IGNORECASE
        )

    return highlighted

# =========================
# Main Button
# =========================
if st.button("🚀 Generate Controlled Descriptions", use_container_width=True):
    required_list = clean_words(must_include)
    forbidden_list = clean_words(forbidden_words)

    results = []

    for i in range(number_of_outputs):
        generated = generate_description(
            product_name,
            category,
            target_audience,
            required_list,
            main_feature,
            tone,
            length_style
        )

        safe_generated = remove_forbidden_words(generated, forbidden_list)

        included, missing, violations, score, quality = evaluate_text(
            safe_generated,
            required_list,
            forbidden_list
        )

        results.append({
            "Version": i + 1,
            "Generated Description": safe_generated,
            "Included Required Words": ", ".join(included) if included else "None",
            "Missing Required Words": ", ".join(missing) if missing else "None",
            "Forbidden Violations": ", ".join(violations) if violations else "None",
            "Constraint Score": score,
            "Quality": quality
        })

    best_result = max(results, key=lambda x: x["Constraint Score"])

    st.subheader("🏆 Best Generated Description")

    best_colored = highlight_text(
        best_result["Generated Description"],
        required_list,
        forbidden_list
    )

    st.markdown(f"""
    <div class="best-card">
        <h3>Best Version: {best_result['Version']}</h3>
        <p style="font-size:18px;">{best_colored}</p>
        <h2>Score: {best_result['Constraint Score']}%</h2>
        <h3>Quality: {best_result['Quality']}</h3>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📌 All Generated Descriptions")

    for item in results:
        colored_text = highlight_text(
            item["Generated Description"],
            required_list,
            forbidden_list
        )

        st.markdown(f"""
        <div class="card">
            <h3>Version {item['Version']}</h3>
            <p style="font-size:17px;">{colored_text}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Score", f"{item['Constraint Score']}%")
        c2.metric("Quality", item["Quality"])
        c3.metric("Missing", item["Missing Required Words"])
        c4.metric("Violations", item["Forbidden Violations"])

        st.divider()

    st.subheader("📊 Evaluation Table")
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Evaluation Results",
        data=csv,
        file_name="controlled_text_generation_results.csv",
        mime="text/csv"
    )

    st.subheader("✨ Improved Best Result")
    improved_text = best_result["Generated Description"] + " This output demonstrates controlled generation by respecting required terms, avoiding forbidden words, and producing a clear product-focused description."
    st.success(improved_text)

else:
    st.info("Fill the product information, choose the tone, then click Generate Controlled Descriptions.")

# =========================
# Footer
# =========================
st.markdown("""
<div class="footer">
    © 2026 Noor Al-Hussein Hatim | Department of Computer Engineering | Al-Farabi University
</div>
""", unsafe_allow_html=True)