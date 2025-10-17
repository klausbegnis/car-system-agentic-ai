# API Documentation

## Overview

The Car System Agentic AI API provides intelligent car diagnostics and travel planning through a multi-agent architecture. The API uses streaming responses to provide real-time updates during processing.

## Base URL

```
http://localhost:8083
```

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## Endpoints

### Health Check

#### GET /

Returns a simple welcome message.

**Response:**
```json
{
  "message": "AgenticAI application for trip planning."
}
```

#### GET /health

Returns detailed health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "car-system-agentic-ai",
  "version": "1.0.0"
}
```

### Chat with AI Agents

#### POST /chat

Interact with the AI agents for car diagnostics and travel planning.

**Request Body:**
```json
{
  "message": "string",
  "thread_id": "string"
}
```

**Parameters:**
- `message` (string, required): The question or request for the AI agents
- `thread_id` (string, required): Unique identifier for conversation context

**Response:**
- **Content-Type:** `text/event-stream`
- **Format:** Server-Sent Events (SSE)

**Example Request:**
```bash
curl -X POST "http://localhost:8083/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "quero viajar onde voce recomenda eu ir?",
    "thread_id": "car-diagnosis-456"
  }'
```

**Example Response Stream:**
```
data: {"input_guard_rail": {"processing_status": "input_validated", "error_message": null}}

data: {"reasoning_node": {"messages": [...], "analysis_result": {...}, "recommendations": [...], "processing_status": "analysis_completed", "error_message": null}}

data: {"output_guard_rail": {"messages": [...], "processing_status": "completed_successfully"}}
```

## Response Format

The API uses Server-Sent Events (SSE) for streaming responses. Each event contains JSON data with the following structure:

### Event Types

1. **input_guard_rail**: Input validation results
2. **reasoning_node**: AI reasoning and analysis
3. **output_guard_rail**: Final response processing

### Event Data Structure

```json
{
  "node_name": {
    "messages": [...],
    "processing_status": "status",
    "analysis_result": {...},
    "recommendations": [...],
    "error_message": "string or null"
  }
}
```

### Processing Status Values

- `input_validated`: Input successfully validated
- `analysis_completed`: AI analysis completed
- `completed_successfully`: Final response ready
- `error_processed`: Error handled gracefully
- `completed_with_fallback`: Response with fallback content

## Error Handling

The API handles errors gracefully and provides user-friendly error messages:

- **400 Bad Request**: Invalid request format
- **500 Internal Server Error**: Server-side processing error

Error responses are included in the stream as `error_message` fields.

## Example Usage

### Car Diagnostics

```bash
curl -X POST "http://localhost:8083/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "meu carro está fazendo um barulho estranho",
    "thread_id": "diagnosis-123"
  }'
```

### Travel Planning

```bash
curl -X POST "http://localhost:8083/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "quero viajar para o sul do Brasil, onde você recomenda?",
    "thread_id": "travel-789"
  }'
```

### Trip Feasibility Check

```bash
curl -X POST "http://localhost:8083/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "posso viajar 500km com 30 litros de gasolina?",
    "thread_id": "trip-check-456"
  }'
```

## Development

### Running the API

```bash
# Using UV
uv run main.py

# Using Docker
docker-compose up

# Manual Docker
docker build -f docker/Dockerfile -t car-system-ai .
docker run -p 8083:8083 car-system-ai
```

### Testing the API

```bash
# Health check
curl http://localhost:8083/
curl http://localhost:8083/health

# Chat endpoint
curl -X POST "http://localhost:8083/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "thread_id": "test-123"}' \
  --no-buffer -N
```

