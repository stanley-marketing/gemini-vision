# Security Policy

## Reporting Security Vulnerabilities

Report vulnerabilities to security@progressus-software.com. Do not file public issues for suspected vulnerabilities.

We acknowledge within 2 business days. Supported versions: latest two minor releases.

## Security Guidelines

- Never commit API keys, tokens, or other secrets to the repository
- Use environment variables for all sensitive configuration
- Do not upload PII or confidential data through this service
- Review third-party dependencies regularly for known vulnerabilities
- Keep your OpenRouter API key secure and rotate it periodically

## Safe Usage

- Only analyze images you have permission to process
- Be aware that images are sent to OpenRouter/Google's Gemini service
- Do not include sensitive information in image analysis prompts
- Use appropriate rate limiting to avoid service abuse

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Features

- Input validation for all image formats and sizes
- Secure handling of API credentials through environment variables
- Comprehensive error handling to prevent information leakage
- Rate limiting and timeout protection
- Logging that excludes sensitive information