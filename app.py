import streamlit as st
import os
from openai import OpenAI

# Streamlit App UI
st.title("📝 Streamlit Prompting App")
st.write("Enter details below to refine your prompt.")

# User Inputs
api_provider = st.selectbox("API Provider", ["OpenAI", "Gemini"])
api_key = st.text_input("API Key", type="password")
role = st.text_input("Role (e.g., 'You are a coding expert')")
context = st.text_area("Context (Provide background info)")
task = st.text_area("Task (What do you want the AI to do?)")
response_format = st.selectbox("Response Format", ["Plain Text", "JSON", "Markdown"])

# Check if API key is present
if not api_key:
    st.error("❌ API key is missing. Please enter your API key.")
    st.stop()

# Initialize the API client based on the selected provider
if api_provider == "OpenAI":
    client = OpenAI(api_key=api_key)
elif api_provider == "Gemini":
    # Initialize Gemini client (assuming similar interface)
    client = Gemini(api_key=api_key)

# Submit button
if st.button("Generate Prompt"):
    if role and context and task:
        # Create the system prompt to ask the API to refine the user's prompt
        system_prompt = (
            "You are an expert at creating clear, effective AI prompts. "
            "Your task is to refine and improve the prompt components provided by the user. "
            "Create a well-structured, detailed prompt that will get the best results."
        )
        
        user_input = (
            f"Please refine and improve this prompt:\n\n"
            f"Role: {role}\n\n"
            f"Context: {context}\n\n"
            f"Task: {task}\n\n"
            f"Return only the refined prompt without explanations or additional text."
        )

        # Call the API to refine the prompt
        try:
            response_format_param = None
            if response_format == "JSON":
                response_format_param = {"type": "json_object"}
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                response_format=response_format_param,
                temperature=0.7
            )
            refined_prompt = response.choices[0].message.content
            st.success("✅ Refined Prompt:")
            st.code(refined_prompt)
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
    else:
        st.warning("⚠️ Please fill in all fields before generating the prompt.")