import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from huggingface_hub import InferenceClient 



class MCPClient:


    def __init__(self):

        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = InferenceClient("http://localhost:8081")  



    async def connect_to_server(self, server_script_path: str):

        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
      
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")


        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    
    
    async def process_query(self, query: str) -> str:

        messages = [
          {
              "role": "user",
              "content": query
          }
        ]

        print("The user query is : ", query)

        response = await self.session.list_tools()
        available_tools = [{
          "name": tool.name,
          "description": tool.description,
          "input_schema": tool.inputSchema
        } for tool in response.tools]


        # response = self.client.chat_completion(
        #   model="unsloth/Meta-Llama-3.1-8B",  
        #   messages=messages,
        #   tools=available_tools,
        #   max_tokens=500
        # )

        matched_codes = re.findall(r'\b(8500)\b', query)

        if matched_codes:
            print(f"\nMatched Codes: {matched_codes}")


        # print("The first response is :\n", response)

        final_text = []
        assistant_message_content = []

        for content in response.choices[0].message.content:

            print("\n\nContent : \n", content)
            print("\nResponse : ", response)
            print("\n message ", response.choices[0].message.content)

            if content["type"] == 'text':


                print("Content type is text")
                final_text.append(content["text"])
                assistant_message_content.append(content)
          


            elif content["type"] == 'tool_use':


                print("Content type is tool use")
                tool_name = content["name"]
                tool_args = content["input"]["series"]
                tool_args = {"series" : tool_args}

                print("before result")
                print(f"Details {tool_name} {tool_args}")
                result = await self.session.call_tool(tool_name, tool_args)
                print("after result")

                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)
                messages.append({
                  "role": "assistant",
                  "content": assistant_message_content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            # "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                print("Result content after mcp server ", result.content)

                response = self.client.chat_completion(
                    model="unsloth/Meta-Llama-3.1-8B",
                    messages=messages,
                    tools=available_tools,
                    tool_choice="auto",
                )

                final_text.append(response.content[0].text)

            return "\n".join(final_text)




    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")





    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

  
async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        print("try 1 started")
        await client.connect_to_server(sys.argv[1])
        print("try 1 finished")
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())