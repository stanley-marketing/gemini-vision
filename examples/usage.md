# Gemini Vision MCP Server - Usage Examples

## Basic Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

3. **Start the server:**
   ```bash
   npm run dev
   ```

## MCP Client Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini-vision": {
      "command": "node",
      "args": ["/path/to/gemini-vision-mcp-server/src/index.ts"],
      "env": {
        "OPENROUTER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### OpenCode

Add to your `AGENTS.md`:

```markdown
## MCP Servers

### Gemini Vision
- **Command**: `tsx /path/to/gemini-vision-mcp-server/src/index.ts`
- **Description**: Image analysis using Gemini 2.5 Pro
- **Environment**: `OPENROUTER_API_KEY=your_api_key_here`
```

## Tool Usage Examples

### Basic Image Description

```json
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/photos/vacation.jpg",
    "prompt": "Describe what you see in this image in detail."
  }
}
```

### Object Detection

```json
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/screenshots/desktop.png",
    "prompt": "List all the objects and UI elements you can identify in this screenshot."
  }
}
```

### Text Extraction

```json
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/documents/receipt.jpg",
    "prompt": "Extract and transcribe all text visible in this image, including any numbers, dates, and amounts."
  }
}
```

### Technical Analysis

```json
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/photos/architecture.jpg",
    "prompt": "Analyze the architectural style, materials, and design elements visible in this building."
  }
}
```

### Accessibility Description

```json
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/images/chart.png",
    "prompt": "Provide a detailed accessibility description of this chart or graph, including all data points and trends."
  }
}
```

### Code Analysis

```json
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/screenshots/code.png",
    "prompt": "Analyze this code screenshot. What programming language is it? What does the code do? Are there any potential issues?"
  }
}
```

## Response Format

The server returns responses in this format:

```json
{
  "analysis": "Detailed analysis of the image...",
  "model": "google/gemini-2.0-flash-exp",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Error Handling

Common errors and solutions:

### "Invalid OpenRouter API key"
- Check your `.env` file
- Verify the API key is correct
- Ensure the environment variable is loaded

### "Image file not found"
- Use absolute paths
- Check file permissions
- Verify the file exists

### "Unsupported image format"
- Supported formats: JPG, PNG, GIF, WebP, BMP
- Convert your image to a supported format

### "Image file too large"
- Default limit: 10MB
- Resize your image or increase `MAX_IMAGE_SIZE_MB`

## Tips for Better Results

1. **Be specific in your prompts**: Instead of "What's in this image?", try "Describe the people, objects, and setting in this photograph."

2. **Use appropriate prompts for the content type**:
   - For screenshots: "What UI elements and text are visible?"
   - For documents: "Extract all text and identify the document type"
   - For charts: "Describe the data trends and key insights"

3. **Consider the image quality**: Higher resolution images generally produce better analysis results.

4. **Use absolute paths**: Always provide the full path to your image files.

## Debugging

Enable debug logging:

```bash
LOG_LEVEL=debug npm run dev
```

This will show detailed information about:
- Image validation
- API requests to OpenRouter
- Response processing
- Error details