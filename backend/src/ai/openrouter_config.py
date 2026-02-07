"""
OpenRouter Configuration Module (DEPRECATED)

This module is deprecated after switching to Cohere API.
Kept for reference during transition period.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from openai import OpenAI


class OpenRouterConfig(BaseModel):
    """
    Configuration model for OpenRouter API
    """
    api_key: str = Field(
        default="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",
        description="OpenRouter API key"
    )
    model: str = Field(
        default="tngtech/deepseek-r1t2-chimera:free",
        description="Model to use for AI processing"
    )
    base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="Base URL for OpenRouter API"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for response randomness"
    )


def get_openrouter_client() -> OpenAI:
    """
    Create and return an OpenRouter client configured with the specified settings.

    Returns:
        OpenAI: Configured OpenAI client pointing to OpenRouter
    """
    config = OpenRouterConfig()
    client = OpenAI(
        api_key=config.api_key,
        base_url=config.base_url
    )
    return client


def get_default_model() -> str:
    """
    Get the default model name for OpenRouter.

    Returns:
        str: The default model name
    """
    config = OpenRouterConfig()
    return config.model


# Global client instance
openrouter_client = get_openrouter_client()