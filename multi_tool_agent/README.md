# AI Learning Companion for Children - Dragonborn

This project implements a conversational AI system designed specifically for children under 8 years old. It uses Google's ADK (Agent Development Kit) and Gemini models to create a system that can recognize images, answer questions, and provide child-friendly interactions.

## Overview

The application is built as a multi-agent system where different specialized agents handle specific tasks. A coordinator agent orchestrates these specialized agents to provide a cohesive experience. The system is particularly focused on image recognition and providing educational information about objects that children might be curious about.

## Components

### Agent Structure

- **Root Agent (Coordinator)**: Manages the overall interaction flow and delegates tasks to specialized sub-agents
- **Specialized Sub-Agents**:
  - **Greeting Agent**: Provides friendly greetings tailored for young children
  - **Farewell Agent**: Delivers polite goodbye messages appropriate for children
  - **Description Agent**: Answers questions and provides educational information
  - **Image Fetch Agent**: Retrieves images from the chat
  - **Image Recognizer Agent**: Analyzes images to identify objects
  - **Model Task Agent**: Handles base execution tasks

### Core Functionality

1. **Image Recognition**: Children can upload images, and the system will identify the main objects in them
2. **Educational Responses**: Provides simple, child-friendly explanations about recognized objects
3. **Google Search Integration**: Can search the web for additional information when needed
4. **Child-Friendly Interface**: All interactions are designed to be appealing and understandable for young children

## Technical Details

### Technologies Used

- **Google ADK (Agent Development Kit)**: Framework for building multi-agent AI systems
- **Vertex AI**: Hosts and serves the agent system
- **Gemini Models**: Powers the AI capabilities
  - Gemini 2.0 Flash for most agents
  - Gemini 2.0 Flash Lite for simpler greeting/farewell agents
- **PIL (Python Imaging Library)**: For image processing

### Key Functions

- `get_images(image_path)`: Loads and processes images for the AI to analyze
- Various agent initializations with model specifications and instructions

### Deployment

The system is deployed using Vertex AI's agent engines, making it accessible through a conversational interface. The application includes tracing capabilities for monitoring and debugging conversations.

## Usage

Children (with adult supervision) can interact with the system by:
1. Sending greetings to start a conversation
2. Uploading images of objects they're curious about
3. Asking questions about the identified objects
4. Getting simple, educational responses appropriate for their age group

## Note for Developers

This code appears to be in development, with some commented-out sections and environment variables that need to be configured (PROJECT_ID, LOCATION, STAGING_BUCKET). To deploy this system, you'll need to:

1. Set up a Google Cloud project
2. Configure Vertex AI access
3. Set appropriate environment variables
4. Ensure all required libraries are installed