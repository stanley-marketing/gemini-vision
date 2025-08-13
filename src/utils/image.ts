// SPDX-License-Identifier: MIT
import { promises as fs } from 'fs';
import { logger } from './logger.js';

export class ImageUtils {
  private static readonly SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
  private static readonly MAX_SIZE_BYTES = (process.env.MAX_IMAGE_SIZE_MB ? parseInt(process.env.MAX_IMAGE_SIZE_MB) : 10) * 1024 * 1024;

  static async validateImagePath(imagePath: string): Promise<void> {
    try {
      const stats = await fs.stat(imagePath);
      
      if (!stats.isFile()) {
        throw new Error(`Path is not a file: ${imagePath}`);
      }

      if (stats.size > this.MAX_SIZE_BYTES) {
        throw new Error(`Image file too large: ${stats.size} bytes (max: ${this.MAX_SIZE_BYTES} bytes)`);
      }

      const extension = imagePath.toLowerCase().substring(imagePath.lastIndexOf('.'));
      if (!this.SUPPORTED_FORMATS.includes(extension)) {
        throw new Error(`Unsupported image format: ${extension}. Supported formats: ${this.SUPPORTED_FORMATS.join(', ')}`);
      }

      logger.debug(`Image validation passed for: ${imagePath}`);
    } catch (error) {
      if (error instanceof Error && error.message.includes('ENOENT')) {
        throw new Error(`Image file not found: ${imagePath}`);
      }
      throw error;
    }
  }

  static async imageToBase64(imagePath: string): Promise<string> {
    try {
      await this.validateImagePath(imagePath);
      
      const imageBuffer = await fs.readFile(imagePath);
      const base64String = imageBuffer.toString('base64');
      
      const extension = imagePath.toLowerCase().substring(imagePath.lastIndexOf('.') + 1);
      const mimeType = this.getMimeType(extension);
      
      logger.debug(`Converted image to base64: ${imagePath} (${imageBuffer.length} bytes)`);
      
      return `data:${mimeType};base64,${base64String}`;
    } catch (error) {
      logger.error(`Failed to convert image to base64: ${imagePath}`, error);
      throw error;
    }
  }

  private static getMimeType(extension: string): string {
    const mimeTypes: Record<string, string> = {
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'gif': 'image/gif',
      'webp': 'image/webp',
      'bmp': 'image/bmp'
    };
    
    return mimeTypes[extension] || 'image/jpeg';
  }
}