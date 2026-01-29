"""
Remove all emojis from Python files for professional presentation
"""

import re
import os

def remove_emojis_from_file(filepath):
    """Remove all emojis from a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove common emojis used in the files
        emoji_replacements = {
            '🔽': '',
            '🔼': '',
            '📊': '',
            '💾': '',
            '🎯': '',
            '❌': '',
            '✅': '',
            '✏️': '',
            '⏰': '',
            '🟢': '',
            '🔴': '',
            '🟡': '',
            '🚫': '',
            '📥': '',
            '⚖️': '',
            '🤖': '',
            '⚡': '',
            '🏆': '',
            '🎬': '',
            '🛡️': '',
            '📹': '',
            '🔒': '',
            '💯': '',
            '🎭': '',
            '📄': '',
            '🔧': '',
            '🧪': '',
            '👥': '',
            '📋': '',
            '🎨': '',
            '🔤': '',
            '📱': '',
            '🎯': '',
            '🛡️': '',
            '⚡': '',
            '💾': '',
            '📊': '',
            '🔗': '',
            '🏆': '',
        }
        
        # Apply replacements
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        # Remove any remaining emojis using regex
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        
        content = emoji_pattern.sub('', content)
        
        # Clean up extra spaces
        content = re.sub(r'  +', ' ', content)
        content = re.sub(r' \n', '\n', content)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Cleaned emojis from: {filepath}")
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Remove emojis from all Python files"""
    files_to_clean = [
        "mediation_system.py",
        "enforcement_execution_system.py", 
        "live_safety_demo.py",
        "unified_validator.py",
        "integration_test_suite.py"
    ]
    
    cleaned_count = 0
    for filename in files_to_clean:
        if os.path.exists(filename):
            if remove_emojis_from_file(filename):
                cleaned_count += 1
        else:
            print(f"File not found: {filename}")
    
    print(f"\nCleaned {cleaned_count} files successfully")
    print("All emojis removed for professional presentation")

if __name__ == "__main__":
    main()