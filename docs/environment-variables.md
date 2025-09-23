# Environment Variables

This guide explains how to configure environment variables for the Car System Agentic AI project.

## Overview

The project uses environment variables to manage sensitive configuration like API keys and other settings. These are loaded from a `.env` file in the project root.

## Setup

### 1. Create Environment File

Create a `.env` file in the project root directory:

```bash
# Copy the example file (if available)
cp .env.example .env

# Or create manually
touch .env
```

### 2. Required Variables

Add the following variables to your `.env` file:

```bash
# Google AI API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here

# LangSmith Configuration (Optional - for observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=car-system-agentic-ai
```

## Variable Descriptions

### Required Variables

#### `GOOGLE_API_KEY`
- **Purpose**: Authentication for Google Gemini AI models
- **Required**: Yes
- **Format**: String (API key from Google AI Studio)
- **Example**: `GOOGLE_API_KEY=AIzaSyC9X8Y7Z6W5V4U3T2S1R0Q9P8O7N6M5L4K3`

**How to get your API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" 
4. Create a new API key or use an existing one
5. Copy the key to your `.env` file

### Optional Variables (LangSmith Observability)

#### `LANGCHAIN_TRACING_V2`
- **Purpose**: Enable LangSmith tracing for debugging and monitoring
- **Required**: No (but recommended for development)
- **Format**: Boolean (`true` or `false`)
- **Default**: `false`
- **Example**: `LANGCHAIN_TRACING_V2=true`

#### `LANGCHAIN_API_KEY`
- **Purpose**: Authentication for LangSmith platform
- **Required**: Only if `LANGCHAIN_TRACING_V2=true`
- **Format**: String (API key from LangSmith)
- **Example**: `LANGCHAIN_API_KEY=ls__abc123def456ghi789jkl012mno345pqr678`

#### `LANGCHAIN_PROJECT`
- **Purpose**: Project name for organizing traces in LangSmith
- **Required**: No
- **Format**: String (project identifier)
- **Default**: `default`
- **Example**: `LANGCHAIN_PROJECT=car-system-agentic-ai`

**How to get your LangSmith API key:**
1. Go to [LangSmith](https://smith.langchain.com/)
2. Sign up or sign in to your account
3. Navigate to Settings → API Keys
4. Create a new API key
5. Copy the key to your `.env` file

**Benefits of LangSmith integration:**
- 🔍 **Trace Debugging**: See detailed execution flows of your agents
- 📊 **Performance Monitoring**: Track token usage and response times
- 🐛 **Error Analysis**: Identify and debug issues in agent interactions
- 📈 **Usage Analytics**: Monitor system performance over time
