import streamlit as st
import os

# Import API clients with proper error handling
try:
    from openai import OpenAI
except ImportError:
    st.error("OpenAI package not installed. Run: pip install openai")

# Placeholder for Gemini API - Google's API client needs proper import
try:
    import google.generativeai as genai
except ImportError:
    st.warning("Google Generative AI package not installed. Run: pip install google-generativeai")

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

# Only proceed if API key is entered
if not api_key:
    st.error("❌ API key is missing. Please enter your API key.")
    st.stop()

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
        
        # Call the API to refine the prompt based on selected provider
        try:
            refined_prompt = None
            
            if api_provider == "OpenAI":
                client = OpenAI(api_key=api_key)
                response_format_param = None
                if response_format == "JSON":
                    response_format_param = {"type": "json_object"}
                
                response = client.chat.completions.create(
                    model="gpt-4",  # You might want to make this configurable
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    response_format=response_format_param,
                    temperature=0.7
                )
                refined_prompt = response.choices[0].message.content
                
            elif api_provider == "Gemini":
                # Configure the Gemini API
                genai.configure(api_key=api_key)
                
                # Create a GenerativeModel object
                model = genai.GenerativeModel('gemini-pro')
                
                # Format messages for Gemini API
                messages = [
                    {"role": "user", "parts": [system_prompt + "\n\n" + user_input]}
                ]
                
                # Generate content with Gemini
                response = model.generate_content(messages)
                refined_prompt = response.text
            
            if refined_prompt:
                st.success("✅ Refined Prompt:")
                
                if response_format == "Markdown":
                    st.markdown(refined_prompt)
                else:
                    st.code(refined_prompt)
            else:
                st.error("❌ Failed to generate prompt: Empty response")
                
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
    else:
        st.warning("⚠️ Please fill in all fields before generating the prompt.")
