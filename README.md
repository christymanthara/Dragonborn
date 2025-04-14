# Dragonborn

## DragonHack 2025 Hackathon Project

This repository contains the code for our DragonHack 2025 hackathon project, Dragonborn - an AI learning companion designed specifically for children under 8 years old.

## Project Overview

Dragonborn is a conversational AI system that uses Google's Agent Development Kit (ADK) and Gemini models to create an engaging, educational experience for young children. Our multi-agent architecture enables the system to recognize images, answer questions, and provide child-friendly interactions in a safe, educational environment.

## Key Features

- **[Multi-Agent AI System](multi_tool_agent/README.md)**: Utilizes a coordinator agent that orchestrates specialized sub-agents for different tasks
- **Image Recognition**: Children can upload images of objects they're curious about
- **Educational Responses**: Provides simple, age-appropriate explanations about recognized objects
- **Child-Friendly Interface**: All interactions designed specifically for children under 8
- **AR Integration**: Implements augmented reality to enhance the learning experience
- **Interactive Avatar**: "Tinty" serves as an engaging companion that guides children through their learning journey
- **Contextual Learning**: Prompts children if they want to learn more about objects they're viewing

## Technical Implementation

### [Agent Architecture](multi_tool_agent/README.md)

- **Root Coordinator Agent**: Manages conversation flow and delegates to specialized agents
- **Specialized Sub-Agents**:
  - **Greeting Agent**: Provides friendly greetings tailored for young children
  - **Farewell Agent**: Delivers polite goodbye messages
  - **Description Agent**: Answers questions and provides educational information
  - **Image Fetch Agent**: Retrieves images from the chat
  - **Image Recognizer Agent**: Analyzes images to identify objects
  - **Model Task Agent**: Handles base execution tasks

### Technologies Used

- **[Google ADK (Agent Development Kit)](multi_tool_agent/README.md)**: Framework for building our multi-agent system
- **Vertex AI**: Hosts and serves the agent system
- **Gemini Models**: Powers the AI capabilities, using different models based on task complexity
- **Google Search Integration**: Enables the system to find additional information when needed
- **FastAPI**: Backend framework for handling API requests
- **Computer Vision Models**: Utilizes local vision models including ResNet50 and YOLOv8 for image recognition
- **Unity Integration**: Receives camera input directly from Unity for seamless AR experience
- **Cloud Hosting**: Deployed on cloud infrastructure for scalability and accessibility

### User Experience

- **AR Interface**: Children interact with the real world through an augmented reality interface
- **Avatar Companion**: Tinty, our friendly avatar, guides children through their learning experience
- **Contextual Prompting**: System intelligently asks if children want to learn more about what they're seeing
- **Focused Information**: Provides concise, relevant information tailored to young attention spans
- **Interactive Learning**: Combines entertainment with education to keep children engaged

## Team

Created with ❤️ for DragonHack 2025
