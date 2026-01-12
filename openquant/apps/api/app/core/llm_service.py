"""
LLM Service - Unified interface for chatmock and OpenAI
"""
from openai import AsyncOpenAI
from typing import AsyncGenerator, List, Dict, Optional
import logging

from app.core.config import Settings


class LLMService:
    """
    Unified LLM service supporting chatmock (local) and OpenAI.
    Uses OpenAI SDK with configurable base_url for compatibility.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)

        # Configure client based on provider
        if settings.llm_provider == "chatmock":
            self.client = AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url
            )
            self.logger.info(f"LLM Service initialized with chatmock at {settings.llm_base_url}")
        else:
            # Use OpenAI directly
            api_key = settings.openai_api_key or settings.llm_api_key
            self.client = AsyncOpenAI(api_key=api_key)
            self.logger.info("LLM Service initialized with OpenAI")

        self.model = settings.llm_model

    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """
        Non-streaming completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            json_mode: If True, request JSON output format

        Returns:
            Generated text content
        """
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature if temperature is not None else self.settings.llm_temperature,
                "max_tokens": max_tokens or self.settings.llm_max_tokens,
            }

            # Add JSON mode if supported and requested
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""

        except Exception as e:
            self.logger.error(f"LLM completion failed: {e}")
            raise

    async def stream(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None
    ) -> AsyncGenerator[str, None]:
        """
        Streaming completion for chat interfaces.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature

        Yields:
            Text chunks as they are generated
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.settings.llm_temperature,
                stream=True
            )

            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            self.logger.error(f"LLM streaming failed: {e}")
            raise

    async def complete_with_fallback(
        self,
        messages: List[Dict[str, str]],
        fallback_response: str = "I'm currently unable to process your request.",
        **kwargs
    ) -> str:
        """
        Completion with graceful fallback on error.

        Args:
            messages: List of message dicts
            fallback_response: Response to return on failure
            **kwargs: Additional arguments for complete()

        Returns:
            Generated text or fallback response
        """
        try:
            return await self.complete(messages, **kwargs)
        except Exception as e:
            self.logger.warning(f"LLM completion failed, using fallback: {e}")
            return fallback_response

    async def health_check(self) -> bool:
        """
        Check if LLM service is responsive.

        Returns:
            True if service is healthy
        """
        try:
            await self.complete(
                [{"role": "user", "content": "ping"}],
                max_tokens=5,
                temperature=0
            )
            return True
        except Exception as e:
            self.logger.error(f"LLM health check failed: {e}")
            return False
