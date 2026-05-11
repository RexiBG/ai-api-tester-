import streamlit as st
import requests
import time

st.title("AI API Tester")

PROVIDERS = {
    "Groq": {
        "signup": "https://console.groq.com/keys",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama-3.3-70b-versatile"
    },
    "Google Gemini": {
        "signup": "https://aistudio.google.com/app/apikey",
        "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        "model": "gemini-2.0-flash"
    },
    "Together AI": {
        "signup": "https://api.together.xyz/settings/api-keys",
        "url": "https://api.together.xyz/v1/chat/completions",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    },
    "Scaleway": {
        "signup": "https://console.scaleway.com/iam/api-keys",
        "url": "https://api.scaleway.ai/v1/chat/completions",
        "model": "llama-3.1-8b-instruct"
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
            error_detail = None
            if name == "Google Gemini":
                r = requests.post(
                    p["url"],
                    headers={"Content-Type": "application/json", "x-goog-api-key": key},
                    json={"contents": [{"role": "user", "parts": [{"text": "Здравей"}]}]},
                    timeout=30
                )
                data = r.json()
                if r.status_code == 200:
                    candidates = data.get("candidates") or []
                    parts = ((candidates[0].get("content") or {}).get("parts") or []) if candidates else []
                    ans = "\n".join(part.get("text", "") for part in parts if part.get("text")).strip() or None
                else:
                    ans = None
                    error_detail = (data.get("error") or {}).get("message")
            else:
                r = requests.post(
                    p["url"],
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": p["model"], "messages": [{"role": "user", "content": "Здравей"}]},
                    timeout=30
                )
                data = r.json()
                ans = data["choices"][0]["message"]["content"] if r.status_code == 200 else None
                if r.status_code != 200:
                    error_detail = (data.get("error") or {}).get("message")
            
            if ans:
                st.success(f"Работи! ({time.time()-start:.1f}s)")
                st.write(ans)
            else:
                details = f" - {error_detail}" if error_detail else ""
                st.error(f"Грешка: {r.status_code}{details}")
        except Exception as e:
            st.error(f"Грешка: {e}")
