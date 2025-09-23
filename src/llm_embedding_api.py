#!/usr/bin/env python3
"""
LLM Embedding API Service - Eugene Schwartz VSL Analyzer
Lightweight service for handling LLM requests and embeddings
"""

import os
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# FastAPI app
app = FastAPI(
    title="LLM Embedding Service",
    description="Multi-LLM service for embeddings and text processing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class EmbeddingRequest(BaseModel):
    text: str
    model: str = "text-embedding-ada-002"

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    model: str
    usage: Dict[str, Any]
    timestamp: str

class LLMRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: str = "gpt-4o-mini"
    max_tokens: int = 4000
    temperature: float = 0.1

class LLMResponse(BaseModel):
    content: str
    model: str
    usage: Dict[str, Any]
    timestamp: str

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "openai": bool(OPENAI_API_KEY),
            "anthropic": bool(ANTHROPIC_API_KEY),
            "gemini": bool(GEMINI_API_KEY)
        },
        "timestamp": datetime.now().isoformat()
    }

# Embedding endpoint
@app.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """Create embeddings using OpenAI"""

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, "OpenAI API key not configured")

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "input": request.text.replace("\\n", " "),
                "model": request.model
            }

            async with session.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(status_code=response.status, f"OpenAI API error: {error_text}")

                data = await response.json()

                return EmbeddingResponse(
                    embedding=data["data"][0]["embedding"],
                    model=request.model,
                    usage=data.get("usage", {}),
                    timestamp=datetime.now().isoformat()
                )

    except Exception as e:
        raise HTTPException(status_code=500, f"Embedding generation failed: {str(e)}")

# LLM completion endpoint
@app.post("/completions", response_model=LLMResponse)
async def create_completion(request: LLMRequest):
    """Create completion using specified LLM"""

    if "gpt" in request.model.lower():
        return await openai_completion(request)
    elif "claude" in request.model.lower():
        return await anthropic_completion(request)
    else:
        raise HTTPException(status_code=400, f"Unsupported model: {request.model}")

async def openai_completion(request: LLMRequest) -> LLMResponse:
    """OpenAI completion"""

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, "OpenAI API key not configured")

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": request.model,
                "messages": request.messages,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature
            }

            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(status_code=response.status, f"OpenAI API error: {error_text}")

                data = await response.json()

                return LLMResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=request.model,
                    usage=data.get("usage", {}),
                    timestamp=datetime.now().isoformat()
                )

    except Exception as e:
        raise HTTPException(status_code=500, f"OpenAI completion failed: {str(e)}")

async def anthropic_completion(request: LLMRequest) -> LLMResponse:
    """Anthropic Claude completion"""

    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, "Anthropic API key not configured")

    try:
        # Convert messages format for Anthropic
        system_message = ""
        user_messages = []

        for msg in request.messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        async with aiohttp.ClientSession() as session:
            headers = {
                "x-api-key": ANTHROPIC_API_KEY,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": request.max_tokens,
                "messages": user_messages,
                "system": system_message
            }

            async with session.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(status_code=response.status, f"Anthropic API error: {error_text}")

                data = await response.json()

                return LLMResponse(
                    content=data["content"][0]["text"],
                    model="claude-3-haiku",
                    usage=data.get("usage", {}),
                    timestamp=datetime.now().isoformat()
                )

    except Exception as e:
        raise HTTPException(status_code=500, f"Anthropic completion failed: {str(e)}")

# Statistics endpoint
@app.get("/stats")
async def get_stats():
    """Get service statistics"""
    return {
        "service": "LLM Embedding API",
        "version": "1.0.0",
        "providers": {
            "openai": bool(OPENAI_API_KEY),
            "anthropic": bool(ANTHROPIC_API_KEY),
            "gemini": bool(GEMINI_API_KEY)
        },
        "endpoints": {
            "embeddings": "/embeddings",
            "completions": "/completions",
            "health": "/health",
            "stats": "/stats"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)