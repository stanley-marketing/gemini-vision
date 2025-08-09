#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

import { getConfig } from './utils/config.js';
import { logger } from './utils/logger.js';
import { ImageUtils } from './utils/image.js';
import { OpenRouterService } from './services/openrouter.js';
import { ImageAnalysisRequest, ImageAnalysisResponse } from './types/index.js';

class GeminiVisionMCPServer {
  private server: Server;
  private openRouterService: OpenRouterService;

  constructor() {
    this.server = new Server(
      {
        name: 'gemini-vision-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    const config = getConfig();
    this.openRouterService = new OpenRouterService(config);
    
    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'analyze_image',
            description: 'Analyze an image using Gemini 2.5 Pro through OpenRouter. Provide detailed visual analysis, object detection, text extraction, and answer questions about the image content.',
            inputSchema: {
              type: 'object',
              properties: {
                imagePath: {
                  type: 'string',
                  description: 'Absolute path to the image file to analyze. Supports JPG, PNG, GIF, WebP, and BMP formats.',
                },
                prompt: {
                  type: 'string',
                  description: 'Question or instruction for analyzing the image. Be specific about what you want to know about the image.',
                },
              },
              required: ['imagePath', 'prompt'],
            },
          } as Tool,
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      if (name === 'analyze_image') {
        return await this.handleImageAnalysis(args as ImageAnalysisRequest);
      }

      throw new Error(`Unknown tool: ${name}`);
    });
  }

  private async handleImageAnalysis(request: ImageAnalysisRequest) {
    try {
      logger.info(`Starting image analysis for: ${request.imagePath}`);
      logger.debug(`Analysis prompt: ${request.prompt}`);

      // Validate and convert image to base64
      const imageBase64 = await ImageUtils.imageToBase64(request.imagePath);
      
      // Analyze image using OpenRouter/Gemini
      const analysis = await this.openRouterService.analyzeImage(imageBase64, request.prompt);
      
      const response: ImageAnalysisResponse = {
        analysis,
        model: 'google/gemini-2.0-flash-exp',
        timestamp: new Date().toISOString(),
      };

      logger.info(`Image analysis completed successfully for: ${request.imagePath}`);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(response, null, 2),
          },
        ],
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      logger.error(`Image analysis failed for ${request.imagePath}:`, errorMessage);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              error: errorMessage,
              imagePath: request.imagePath,
              timestamp: new Date().toISOString(),
            }, null, 2),
          },
        ],
        isError: true,
      };
    }
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      logger.error('MCP Server error:', error);
    };

    process.on('SIGINT', async () => {
      logger.info('Received SIGINT, shutting down gracefully...');
      await this.server.close();
      process.exit(0);
    });

    process.on('SIGTERM', async () => {
      logger.info('Received SIGTERM, shutting down gracefully...');
      await this.server.close();
      process.exit(0);
    });
  }

  async start(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    logger.info('Gemini Vision MCP Server started successfully');
  }
}

// Start the server
async function main() {
  try {
    const server = new GeminiVisionMCPServer();
    await server.start();
  } catch (error) {
    logger.error('Failed to start MCP server:', error);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    logger.error('Unhandled error in main:', error);
    process.exit(1);
  });
}