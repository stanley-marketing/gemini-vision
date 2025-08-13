// SPDX-License-Identifier: MIT
import { config as dotenvConfig } from 'dotenv';
import { Config } from '../types/index.js';
import { logger } from './logger.js';

dotenvConfig();

export function getConfig(): Config {
  const openRouterApiKey = process.env.OPENROUTER_API_KEY;
  
  if (!openRouterApiKey) {
    throw new Error('OPENROUTER_API_KEY environment variable is required');
  }

  const config: Config = {
    openRouterApiKey,
    logLevel: process.env.LOG_LEVEL || 'info',
    maxImageSizeMB: parseInt(process.env.MAX_IMAGE_SIZE_MB || '10'),
    geminiModel: process.env.GEMINI_MODEL || 'google/gemini-2.5-pro'
  };

  logger.debug('Configuration loaded:', {
    ...config,
    openRouterApiKey: '***' // Hide API key in logs
  });

  return config;
}