import streamlit as st
import requests
import time

st.title("AI API Tester")

PROVIDERS = {
    "Groq": {
        "signup": "https://console.groq.com/keys",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama-3.3-70b-versatile"
    }
}

name = st.selectbox("Избери:", list(PROVIDERS.keys()))
p = PROVIDERS[name]

st.markdown(f"[Вземи API ключ]({p['signup']})")

key = st.text_input("API ключ:", type="password")

if st.button("Тествай") and key:
    with st.spinner("Тествам..."):
        start = time.time()
        try:
            r = requests.post(
                p["url"],
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": p["model"], "messages": [{"role": "user", "content": "Здравей"}]},
                timeout=30
            )
            if r.status_code == 200:
                ans = r.json()["choices"][0]["message"]["content"]
                st.success(f"Работи! ({time.time()-start:.1f}s)")
                st.write(ans)
            else:
                st.error(f"Грешка: {r.status_code}")
        except Exception as e:
            st.error(f"Грешка: {e}")
