"""
Client that launches the repo MCP server (stdio) and creates a React-style agent 
using ChatGoogleGenerativeAI (Gemini).

Before running, set GOOGLE_API_KEY in your .env file.

Usage:
    python client.py --repo-path /absolute/path/to/repo
"""
import asyncio
import os
import argparse
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load env vars
load_dotenv()
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"

# CLI args
parser = argparse.ArgumentParser()
parser.add_argument("--repo-path", type=str, default=os.getcwd(),
                    help="Path to the repository/folder the server should expose.")
args = parser.parse_args()


def extract_text_content(result):
    """Extract text content from MCP result, handling both string and TextContent formats."""
    if not result:
        return ""
    
    if hasattr(result, 'content'):
        content = result.content
        if isinstance(content, list) and content:
            return content[0].text if hasattr(content[0], 'text') else str(content[0])
        elif hasattr(content, 'text'):
            return content.text
        else:
            return str(content)
    else:
        return str(result)


async def find_python_files(client):
    """Find Python files in the repository (root + some common subdirs)."""
    print("\n" + "="*50)
    print("🐍 FINDING PYTHON FILES")
    print("="*50)

    python_files = []

    # We'll scan just a few common folders
    for subdir in ["", "tools", "clients"]:
        try:
            async with client.session("repo") as session:
                list_result = await session.call_tool("count_files", {"relative_path": subdir})
                print(f"Scanned {subdir or '.'}, found count: {list_result}")

                # Try reading directory files (basic heuristic)
                for candidate in ["client.py", "doctools.py"]:
                    test_path = f"{subdir}/{candidate}" if subdir else candidate
                    file_resp = await session.call_tool("read_file", {"relpath": test_path})
                    content = extract_text_content(file_resp)
                    if file_resp and content and not content.startswith("ERROR"):
                        python_files.append(test_path)
                        print(f"✅ Found Python file: {test_path}")
        except Exception as e:
            print(f"❌ Error scanning {subdir}: {e}")

    return python_files


async def main():
    repo_path = os.path.abspath(args.repo_path)
    print(f"🚀 Starting MCP Client")
    print(f"📁 Repository path: {repo_path}")
    
    # Path to MCP server script
    server_script = "/Users/jayanth/Desktop/chatwithfile/servers/doctools.py"
    print(f"🔧 Server script: {server_script}")
    
    if not os.path.exists(server_script):
        print(f"❌ ERROR: Server script not found at {server_script}")
        return
    
    client = MultiServerMCPClient(
        {
            "repo": {
                "command": "python",
                "args": [server_script, "--base-dir", repo_path],
                "transport": "stdio",
            }
        }
    )
    
    try:
        # Get tools
        tools = await client.get_tools()
        print(f"\n🛠️  Available tools from MCP server: {[t.name for t in tools]}")
        
        # Find Python files
        python_files = await find_python_files(client)
        
        # Configure Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ ERROR: GOOGLE_API_KEY not found in environment variables")
            return
            
        model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash")
        agent = create_react_agent(model, tools)
        
        print("\n" + "="*50)
        print("🤖 RUNNING AGENT TASKS")
        print("="*50)
        
        # Task 1: Count files
        print("\n📊 Task 1: Counting files...")
        resp = await agent.ainvoke({
            "messages": [{"role": "user", "content": "How many files are in the repository? Use count_files tool."}]
        })
        print("Agent response (file count):")
        print(resp["messages"][-1].content)
        
        # Task 2: Read and summarize a Python file
        if python_files:
            target_file = python_files[0]
            print(f"\n📄 Task 2: Reading and summarizing {target_file}...")
            
            async with client.session("repo") as session:
                file_resp = await session.call_tool("read_file", {"relpath": target_file})
                content = extract_text_content(file_resp)
                
                if content and not content.startswith("ERROR"):
                    print(f"✅ Successfully fetched {target_file} ({len(content)} characters)")
                    
                    ask_msg = f"Summarize the following Python file '{target_file}':\n\n{content[:4000]}"
                    resp2 = await agent.ainvoke({
                        "messages": [{"role": "user", "content": ask_msg}]
                    })
                    print(f"\n🤖 Agent response (summary of {target_file}):")
                    print(resp2["messages"][-1].content)
                else:
                    print(f"❌ Could not fetch file: {target_file}")
                    print(f"Response: {content}")
        else:
            print("❌ No Python files found to summarize")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🧹 Cleaning up...")


if __name__ == "__main__":
    asyncio.run(main())