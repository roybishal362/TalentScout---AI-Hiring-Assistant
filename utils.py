"""
Utility functions for TalentScout Hiring Assistant
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime

def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if phone is valid, False otherwise
    """
    # Remove all non-digit characters
    cleaned_phone = re.sub(r'\D', '', phone)
    # Check if it's between 10-15 digits (international format)
    return 10 <= len(cleaned_phone) <= 15

def extract_years_experience(text: str) -> Optional[str]:
    """
    Extract years of experience from text
    
    Args:
        text (str): Text containing experience information
        
    Returns:
        Optional[str]: Extracted years or None
    """
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
        r'(\d+(?:\.\d+)?)\s*(?:year|yr)',
        r'(\d+)\+?\s*(?:years?|yrs?)',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1)
    
    # Look for standalone numbers that might represent years
    numbers = re.findall(r'\b(\d+)\b', text)
    if numbers:
        # Return the first reasonable number (between 0 and 50)
        for num in numbers:
            if 0 <= int(num) <= 50:
                return num
    
    return None

def parse_tech_stack(tech_stack: str) -> Dict[str, List[str]]:
    """
    Parse tech stack into categories
    
    Args:
        tech_stack (str): Raw tech stack string
        
    Returns:
        Dict[str, List[str]]: Categorized technologies
    """
    # Common technology categories and their keywords
    categories = {
        'languages': [
            'python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 
            'ruby', 'swift', 'kotlin', 'typescript', 'scala', 'r', 'matlab'
        ],
        'frameworks': [
            'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'express',
            'spring', 'laravel', 'rails', 'nextjs', 'nuxt', 'svelte', 'ember'
        ],
        'databases': [
            'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
            'cassandra', 'elasticsearch', 'dynamodb', 'firestore'
        ],
        'cloud': [
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'jenkins', 'gitlab', 'github actions', 'heroku', 'vercel'
        ],
        'tools': [
            'git', 'jira', 'figma', 'photoshop', 'vscode', 'intellij',
            'postman', 'slack', 'trello', 'notion', 'confluence'
        ]
    }
    
    tech_stack_lower = tech_stack.lower()
    parsed = {category: [] for category in categories}
    
    for category, techs in categories.items():
        for tech in techs:
            if tech in tech_stack_lower:
                parsed[category].append(tech.title())
    
    # Add uncategorized items
    parsed['other'] = []
    words = re.findall(r'\b\w+\b', tech_stack)
    for word in words:
        word_lower = word.lower()
        found = False
        for category_techs in categories.values():
            if word_lower in category_techs:
                found = True
                break
        if not found and len(word) > 2:
            parsed['other'].append(word.title())
    
    return {k: v for k, v in parsed.items() if v}  # Remove empty categories

def generate_candidate_summary(candidate_info: Dict) -> str:
    """
    Generate a formatted summary of candidate information
    
    Args:
        candidate_info (Dict): Dictionary containing candidate information
        
    Returns:
        str: Formatted candidate summary
    """
    summary = []
    summary.append(f"📋 **CANDIDATE SUMMARY**")
    summary.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("")
    
    # Basic Information
    summary.append("**📝 Personal Information:**")
    summary.append(f"• Name: {candidate_info.get('name', 'N/A')}")
    summary.append(f"• Email: {candidate_info.get('email', 'N/A')}")
    summary.append(f"• Phone: {candidate_info.get('phone', 'N/A')}")
    summary.append(f"• Location: {candidate_info.get('location', 'N/A')}")
    summary.append("")
    
    # Professional Information
    summary.append("**💼 Professional Information:**")
    summary.append(f"• Experience: {candidate_info.get('experience', 'N/A')} years")
    summary.append(f"• Position Interest: {candidate_info.get('position', 'N/A')}")
    summary.append(f"• Tech Stack: {candidate_info.get('tech_stack', 'N/A')}")
    summary.append("")
    
    # Technical Answers
    summary.append("**🔍 Technical Assessment:**")
    answer_count = 0
    for key, value in candidate_info.items():
        if key.startswith('answer_'):
            answer_count += 1
            summary.append(f"• Answer {answer_count}: {value[:100]}{'...' if len(value) > 100 else ''}")
    
    if answer_count == 0:
        summary.append("• No technical answers recorded")
    
    return "\n".join(summary)

def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent potential issues
    
    Args:
        user_input (str): Raw user input
        
    Returns:
        str: Sanitized input
    """
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>\"\'%;()&+]', '', user_input)
    # Limit length
    sanitized = sanitized[:500]
    # Strip whitespace
    sanitized = sanitized.strip()
    return sanitized

def format_tech_stack_display(tech_stack: str) -> str:
    """
    Format tech stack for better display
    
    Args:
        tech_stack (str): Raw tech stack string
        
    Returns:
        str: Formatted tech stack
    """
    parsed = parse_tech_stack(tech_stack)
    
    if not parsed:
        return tech_stack
    
    formatted_parts = []
    for category, technologies in parsed.items():
        if technologies:
            category_display = category.replace('_', ' ').title()
            tech_list = ', '.join(technologies)
            formatted_parts.append(f"**{category_display}:** {tech_list}")
    
    return '\n'.join(formatted_parts)

def get_question_difficulty_level(question: str, tech_stack: str) -> str:
    """
    Determine the difficulty level of a technical question
    
    Args:
        question (str): Technical question
        tech_stack (str): Candidate's tech stack
        
    Returns:
        str: Difficulty level (Beginner, Intermediate, Advanced)
    """
    question_lower = question.lower()
    
    # Keywords that suggest different difficulty levels
    beginner_keywords = [
        'what is', 'define', 'explain', 'basic', 'introduction', 'simple'
    ]
    
    intermediate_keywords = [
        'how would you', 'implement', 'design', 'optimize', 'compare',
        'difference between', 'best practices'
    ]
    
    advanced_keywords = [
        'architecture', 'scalability', 'performance', 'security', 'complex',
        'enterprise', 'microservices', 'system design'
    ]
    
    # Count keyword matches
    beginner_score = sum(1 for keyword in beginner_keywords if keyword in question_lower)
    intermediate_score = sum(1 for keyword in intermediate_keywords if keyword in question_lower)
    advanced_score = sum(1 for keyword in advanced_keywords if keyword in question_lower)
    
    # Determine level based on scores
    if advanced_score > 0 or 'senior' in tech_stack.lower():
        return 'Advanced'
    elif intermediate_score > beginner_score:
        return 'Intermediate'
    else:
        return 'Beginner'

def export_candidate_data(candidate_info: Dict, format_type: str = 'json') -> str:
    """
    Export candidate data in specified format
    
    Args:
        candidate_info (Dict): Candidate information
        format_type (str): Export format ('json' or 'csv')
        
    Returns:
        str: Formatted data string
    """
    if format_type.lower() == 'json':
        # Add metadata
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'candidate_data': candidate_info,
            'summary': generate_candidate_summary(candidate_info)
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    elif format_type.lower() == 'csv':
        # Convert to CSV format
        import io
        output = io.StringIO()
        
        # Write headers and data
        output.write("Field,Value\n")
        for key, value in candidate_info.items():
            # Escape commas and quotes in values
            escaped_value = str(value).replace('"', '""')
            if ',' in escaped_value:
                escaped_value = f'"{escaped_value}"'
            output.write(f"{key},{escaped_value}\n")
        
        return output.getvalue()
    
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

def calculate_interview_score(candidate_info: Dict) -> Dict[str, any]:
    """
    Calculate a basic interview score based on responses
    
    Args:
        candidate_info (Dict): Candidate information
        
    Returns:
        Dict[str, any]: Score breakdown
    """
    score_breakdown = {
        'completion_score': 0,
        'response_quality_score': 0,
        'total_score': 0,
        'recommendations': []
    }
    
    # Calculate completion score (40% of total)
    required_fields = ['name', 'email', 'phone', 'experience', 'position', 'location', 'tech_stack']
    completed_fields = sum(1 for field in required_fields if candidate_info.get(field))
    completion_percentage = (completed_fields / len(required_fields)) * 100
    score_breakdown['completion_score'] = completion_percentage * 0.4
    
    # Calculate response quality score (60% of total)
    answer_keys = [key for key in candidate_info.keys() if key.startswith('answer_')]
    if answer_keys:
        total_answer_length = sum(len(str(candidate_info[key])) for key in answer_keys)
        avg_answer_length = total_answer_length / len(answer_keys)
        
        # Score based on average answer length (more detailed = better)
        if avg_answer_length > 100:
            quality_score = 90
        elif avg_answer_length > 50:
            quality_score = 75
        elif avg_answer_length > 20:
            quality_score = 60
        else:
            quality_score = 40
            
        score_breakdown['response_quality_score'] = quality_score * 0.6
    
    # Calculate total score
    score_breakdown['total_score'] = score_breakdown['completion_score'] + score_breakdown['response_quality_score']
    
    # Generate recommendations
    if completion_percentage < 100:
        score_breakdown['recommendations'].append("Complete all required information fields")
    
    if score_breakdown['response_quality_score'] < 50:
        score_breakdown['recommendations'].append("Provide more detailed technical answers")
    
    if score_breakdown['total_score'] >= 80:
        score_breakdown['recommendations'].append("Excellent candidate - recommend for next round")
    elif score_breakdown['total_score'] >= 60:
        score_breakdown['recommendations'].append("Good candidate - consider for interview")
    else:
        score_breakdown['recommendations'].append("May need additional screening")
    
    return score_breakdown

# Constants for the application
CONVERSATION_STATES = [
    "greeting",
    "collect_name",
    "collect_email", 
    "collect_phone",
    "collect_experience",
    "collect_position",
    "collect_location",
    "collect_tech_stack",
    "technical_questions",
    "completed"
]

END_KEYWORDS = [
    'bye', 'goodbye', 'exit', 'quit', 'end', 'finish', 'done', 'thank you',
    'thanks', 'stop', 'close', 'terminate'
]

TECH_STACK_EXAMPLES = [
    "Python, Django, PostgreSQL, AWS",
    "JavaScript, React, Node.js, MongoDB",
    "Java, Spring Boot, MySQL, Docker",
    "C#, .NET Core, SQL Server, Azure",
    "Go, Gin, Redis, Kubernetes"
]