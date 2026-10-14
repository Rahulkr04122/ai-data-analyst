
import requests
import pandas as pd
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AI Data Analyst Copilot",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Data Analyst Copilot")
st.write(
    "Ask questions about your business data "
    "using natural language."
)

question = st.text_input(
    "Your business question",
    placeholder="Which five products generated the most revenue?",
)

if st.button("Analyze", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Analyzing your data..."):
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=180,
                )

            if response.ok:
                data = response.json()

                st.subheader("Answer")
                st.write(f"Question: {data['question']}")
                st.metric("Rows returned", data["row_count"])

                results = data["results"]

                if results:
                    st.dataframe(
                        pd.DataFrame(results),
                        use_container_width=True,
                    )
                else:
                    st.info("No matching records found.")

                with st.expander("View generated SQL"):
                    st.code(data["sql"], language="sql")

            else:
                st.error(
                    f"Request failed ({response.status_code}): "
                    f"{response.text}"
                )

        except requests.RequestException as error:
            st.error(
                "Could not connect to the API. "
                "Check that FastAPI is running."
            )
            st.caption(str(error))
