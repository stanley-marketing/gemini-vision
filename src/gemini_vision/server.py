#!/usr/bin/env python3
"""
Gemini Vision MCP Server

An MCP server that provides image analysis capabilities using Gemini 2.5 Pro
through OpenRouter API. This enables Claude Desktop and OpenCode to analyze
images even when the primary AI model doesn't have native image viewing capabilities.
"""

import asyncio
import base64
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import aiohttp
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("gemini_vision.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("gemini-vision-mcp")

# Supported image formats
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
GEMINI_MODEL = "google/gemini-2.0-flash-exp"

class GeminiVisionServer:
    """MCP Server for Gemini Vision image analysis."""
    
    def __init__(self):
        self.server = Server("gemini-vision")
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            logger.error("OPENROUTER_API_KEY environment variable not set")
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        # Register handlers
        self.server.list_tools = self.list_tools
        self.server.call_tool = self.call_tool
        
        logger.info("Gemini Vision MCP Server initialized")
    
    async def list_tools(self) -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="analyze_image",
                description="Analyze an image using Gemini 2.5 Pro model. Provide a prompt describing what you want to know about the image and the path to the image file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Path to the image file to analyze"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "Prompt describing what you want to know about the image",
                            "default": "Describe this image in detail"
                        }
                    },
                    "required": ["image_path"]
                }
            )
        ]
    
    def _validate_image_path(self, image_path: str) -> Path:
        """Validate image path and format."""
        try:
            path = Path(image_path).resolve()
            
            if not path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            if not path.is_file():
                raise ValueError(f"Path is not a file: {image_path}")
            
            if path.suffix.lower() not in SUPPORTED_FORMATS:
                raise ValueError(
                    f"Unsupported image format: {path.suffix}. "
                    f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
                )
            
            return path
            
        except Exception as e:
            logger.error(f"Image validation failed: {e}")
            raise
    
    def _encode_image(self, image_path: Path) -> str:
        """Encode image to base64."""
        try:
            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                logger.info(f"Successfully encoded image: {image_path}")
                return encoded
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            raise
    
    def _get_mime_type(self, image_path: Path) -> str:
        """Get MIME type for image."""
        extension = image_path.suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        return mime_types.get(extension, "image/jpeg")
    
    async def _call_gemini_api(self, prompt: str, image_base64: str, mime_type: str) -> str:
        """Call Gemini API through OpenRouter."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo/gemini-vision-mcp",
            "X-Title": "Gemini Vision MCP Server"
        }
        
        payload = {
            "model": GEMINI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"API request failed: {response.status} - {error_text}")
                        raise Exception(f"API request failed: {response.status} - {error_text}")
                    
                    result = await response.json()
                    
                    if "choices" not in result or not result["choices"]:
                        raise Exception("No response from Gemini API")
                    
                    content = result["choices"][0]["message"]["content"]
                    logger.info("Successfully received response from Gemini API")
                    return content
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error calling Gemini API: {e}")
            raise Exception(f"Network error: {e}")
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise
    
    async def call_tool(self, request: CallToolRequest) -> CallToolResult:
        """Handle tool calls."""
        try:
            if request.params.name == "analyze_image":
                # Extract parameters
                image_path = request.params.arguments.get("image_path")
                prompt = request.params.arguments.get("prompt", "Describe this image in detail")
                
                if not image_path:
                    raise ValueError("image_path parameter is required")
                
                logger.info(f"Analyzing image: {image_path} with prompt: {prompt}")
                
                # Validate image
                validated_path = self._validate_image_path(image_path)
                
                # Encode image
                image_base64 = self._encode_image(validated_path)
                mime_type = self._get_mime_type(validated_path)
                
                # Call Gemini API
                analysis = await self._call_gemini_api(prompt, image_base64, mime_type)
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Image Analysis for: {image_path}\n\nPrompt: {prompt}\n\nAnalysis:\n{analysis}"
                        )
                    ]
                )
            
            else:
                raise ValueError(f"Unknown tool: {request.params.name}")
                
        except Exception as e:
            logger.error(f"Tool call failed: {e}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error: {str(e)}"
                    )
                ],
                isError=True
            )

async def main():
    """Main entry point for the MCP server."""
    try:
        # Initialize server
        vision_server = GeminiVisionServer()
        
        # Run server
        async with stdio_server() as (read_stream, write_stream):
            await vision_server.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="gemini-vision",
                    server_version="1.0.0",
                    capabilities=vision_server.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())