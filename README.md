# Gemini Vision MCP Server

A Model Context Protocol (MCP) server that enables AI assistants like Claude and OpenCode to analyze images using Google's Gemini 2.5 Pro model through the OpenRouter API.

## Features

- **Image Analysis**: Analyze images with detailed visual descriptions, object detection, and text extraction
- **Multiple Formats**: Supports JPG, PNG, GIF, WebP, and BMP image formats
- **Flexible Prompting**: Ask specific questions about image content
- **Error Handling**: Robust error handling with detailed logging
- **Type Safety**: Full TypeScript implementation with comprehensive type definitions
- **Production Ready**: Includes proper logging, validation, and configuration management

## Prerequisites

- Node.js 18.0.0 or higher
- An OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai/keys))

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the environment template and configure your API key:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

5. Build the project:
   ```bash
   npm run build
   ```

## Usage

### Running the Server

For development:
```bash
npm run dev
```

For production:
```bash
npm start
```

### MCP Client Configuration

To use this server with Claude Desktop or other MCP clients, add the following to your MCP configuration:

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "gemini-vision": {
      "command": "node",
      "args": ["/path/to/gemini-vision-mcp-server/dist/index.js"],
      "env": {
        "OPENROUTER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**OpenCode:**
Add to your `AGENTS.md` file:
```markdown
## MCP Servers

### Gemini Vision
- **Command**: `node /path/to/gemini-vision-mcp-server/dist/index.js`
- **Description**: Image analysis using Gemini 2.5 Pro
- **Environment**: `OPENROUTER_API_KEY=your_api_key_here`
```

## Available Tools

### `analyze_image`

Analyzes an image using Gemini 2.5 Pro and returns detailed insights.

**Parameters:**
- `imagePath` (string, required): Absolute path to the image file
- `prompt` (string, required): Question or instruction for analyzing the image

**Example Usage:**
```typescript
{
  "name": "analyze_image",
  "arguments": {
    "imagePath": "/home/user/photos/vacation.jpg",
    "prompt": "Describe what you see in this image and identify any notable objects or people."
  }
}
```

**Response Format:**
```json
{
  "analysis": "Detailed analysis of the image...",
  "model": "google/gemini-2.0-flash-exp",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Example Prompts

Here are some effective prompts you can use:

- **General Description**: "Describe what you see in this image in detail."
- **Object Detection**: "List all the objects you can identify in this image."
- **Text Extraction**: "Extract and transcribe any text visible in this image."
- **Scene Analysis**: "What is the setting or location of this image?"
- **People Analysis**: "Describe the people in this image, including their actions and expressions."
- **Technical Analysis**: "Analyze the composition, lighting, and photographic techniques used."
- **Accessibility**: "Provide an accessibility description for this image."

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY` (required): Your OpenRouter API key
- `LOG_LEVEL` (optional): Logging level (`debug`, `info`, `warn`, `error`). Default: `info`
- `MAX_IMAGE_SIZE_MB` (optional): Maximum image size in MB. Default: `10`

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)

### Size Limits

- Maximum image size: 10MB (configurable via `MAX_IMAGE_SIZE_MB`)
- API timeout: 60 seconds

## Development

### Scripts

- `npm run build`: Compile TypeScript to JavaScript
- `npm run dev`: Run in development mode with hot reload
- `npm start`: Run the compiled server
- `npm run lint`: Run ESLint
- `npm run typecheck`: Run TypeScript type checking

### Project Structure

```
src/
├── index.ts              # Main server implementation
├── types/
│   └── index.ts          # TypeScript type definitions
├── utils/
│   ├── config.ts         # Configuration management
│   ├── logger.ts         # Logging utilities
│   └── image.ts          # Image processing utilities
└── services/
    └── openrouter.ts     # OpenRouter API service
```

## Error Handling

The server includes comprehensive error handling for:

- Invalid or missing API keys
- Unsupported image formats
- File not found errors
- Image size limits
- Network timeouts
- API rate limits

All errors are logged with appropriate detail levels and returned to the client with helpful error messages.

## Troubleshooting

### Common Issues

1. **"Invalid OpenRouter API key"**
   - Verify your API key is correct in the `.env` file
   - Ensure the environment variable is properly loaded

2. **"Image file not found"**
   - Check that the image path is absolute and correct
   - Verify file permissions allow reading

3. **"Unsupported image format"**
   - Ensure your image is in a supported format (JPG, PNG, GIF, WebP, BMP)

4. **"Image file too large"**
   - Reduce image size or increase `MAX_IMAGE_SIZE_MB` limit

5. **"Rate limit exceeded"**
   - Wait before making additional requests
   - Consider upgrading your OpenRouter plan

### Debug Mode

Enable debug logging to see detailed information:

```bash
LOG_LEVEL=debug npm run dev
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite and linting
6. Submit a pull request

## Support

- Create an issue on GitHub for bug reports or feature requests
- Check the logs for detailed error information
- Ensure your OpenRouter API key is valid and has sufficient credits