import axios, { AxiosResponse } from 'axios';
import { OpenRouterRequest, OpenRouterResponse, Config } from '../types/index.js';
import { logger } from '../utils/logger.js';

export class OpenRouterService {
  private readonly apiKey: string;
  private readonly baseURL = process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';
  private readonly model: string;

  constructor(config: Config) {
    this.apiKey = config.openRouterApiKey;
    this.model = config.geminiModel;
  }

  async analyzeImage(imageBase64: string, prompt: string): Promise<string> {
    const request: OpenRouterRequest = {
      model: this.model,
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: prompt
            },
            {
              type: 'image_url',
              image_url: {
                url: imageBase64
              }
            }
          ]
        }
      ],
      max_tokens: 4000,
      temperature: 0.1
    };

    try {
      logger.debug(`Sending request to OpenRouter with model: ${this.model}`);
      
      const response: AxiosResponse<OpenRouterResponse> = await axios.post(
        `${this.baseURL}/chat/completions`,
        request,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/your-username/gemini-vision-mcp',
            'X-Title': 'Gemini Vision MCP Server'
          },
          timeout: 60000 // 60 second timeout
        }
      );

      if (!response.data.choices || response.data.choices.length === 0) {
        throw new Error('No response choices returned from OpenRouter');
      }

      const analysis = response.data.choices[0].message.content;
      
      logger.info(`Image analysis completed successfully using ${response.data.model}`);
      logger.debug(`Token usage:`, response.data.usage);
      
      return analysis;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const status = error.response?.status;
        const statusText = error.response?.statusText;
        const errorData = error.response?.data;
        
        logger.error(`OpenRouter API error: ${status} ${statusText}`, errorData);
        
        if (status === 401) {
          throw new Error('Invalid OpenRouter API key. Please check your OPENROUTER_API_KEY environment variable.');
        } else if (status === 429) {
          throw new Error('Rate limit exceeded. Please try again later.');
        } else if (status === 400) {
          throw new Error(`Bad request: ${errorData?.error?.message || 'Invalid request format'}`);
        } else {
          throw new Error(`OpenRouter API error: ${status} ${statusText}`);
        }
      } else {
        logger.error('Unexpected error during image analysis:', error);
        throw new Error(`Failed to analyze image: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    }
  }
}