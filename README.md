# AI PM Buddy v2.0 - Cloud Version

This is a cloud-friendly version of the AI PM Buddy v2.0 application, optimized for deployment on Streamlit Cloud and other cloud platforms.

## Deployment Instructions

### Streamlit Cloud Deployment

1. **Create a Streamlit Cloud account**:
   - Visit https://streamlit.io/cloud and sign up

2. **Important: File Naming for Streamlit Cloud**:
   - Rename `app_v2.py` to `streamlit_app.py` before uploading
   - OR specify `app_v2.py` as the main file during configuration

3. **Deploy the application**:
   - Click "New app" 
   - Connect your GitHub repository or use the template option
   - If using GitHub, make sure to specify `app_v2.py` as the main file
   - Add your OpenAI API key as a secret (name: OPENAI_API_KEY)
   - Click "Deploy"

### Setting up OpenAI API Key

The application requires an OpenAI API key to use the AI features:

1. Create an account at https://platform.openai.com
2. Generate an API key
3. Add it to your deployment as an environment variable or secret

## Files Structure

- `app_v2.py`: Main application file
- `utils/data_utils.py`: Data management utilities
- `utils/visualization.py`: Visualization functions (cloud-optimized)
- `.streamlit/config.toml`: Server configuration
- `requirements.txt`: Dependencies list (cloud-optimized)

## Features

- Interactive project dashboard
- AI-powered project insights
- Resource allocation monitoring
- RAID (Risks, Assumptions, Issues, Dependencies) management
- Decision log tracking
- Team sentiment analysis
- And more!

## Cloud Optimization Notes

This version has been modified for cloud compatibility:

- Removed PyGraphviz dependency for better compatibility with cloud platforms
- Used pure Python implementations for network visualizations
- Optimized requirements for faster deployment
- Added proper server configuration for cloud environments