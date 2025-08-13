# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""
Usage examples for the Gemini Vision MCP Server.

This file demonstrates various ways to use the image analysis tool
with different types of prompts and use cases.
"""

# Example tool calls that would be made by Claude Desktop or OpenCode

USAGE_EXAMPLES = [
    {
        "name": "Basic Image Description",
        "description": "Get a general description of any image",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/your/image.jpg"
            }
        },
        "expected_output": "Detailed description of the image contents, objects, people, scenery, etc."
    },
    
    {
        "name": "Screenshot Analysis",
        "description": "Analyze UI elements in a screenshot",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/screenshot.png",
                "prompt": "What UI elements are visible in this screenshot? List all buttons, menus, text fields, and other interface components you can see."
            }
        },
        "expected_output": "Detailed list of UI components, their positions, and functionality"
    },
    
    {
        "name": "Code Screenshot Analysis",
        "description": "Analyze code in a screenshot",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/code_screenshot.png",
                "prompt": "What programming language is this? Describe the code structure, functions, and any potential issues you can identify."
            }
        },
        "expected_output": "Programming language identification, code structure analysis, potential issues"
    },
    
    {
        "name": "Chart/Graph Analysis",
        "description": "Analyze data visualizations",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/chart.png",
                "prompt": "What type of chart is this? What are the key trends, patterns, and insights shown in this data visualization?"
            }
        },
        "expected_output": "Chart type identification, trend analysis, key insights from the data"
    },
    
    {
        "name": "Document OCR",
        "description": "Extract text from document images",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/document.jpg",
                "prompt": "Please extract and transcribe all the text visible in this document image. Maintain the original formatting as much as possible."
            }
        },
        "expected_output": "Transcribed text from the document with preserved formatting"
    },
    
    {
        "name": "Error Message Analysis",
        "description": "Analyze error messages in screenshots",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/error_screenshot.png",
                "prompt": "What error is shown in this screenshot? What might be causing this error and how can it be resolved?"
            }
        },
        "expected_output": "Error identification, potential causes, and suggested solutions"
    },
    
    {
        "name": "Design Review",
        "description": "Review UI/UX design mockups",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/design_mockup.png",
                "prompt": "Review this UI design. Comment on the layout, color scheme, typography, user experience, and suggest any improvements."
            }
        },
        "expected_output": "Design critique with suggestions for improvement"
    },
    
    {
        "name": "Accessibility Analysis",
        "description": "Check accessibility of UI designs",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/interface.png",
                "prompt": "Analyze this interface for accessibility. Check color contrast, text readability, button sizes, and other accessibility considerations."
            }
        },
        "expected_output": "Accessibility assessment with specific recommendations"
    },
    
    {
        "name": "Diagram Explanation",
        "description": "Explain technical diagrams",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/architecture_diagram.png",
                "prompt": "Explain this technical diagram. What system or process does it represent? Describe the components and their relationships."
            }
        },
        "expected_output": "Detailed explanation of the diagram's components and relationships"
    },
    
    {
        "name": "Meme/Social Media Analysis",
        "description": "Understand memes and social media content",
        "tool_call": {
            "name": "analyze_image",
            "arguments": {
                "image_path": "/path/to/meme.jpg",
                "prompt": "Explain this meme or social media image. What's the joke or message? What cultural references does it make?"
            }
        },
        "expected_output": "Explanation of the meme's humor, cultural context, and references"
    }
]

def print_examples():
    """Print all usage examples in a readable format."""
    print("🖼️  Gemini Vision MCP Server - Usage Examples")
    print("=" * 60)
    
    for i, example in enumerate(USAGE_EXAMPLES, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Description: {example['description']}")
        print(f"   Tool Call:")
        print(f"     Name: {example['tool_call']['name']}")
        print(f"     Arguments:")
        for key, value in example['tool_call']['arguments'].items():
            print(f"       {key}: {value}")
        print(f"   Expected Output: {example['expected_output']}")
        print("-" * 60)

if __name__ == "__main__":
    print_examples()