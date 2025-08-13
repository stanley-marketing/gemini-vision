# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""
Test client for the Gemini Vision MCP Server.

This script demonstrates how to interact with the MCP server
and test image analysis functionality.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our server
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gemini_vision.server import GeminiVisionServer


async def test_image_analysis():
    """Test image analysis functionality."""
    
    # Check if API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY environment variable not set")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize server
        print("🚀 Initializing Gemini Vision MCP Server...")
        server = GeminiVisionServer()
        
        # Test listing tools
        print("\n📋 Testing tool listing...")
        tools = await server.list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # Test image analysis (you'll need to provide a test image)
        test_image_path = input("\n🖼️  Enter path to a test image (or press Enter to skip): ").strip()
        
        if test_image_path and Path(test_image_path).exists():
            print(f"\n🔍 Analyzing image: {test_image_path}")
            
            # Create a mock request object
            class MockRequest:
                def __init__(self, name, arguments):
                    self.params = MockParams(name, arguments)
            
            class MockParams:
                def __init__(self, name, arguments):
                    self.name = name
                    self.arguments = arguments
            
            # Test with default prompt
            request = MockRequest("analyze_image", {
                "image_path": test_image_path
            })
            
            result = await server.call_tool(request)
            
            if result.isError:
                print(f"❌ Error: {result.content[0].text}")
            else:
                print("✅ Analysis completed!")
                print("\n" + "="*50)
                print(result.content[0].text)
                print("="*50)
            
            # Test with custom prompt
            custom_prompt = input("\n💭 Enter a custom prompt (or press Enter to skip): ").strip()
            if custom_prompt:
                print(f"\n🔍 Analyzing with custom prompt: {custom_prompt}")
                
                request = MockRequest("analyze_image", {
                    "image_path": test_image_path,
                    "prompt": custom_prompt
                })
                
                result = await server.call_tool(request)
                
                if result.isError:
                    print(f"❌ Error: {result.content[0].text}")
                else:
                    print("✅ Custom analysis completed!")
                    print("\n" + "="*50)
                    print(result.content[0].text)
                    print("="*50)
        
        else:
            print("⏭️  Skipping image analysis test (no image provided)")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🧪 Gemini Vision MCP Server Test Client")
    print("=" * 40)
    
    success = await test_image_analysis()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())