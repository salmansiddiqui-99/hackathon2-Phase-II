"""
Cohere Configuration Module

This module handles the configuration for Cohere API access using the OpenAI-compatible API layer including:
- API Key: SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM
- Model: command-r7b-12-2024
- Base URL: https://api.cohere.ai/compatibility/v1
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from openai import OpenAI


class CohereConfig(BaseModel):
    """
    Configuration model for Cohere API using OpenAI compatibility layer
    """
    api_key: str = Field(
        default="SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM",
        description="Cohere API key for compatibility layer"
    )
    model: str = Field(
        default="command-r7b-12-2024",
        description="Model to use for AI processing"
    )
    base_url: str = Field(
        default="https://api.cohere.ai/compatibility/v1",
        description="Base URL for Cohere API compatibility layer"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for response randomness"
    )


def get_cohere_client() -> OpenAI:
    """
    Create and return a Cohere client configured with the specified settings
    using the OpenAI compatibility layer.

    Returns:
        OpenAI: Configured OpenAI client pointing to Cohere
    """
    config = CohereConfig()
    client = OpenAI(
        api_key=config.api_key,
        base_url=config.base_url
    )
    return client


def get_default_model() -> str:
    """
    Get the default model name for Cohere.

    Returns:
        str: The default model name
    """
    config = CohereConfig()
    return config.model


# Global client instance
cohere_client = get_cohere_client()