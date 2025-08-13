// SPDX-License-Identifier: MIT
export interface ImageAnalysisRequest {
  imagePath: string;
  prompt: string;
}

export interface ImageAnalysisResponse {
  analysis: string;
  model: string;
  timestamp: string;
}

export interface OpenRouterMessage {
  role: 'user' | 'assistant' | 'system';
  content: Array<{
    type: 'text' | 'image_url';
    text?: string;
    image_url?: {
      url: string;
    };
  }>;
}

export interface OpenRouterRequest {
  model: string;
  messages: OpenRouterMessage[];
  max_tokens?: number;
  temperature?: number;
}

export interface OpenRouterResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
  model: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface Config {
  openRouterApiKey: string;
  logLevel: string;
  maxImageSizeMB: number;
  geminiModel: string;
}