import streamlit as st
import os
from datetime import datetime
import json
import re
from typing import Dict, List, Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="TalentScout - AI Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .chat-message div {
        color: #000000  
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #e8f4fd;
        color: #000000; 
    }
    .chat-message.bot {
        background-color: #f0f2f6;
        color: #000000;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .user .avatar {
        background-color: #007bff;
        color: white;
    }
    .bot .avatar {
        background-color: #28a745;
        color: white;
    }
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class HiringAssistant:
    def __init__(self):
        self.groq_api_key = self._get_groq_api_key()
        if self.groq_api_key:
            self.llm = ChatGroq(
                groq_api_key=self.groq_api_key,
                model_name="llama3-70b-8192",
                temperature=0.1
            )
        else:
            self.llm = None
        
        self.conversation_state = "greeting"
        self.candidate_info = {}
        self.tech_questions = []
        self.current_question_index = 0
        
    def _get_groq_api_key(self) -> Optional[str]:
        """Get Groq API key from environment or user input"""
        if 'GROQ_API_KEY' in os.environ:
            return os.environ['GROQ_API_KEY']
        
        if 'groq_api_key' not in st.session_state:
            return None
        
        return st.session_state.groq_api_key
    
    def extract_candidate_info(self, user_input: str, field: str) -> str:
        """Extract specific information from user input using LLM"""
        if not self.llm:
            return user_input.strip()
            
        prompt = ChatPromptTemplate.from_template(
            """Extract the {field} from the following text. Return only the extracted value, nothing else.
            If the information is not found, return 'NOT_FOUND'.
            
            Text: {text}
            
            Field to extract: {field}
            
            Examples:
            - For name: "Hi, I'm John Doe" -> "John Doe"
            - For email: "My email is john@example.com" -> "john@example.com"
            - For experience: "I have 5 years of experience" -> "5"
            - For tech stack: "I know Python, React, and MongoDB" -> "Python, React, MongoDB"
            """
        )
        
        try:
            response = self.llm.invoke(prompt.format_messages(field=field, text=user_input))
            result = response.content.strip()
            return result if result != 'NOT_FOUND' else user_input.strip()
        except Exception as e:
            st.error(f"Error extracting information: {str(e)}")
            return user_input.strip()
    
    def generate_technical_questions(self, tech_stack: str) -> List[str]:
        """Generate technical questions based on tech stack"""
        if not self.llm:
            return [
                f"Can you explain your experience with {tech_stack}?",
                f"What projects have you worked on using {tech_stack}?",
                f"What are some best practices you follow when working with {tech_stack}?"
            ]
        
        prompt = ChatPromptTemplate.from_template(
            """Generate 4 technical questions for a candidate based on their tech stack.
            The questions should be relevant, practical, and assess different aspects of their knowledge.
            
            Tech Stack: {tech_stack}
            
            Requirements:
            - Questions should be clear and specific
            - Cover different difficulty levels (basic to intermediate)
            - Focus on practical application, not just theory
            - Each question should be on a new line starting with "Q:"
            
            Example format:
            Q: Can you explain the difference between let, const, and var in JavaScript?
            Q: How would you handle state management in a large React application?
            """
        )
        
        try:
            response = self.llm.invoke(prompt.format_messages(tech_stack=tech_stack))
            questions = []
            for line in response.content.strip().split('\n'):
                if line.strip().startswith('Q:'):
                    questions.append(line.strip()[2:].strip())
            return questions[:4] if questions else [f"Tell me about your experience with {tech_stack}"]
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return [f"Tell me about your experience with {tech_stack}"]
    
    def get_bot_response(self, user_input: str) -> str:
        """Generate appropriate bot response based on conversation state"""
        user_input_lower = user_input.lower().strip()
        
        # Check for conversation ending keywords
        end_keywords = ['bye', 'goodbye', 'exit', 'quit', 'end', 'finish', 'done', 'thank you']
        if any(keyword in user_input_lower for keyword in end_keywords):
            return self._end_conversation()
        
        if self.conversation_state == "greeting":
            return self._handle_greeting()
        
        elif self.conversation_state == "collect_name":
            name = self.extract_candidate_info(user_input, "full name")
            self.candidate_info['name'] = name
            self.conversation_state = "collect_email"
            return f"Nice to meet you, {name}! 📧 Could you please provide your email address?"
        
        elif self.conversation_state == "collect_email":
            email = self.extract_candidate_info(user_input, "email address")
            # Simple email validation
            if '@' in email and '.' in email:
                self.candidate_info['email'] = email
                self.conversation_state = "collect_phone"
                return "Great! 📱 What's your phone number?"
            else:
                return "Please provide a valid email address (e.g., john@example.com)"
        
        elif self.conversation_state == "collect_phone":
            phone = self.extract_candidate_info(user_input, "phone number")
            self.candidate_info['phone'] = phone
            self.conversation_state = "collect_experience"
            return "Perfect! 💼 How many years of experience do you have in your field?"
        
        elif self.conversation_state == "collect_experience":
            experience = self.extract_candidate_info(user_input, "years of experience")
            self.candidate_info['experience'] = experience
            self.conversation_state = "collect_position"
            return "Excellent! 🎯 What position(s) are you interested in applying for?"
        
        elif self.conversation_state == "collect_position":
            position = self.extract_candidate_info(user_input, "desired position")
            self.candidate_info['position'] = position
            self.conversation_state = "collect_location"
            return "Awesome! 📍 What's your current location (city, state/country)?"
        
        elif self.conversation_state == "collect_location":
            location = self.extract_candidate_info(user_input, "location")
            self.candidate_info['location'] = location
            self.conversation_state = "collect_tech_stack"
            return "Perfect! 💻 Now, please tell me about your tech stack. What programming languages, frameworks, databases, and tools are you proficient in?"
        
        elif self.conversation_state == "collect_tech_stack":
            tech_stack = self.extract_candidate_info(user_input, "technology stack")
            self.candidate_info['tech_stack'] = tech_stack
            
            # Generate technical questions
            self.tech_questions = self.generate_technical_questions(tech_stack)
            self.current_question_index = 0
            self.conversation_state = "technical_questions"
            
            return f"Great! Based on your tech stack ({tech_stack}), I'll ask you a few technical questions to assess your skills.\n\n🔍 **Question 1:** {self.tech_questions[0]}"
        
        elif self.conversation_state == "technical_questions":
            # Store the answer
            question_key = f"answer_{self.current_question_index + 1}"
            self.candidate_info[question_key] = user_input
            
            self.current_question_index += 1
            
            if self.current_question_index < len(self.tech_questions):
                return f"Thank you for your answer! 👍\n\n🔍 **Question {self.current_question_index + 1}:** {self.tech_questions[self.current_question_index]}"
            else:
                self.conversation_state = "completed"
                return self._complete_interview()
        
        elif self.conversation_state == "completed":
            return "The interview has been completed. Thank you! 🙏 If you have any questions about the next steps, please feel free to ask, or type 'bye' to end our conversation."
        
        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase your response?"
    
    def _handle_greeting(self) -> str:
        """Handle the initial greeting"""
        self.conversation_state = "collect_name"
        return """🎯 **Welcome to TalentScout!** 

I'm your AI Hiring Assistant, here to help streamline your application process. I'll gather some basic information about you and ask a few technical questions to better understand your skills.

This should take about 5-10 minutes. Ready to get started? 

👋 **Let's begin! What's your full name?**"""
    
    def _complete_interview(self) -> str:
        """Complete the interview process"""
        summary = f"""🎉 **Interview Completed!** 

Thank you, **{self.candidate_info.get('name', 'Candidate')}**! I've successfully gathered all the information needed for your application.

📋 **Summary of your information:**
- **Email:** {self.candidate_info.get('email')}
- **Phone:** {self.candidate_info.get('phone')}
- **Experience:** {self.candidate_info.get('experience')} years
- **Position:** {self.candidate_info.get('position')}
- **Location:** {self.candidate_info.get('location')}
- **Tech Stack:** {self.candidate_info.get('tech_stack')}

✅ **Next Steps:**
1. Your responses have been recorded for review
2. Our recruitment team will evaluate your technical answers
3. You'll hear back from us within 2-3 business days
4. If selected, you'll be contacted for the next round

Thank you for your time and interest in TalentScout! 🚀

*Type 'bye' to end our conversation.*"""
        return summary
    
    def _end_conversation(self) -> str:
        """End the conversation gracefully"""
        return "🙏 Thank you for using TalentScout's Hiring Assistant! Best of luck with your application. Have a great day! 👋"

def main():
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'hiring_assistant' not in st.session_state:
        st.session_state.hiring_assistant = HiringAssistant()
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🎯 TalentScout")
        st.markdown("### AI-Powered Hiring Assistant")
        st.markdown("---")
    
    # Sidebar for API key and candidate info
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        if not st.session_state.hiring_assistant.llm:
            groq_api_key = st.text_input(
                "Groq API Key", 
                type="password", 
                help="Enter your Groq API key to enable AI features"
            )
            if groq_api_key:
                st.session_state.groq_api_key = groq_api_key
                st.session_state.hiring_assistant = HiringAssistant()
                st.rerun()
        else:
            st.success("✅ AI Assistant Ready!")
        
        st.markdown("---")
        
        # Display candidate information
        st.markdown("### 📋 Candidate Information")
        if st.session_state.hiring_assistant.candidate_info:
            info_container = st.container()
            with info_container:
                for key, value in st.session_state.hiring_assistant.candidate_info.items():
                    if not key.startswith('answer_'):
                        st.markdown(f"**{key.title()}:** {value}")
        else:
            st.markdown("*Information will appear here as you chat*")
        
        st.markdown("---")
        
        # Export functionality
        if st.session_state.hiring_assistant.candidate_info:
            st.markdown("### 💾 Export Data")
            if st.button("📊 Download Candidate Data"):
                # Create DataFrame
                data = {
                    'Field': list(st.session_state.hiring_assistant.candidate_info.keys()),
                    'Value': list(st.session_state.hiring_assistant.candidate_info.values())
                }
                df = pd.DataFrame(data)
                
                # Convert to CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"candidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    # Main chat interface
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="avatar">👤</div>
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot">
                    <div class="avatar">🤖</div>
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Start conversation button or input
    if not st.session_state.conversation_started:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Start Interview", type="primary", use_container_width=True):
                st.session_state.conversation_started = True
                bot_response = st.session_state.hiring_assistant.get_bot_response("start")
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                st.rerun()
    else:
        # Chat input
        user_input = st.chat_input("Type your response here...", key="user_input")
        
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get bot response
            bot_response = st.session_state.hiring_assistant.get_bot_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            
            # Rerun to update the display
            st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Reset Chat", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.hiring_assistant = HiringAssistant()
                st.session_state.conversation_started = False
                st.rerun()

if __name__ == "__main__":
    main()