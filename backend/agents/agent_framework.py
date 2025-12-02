"""
Simple Agent Framework with Ollama and Direct Tool Calling

This module provides a straightforward agent implementation using ChatOllama
with tool calling capabilities, avoiding deprecated LangChain agent APIs.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from typing import List, Dict, Any, Optional
import json
import os


class BaseAgent:
    """
    Simple agent class with Ollama LLM and tool calling support.
    
    This bypasses LangChain's agent abstractions and directly uses
    tool-calling functionality for better compatibility.
    """
    
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: List,
        verbose: bool = True,
        max_iterations: int = 5
    ):
        """
        Initialize a new agent.
        
        Args:
            role: The agent's role/title
            goal: What the agent is trying to achieve
            backstory: Background context for the agent
            tools: List of @tool decorated functions
            verbose: Whether to print agent reasoning steps
            max_iterations: Maximum number of tool-calling iterations
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.verbose = verbose
        self.max_iterations = max_iterations
        
        # Initialize Ollama LLM with tools
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL_NAME", "llama3.2:1b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.7
        )
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(tools)
        
        # System message
        self.system_message = f"""You are {role}.

Your goal: {goal}

Background: {backstory}

You have access to tools to accomplish tasks. When you need to use a tool, the system will call it for you and provide the results. Think step by step and use tools when necessary."""
    
    def execute(self, task_description: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute a task using the LLM with tool calling.
        
        Args:
            task_description: The task to execute
            context: Optional additional context
            
        Returns:
            The agent's final answer as a string
        """
        # Build context if provided
        if context:
            context_str = "\n\nContext:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
            task_description = task_description + context_str
        
        # Initialize message history
        messages = [
            SystemMessage(content=self.system_message),
            HumanMessage(content=task_description)
        ]
        
        # Iterative tool calling loop
        for iteration in range(self.max_iterations):
            if self.verbose:
                print(f"\n--- Iteration {iteration + 1} ---")
            
            # Get LLM response
            try:
                response = self.llm_with_tools.invoke(messages)
            except Exception as e:
                return f"ERROR: LLM invocation failed - {str(e)}"
            
            if self.verbose:
                print(f"Response: {response.content if response.content else '[Tool calls]'}")
            
            # Append AI response to messages
            messages.append(response)
            
            # Check if there are tool calls
            if not response.tool_calls:
                # No more tool calls, return the content
                return response.content if response.content else "Task completed (no final answer provided)"
            
            # Execute tool calls
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                
                if self.verbose:
                    print(f"Tool Call: {tool_name}({tool_args})")
                
                # Find and execute the tool
                tool_result = self._execute_tool(tool_name, tool_args)
                
                if self.verbose:
                    print(f"Tool Result: {tool_result}")
                
                # Append tool result to messages
                messages.append(ToolMessage(
                    content=json.dumps(tool_result),
                    tool_call_id=tool_call["id"]
                ))
        
        # Max iterations reached
        return f"Task incomplete after {self.max_iterations} iterations. Last response: {response.content}"
    
    def _execute_tool(self, tool_name: str, tool_args: dict) -> Any:
        """Execute a tool by name with given arguments."""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    return tool.invoke(tool_args)
                except Exception as e:
                    return {"error": f"Tool execution failed: {str(e)}"}
        
        return {"error": f"Tool '{tool_name}' not found"}
