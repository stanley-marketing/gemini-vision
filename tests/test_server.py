"""Tests for the Gemini Vision MCP Server."""

import asyncio
import base64
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PIL import Image

from gemini_vision.server import GeminiVisionServer


@pytest.fixture
def temp_image():
    """Create a temporary test image."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        # Create a simple test image
        img = Image.new("RGB", (100, 100), color="red")
        img.save(tmp.name)
        yield tmp.name
    
    # Cleanup
    os.unlink(tmp.name)


@pytest.fixture
def server():
    """Create a test server instance."""
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key"}):
        return GeminiVisionServer()


class TestGeminiVisionServer:
    """Test cases for GeminiVisionServer."""
    
    def test_initialization_without_api_key(self):
        """Test server initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
                GeminiVisionServer()
    
    def test_initialization_with_api_key(self, server):
        """Test server initialization succeeds with API key."""
        assert server.api_key == "test_key"
        assert server.server is not None
    
    @pytest.mark.asyncio
    async def test_list_tools(self, server):
        """Test listing available tools."""
        tools = await server.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "analyze_image"
        assert "image_path" in tools[0].inputSchema["properties"]
        assert "prompt" in tools[0].inputSchema["properties"]
    
    def test_validate_image_path_valid(self, server, temp_image):
        """Test image path validation with valid image."""
        path = server._validate_image_path(temp_image)
        assert path.exists()
        assert path.is_file()
    
    def test_validate_image_path_nonexistent(self, server):
        """Test image path validation with non-existent file."""
        with pytest.raises(FileNotFoundError):
            server._validate_image_path("/nonexistent/path.png")
    
    def test_validate_image_path_unsupported_format(self, server):
        """Test image path validation with unsupported format."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"test content")
            tmp.flush()
            
            try:
                with pytest.raises(ValueError, match="Unsupported image format"):
                    server._validate_image_path(tmp.name)
            finally:
                os.unlink(tmp.name)
    
    def test_encode_image(self, server, temp_image):
        """Test image encoding to base64."""
        path = Path(temp_image)
        encoded = server._encode_image(path)
        
        # Verify it's valid base64
        decoded = base64.b64decode(encoded)
        assert len(decoded) > 0
    
    def test_get_mime_type(self, server):
        """Test MIME type detection."""
        assert server._get_mime_type(Path("test.png")) == "image/png"
        assert server._get_mime_type(Path("test.jpg")) == "image/jpeg"
        assert server._get_mime_type(Path("test.jpeg")) == "image/jpeg"
        assert server._get_mime_type(Path("test.gif")) == "image/gif"
        assert server._get_mime_type(Path("test.webp")) == "image/webp"
    
    @pytest.mark.asyncio
    async def test_call_gemini_api_success(self, server):
        """Test successful Gemini API call."""
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": "This is a test image analysis."
                    }
                }
            ]
        }
        
        with patch("aiohttp.ClientSession.post") as mock_post:
            mock_resp = AsyncMock()
            mock_resp.status = 200
            mock_resp.json = AsyncMock(return_value=mock_response)
            mock_post.return_value.__aenter__.return_value = mock_resp
            
            result = await server._call_gemini_api(
                "Test prompt", "base64_image_data", "image/png"
            )
            
            assert result == "This is a test image analysis."
    
    @pytest.mark.asyncio
    async def test_call_gemini_api_failure(self, server):
        """Test Gemini API call failure."""
        with patch("aiohttp.ClientSession.post") as mock_post:
            mock_resp = AsyncMock()
            mock_resp.status = 400
            mock_resp.text = AsyncMock(return_value="Bad Request")
            mock_post.return_value.__aenter__.return_value = mock_resp
            
            with pytest.raises(Exception, match="API request failed"):
                await server._call_gemini_api(
                    "Test prompt", "base64_image_data", "image/png"
                )
    
    @pytest.mark.asyncio
    async def test_call_tool_analyze_image_success(self, server, temp_image):
        """Test successful analyze_image tool call."""
        # Mock the API call
        with patch.object(server, "_call_gemini_api") as mock_api:
            mock_api.return_value = "Test analysis result"
            
            # Create mock request
            mock_request = MagicMock()
            mock_request.params.name = "analyze_image"
            mock_request.params.arguments = {
                "image_path": temp_image,
                "prompt": "Test prompt"
            }
            
            result = await server.call_tool(mock_request)
            
            assert not result.isError
            assert len(result.content) == 1
            assert "Test analysis result" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_call_tool_missing_image_path(self, server):
        """Test analyze_image tool call with missing image_path."""
        mock_request = MagicMock()
        mock_request.params.name = "analyze_image"
        mock_request.params.arguments = {"prompt": "Test prompt"}
        
        result = await server.call_tool(mock_request)
        
        assert result.isError
        assert "image_path parameter is required" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self, server):
        """Test call to unknown tool."""
        mock_request = MagicMock()
        mock_request.params.name = "unknown_tool"
        mock_request.params.arguments = {}
        
        result = await server.call_tool(mock_request)
        
        assert result.isError
        assert "Unknown tool" in result.content[0].text


@pytest.mark.asyncio
async def test_main_function():
    """Test the main function runs without errors."""
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key"}):
        with patch("gemini_vision.server.stdio_server") as mock_stdio:
            mock_stdio.return_value.__aenter__.return_value = (
                AsyncMock(), AsyncMock()
            )
            
            # Mock the server run method to avoid infinite loop
            with patch.object(GeminiVisionServer, "__init__", return_value=None):
                mock_server = MagicMock()
                mock_server.server.run = AsyncMock()
                mock_server.server.get_capabilities = MagicMock(return_value={})
                
                with patch("gemini_vision.server.GeminiVisionServer", return_value=mock_server):
                    from gemini_vision.server import main
                    
                    # This should not raise an exception
                    await asyncio.wait_for(main(), timeout=1.0)