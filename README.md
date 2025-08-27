# 🎯 TalentScout - AI Hiring Assistant

An intelligent chatbot designed to streamline the initial candidate screening process for TalentScout, a fictional recruitment agency specializing in technology placements.

## 🌟 Project Overview

TalentScout's AI Hiring Assistant is a sophisticated chatbot that:
- Collects essential candidate information
- Generates tailored technical questions based on candidate's tech stack
- Maintains contextual conversation flow
- Provides a seamless user experience through an intuitive Streamlit interface

## ✨ Features

### Core Functionality
- **Smart Information Collection**: Gathers name, email, phone, experience, position, location, and tech stack
- **Dynamic Question Generation**: Creates relevant technical questions based on candidate's declared technologies
- **Context-Aware Conversations**: Maintains conversation flow and handles follow-up questions
- **Graceful Exit Handling**: Responds to conversation-ending keywords appropriately
- **Data Export**: Download candidate information as CSV

### AI-Powered Features
- **LLM Integration**: Uses Groq AI with LLaMA 3 70B model for intelligent responses
- **Smart Information Extraction**: Leverages LangChain for prompt engineering and information parsing
- **Adaptive Question Generation**: Creates questions tailored to specific tech stacks

### User Experience
- **Modern UI**: Clean, responsive Streamlit interface with custom styling
- **Real-time Chat**: Interactive chat experience with message history
- **Sidebar Information**: Live display of collected candidate information
- **Visual Feedback**: Clear indicators for conversation state and progress

## 🛠️ Technical Specifications

### Technology Stack
- **Frontend**: Streamlit
- **AI/ML**: LangChain + Groq AI (LLaMA 3 70B)
- **Data Processing**: Pandas
- **Language**: Python 3.8+

### Architecture Highlights
- **Modular Design**: Clean separation of concerns with OOP approach
- **State Management**: Efficient conversation state handling
- **Error Handling**: Robust error management for API calls and user inputs
- **Scalable Structure**: Easy to extend with additional features

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Groq API key (get it from [Groq Console](https://console.groq.com/))

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional)**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 Usage Guide

### Getting Started
1. **Launch the App**: Run the Streamlit application
2. **Enter API Key**: Input your Groq API key in the sidebar (if not set as environment variable)
3. **Start Interview**: Click "Start Interview" to begin the conversation
4. **Follow Prompts**: Answer the questions as the chatbot guides you through the process

### Conversation Flow
1. **Greeting & Overview**: Chatbot introduces itself and explains the process
2. **Personal Information**: Collects name, email, phone, experience, position, and location
3. **Tech Stack Declaration**: Candidate specifies their technical skills
4. **Technical Questions**: 4 tailored questions based on declared tech stack
5. **Completion**: Summary of information and next steps

### Ending Conversation
Use keywords like: `bye`, `goodbye`, `exit`, `quit`, `end`, `finish`, `done`, `thank you`

### Data Export
- View collected information in the sidebar
- Click "Download Candidate Data" to export as CSV

## 🎨 Prompt Engineering Strategy

### Information Extraction Prompts
```python
# Example prompt for extracting candidate information
"""Extract the {field} from the following text. Return only the extracted value, nothing else.
If the information is not found, return 'NOT_FOUND'.

Text: {text}
Field to extract: {field}"""
```

### Technical Question Generation
```python
# Prompt for generating tech-specific questions
"""Generate 4 technical questions for a candidate based on their tech stack.
The questions should be relevant, practical, and assess different aspects of their knowledge.

Tech Stack: {tech_stack}

Requirements:
- Questions should be clear and specific
- Cover different difficulty levels (basic to intermediate)
- Focus on practical application, not just theory"""
```

### Design Principles
- **Clear Instructions**: Specific, unambiguous prompts
- **Context Preservation**: Maintaining conversation context across interactions
- **Fallback Handling**: Graceful degradation when AI features are unavailable
- **Output Formatting**: Structured responses for consistent parsing

## 🔧 Technical Implementation Details

### State Management
```python
class HiringAssistant:
    def __init__(self):
        self.conversation_state = "greeting"
        self.candidate_info = {}
        self.tech_questions = []
        self.current_question_index = 0
```

### LLM Integration
- **Model**: LLaMA 3 70B via Groq API
- **Temperature**: 0.1 (for consistent, focused responses)
- **Framework**: LangChain for prompt management
- **Fallback**: Graceful degradation when API is unavailable

### Data Privacy & Security
- **No Persistent Storage**: Data exists only during session
- **Input Validation**: Basic email format validation
- **Secure API Handling**: API keys managed through environment variables

## 🚧 Challenges & Solutions

### Challenge 1: Context Management
**Problem**: Maintaining conversation context across multiple user interactions
**Solution**: Implemented state machine pattern with clear conversation states and context preservation

### Challenge 2: Dynamic Question Generation
**Problem**: Creating relevant questions for diverse tech stacks
**Solution**: Designed flexible prompts that adapt to any technology combination using LangChain

### Challenge 3: Error Handling
**Problem**: Managing API failures and unexpected user inputs
**Solution**: Implemented comprehensive error handling with graceful fallbacks

### Challenge 4: User Experience
**Problem**: Creating an engaging, professional interview experience
**Solution**: Custom CSS styling, clear conversation flow, and intuitive UI design

## 📊 Performance Considerations

- **Response Time**: Optimized prompts for quick LLM responses
- **Memory Usage**: Efficient session state management
- **API Efficiency**: Minimal API calls with smart caching
- **Scalability**: Modular architecture for easy feature additions

## 🎯 Future Enhancements

### Planned Features
- **Sentiment Analysis**: Gauge candidate emotions during conversation
- **Multilingual Support**: Support for multiple languages
- **Advanced Analytics**: Detailed candidate scoring and insights
- **Integration APIs**: Connect with ATS systems
- **Voice Interface**: Audio-based interviews

### Performance Optimizations
- **Caching**: Cache frequently generated questions
- **Async Processing**: Non-blocking API calls
- **Database Integration**: Persistent data storage
- **Load Balancing**: Support for multiple concurrent users

## 📝 Code Quality & Standards

### Structure
- **Modular Design**: Clean separation of UI, logic, and AI components
- **OOP Principles**: Well-structured classes with clear responsibilities
- **Documentation**: Comprehensive comments and docstrings
- **Error Handling**: Robust exception management

### Best Practices
- **Type Hints**: Full type annotation for better code clarity
- **Logging**: Comprehensive logging for debugging and monitoring
- **Testing**: Unit tests for critical functions
- **Security**: Secure handling of sensitive information

## 🔐 Security & Privacy

- **Data Handling**: No persistent storage of candidate information
- **API Security**: Secure API key management
- **Input Validation**: Prevention of injection attacks
- **Privacy Compliance**: GDPR-ready data handling practices

## 📄 License

This project is created for educational/assignment purposes. Please ensure compliance with relevant terms when using in production environments.

## 👨‍💻 Author

Created as part of AI/ML Intern Assignment - demonstrating expertise in:
- Large Language Models (LLMs)
- Prompt Engineering
- Full-stack Development
- AI Application Architecture
- User Experience Design

---

### 🎉 Demo

**Live Demo**: https://trestle-labs-assignments-muqwc5xdmwkad3ymi76vru.streamlit.app/

**Video Walkthrough**: https://www.loom.com/share/ff242241a2ea49b683521c5033fc57a8?sid=6385fc22-4343-46e5-9c50-cf8d7a096b65
---

*For questions or support, please contact the development team.*
