MCP Intern Project — Day 1
Objective
Connect existing MCP servers and inspect their tools using MCP Inspector.

Concepts

Host
The AI application the user interacts with. It runs the model.

Client
The component inside the host that communicates with an MCP server.

Server
The program that exposes tools, resources, and prompts to an AI application.

Day 1 Tasks
-  Check the development environment.
-  Connect the Filesystem MCP server.
-  Connect the GitHub MCP server.
-  Capture one `tools/list` exchange.
-  Capture one `tools/call` exchange.
-  Test the servers and record the results.


My First MCP Server

Overview
A Python MCP server that provides mathematical tools.

Features
- Add two numbers
- Multiply two numbers
- Project information resource
- Math helper prompt
- Basic input validation

Requirements
- Python 3.13
- MCP Python SDK 2.x

Run
Activate the virtual environment and run:

powershell
python server.py

For testing, connect the server to MCP Inspector using STDIO.

Tools
- add_numbers(a, b)
- multiply_numbers(a, b)

Resource
- info://project

Prompt
- math_helper(operation)