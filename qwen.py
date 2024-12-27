import streamlit as st
import requests

st.set_page_config(page_title="Chat con Qwen Model", layout="centered")

st.title("🤖 Chat con el modelo Qwen")


API_URL = "https://api-inference.huggingface.co/models/Qwen/QwQ-32B-Preview/v1/chat/completions"
API_KEY = "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"


def query_huggingface(messages, max_tokens=512, stream=False):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "Qwen/QwQ-32B-Preview",
        "messages" : messages,
        "max_tokens": max_tokens,
        "stream": stream,
         
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error al comunicarse con la API: {req_err}")
    except ValueError as json_err:
        st.error(f"Error al procesar la respuesta JSON: {json_err}")
    return None


st.subheader("Envía una consulta al modelo")
user_input = st.text_area("Escribe tu mensaje aqui...")


if st.button("Enviar"):
    if user_input.strip():
        with st.spinner("Obteniendo respuesta del modelo.."):
            messages = [{"role": "user", "content": user_input}]
            try:
                result = query_huggingface(messages)
                if "choices" in result:
                    response_content = result["choices"][0]["message"]["content"]
                    st.write("### Respuesta del Modelo:")
                    st.write(response_content)
                else:
                    st.error("Error en la respuesta del modelo.")
            except Exception as e:
                st.error(f"Error al comunicarse con la API: {e}")
    else:
        st.warning("Por favor, ingresa un mensaje antes de enviar.")


st.markdown("---")
st.caption("Aplicacion creada por Alejandro Muñoz con Streamlit y HuggingFace🤗")
