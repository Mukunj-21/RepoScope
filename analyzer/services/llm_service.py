import requests
import json
from typing import Dict, Any, Optional

class OllamaLLMService:
    def __init__(self, host="http://localhost:11434"):
        self.host = host
        self.models = {
            'code': 'codellama:7b',
            'general': 'llama3:8b', 
            'fallback': 'deepseek-coder:6.7b'
        }
    
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            if response.status_code == 200:
                return [model['name'] for model in response.json().get('models', [])]
        except:
            pass
        return []
    
    def generate(self, prompt: str, model: str = None, max_tokens: int = 2000) -> str:
        """Generate response using Ollama"""
        if not model:
            model = self.models['code']
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(
                f"{self.host}/api/generate", 
                json=payload,
                timeout=120  # Increased timeout for analysis
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response generated')
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"LLM Error: {str(e)}"

class FileAnalyzer:
    def __init__(self):
        self.llm = OllamaLLMService()
    
    def create_analysis_prompt(self, file_content: str, file_path: str) -> str:
        """Create comprehensive analysis prompt"""
        file_ext = file_path.split('.')[-1].lower() if '.' in file_path else 'unknown'
        file_name = file_path.split('/')[-1]
        
        prompt = f"""As an expert code analyst, provide a comprehensive analysis of this {file_ext} file.

FILE INFORMATION:
- Path: {file_path}
- Name: {file_name}
- Type: {file_ext}
- Size: {len(file_content)} characters

FILE CONTENT:
{file_content[:4000]}

ANALYSIS REQUIREMENTS:
Provide a detailed analysis covering:

1. **PRIMARY PURPOSE & FUNCTIONALITY**
   - What is the main purpose of this file?
   - What problems does it solve?
   - How does it fit in the overall project?

2. **DETAILED CODE STRUCTURE**
   - List all classes, functions, methods with descriptions
   - Identify main entry points and execution flow
   - Explain the overall architecture pattern used

3. **DEPENDENCIES & IMPORTS**
   - List all external dependencies
   - Explain what each import is used for
   - Identify potential security or performance concerns

4. **KEY ALGORITHMS & LOGIC**
   - Explain complex algorithms or business logic
   - Identify design patterns used
   - Highlight any optimization techniques

5. **DATA STRUCTURES & MODELS**
   - Describe data structures, classes, or models defined
   - Explain relationships between different components
   - Identify data flow and transformations

6. **API & INTERFACES**
   - List public methods/functions and their parameters
   - Describe input/output formats
   - Explain error handling mechanisms

7. **CONFIGURATION & SETTINGS**
   - Identify configuration options
   - Explain environment dependencies
   - List any hardcoded values or magic numbers

8. **SECURITY & BEST PRACTICES**
   - Identify potential security vulnerabilities
   - Assess code quality and best practices
   - Suggest improvements if any

9. **TESTING & DEBUGGING**
   - Identify test coverage areas
   - Explain debugging mechanisms
   - Suggest testing strategies

10. **INTEGRATION POINTS**
    - How this file interacts with other parts
    - External services or APIs it uses
    - Database interactions if any

Be technical, detailed, and specific. Use code examples where helpful.
Format your response clearly with proper headings and sections.
"""
        return prompt
    
    def analyze_file(self, file_content: str, file_path: str) -> str:
        """Perform comprehensive file analysis"""
        if not self.llm.is_available():
            return self._fallback_analysis(file_content, file_path)
        
        prompt = self.create_analysis_prompt(file_content, file_path)
        
        # Try code-specific model first
        available_models = self.llm.get_available_models()
        
        for model_key in ['code', 'general', 'fallback']:
            model_name = self.llm.models[model_key]
            if model_name in available_models:
                analysis = self.llm.generate(prompt, model_name, max_tokens=3000)
                
                if "Error:" not in analysis and len(analysis) > 100:
                    return analysis
        
        # If no models work, use fallback
        return self._fallback_analysis(file_content, file_path)
    
    def search_code(self, files_content: Dict[str, str], search_query: str) -> str:
        """Search code with AI understanding"""
        if not self.llm.is_available():
            return self._fallback_search(files_content, search_query)
        
        # Limit content for search
        limited_content = {}
        for path, content in files_content.items():
            limited_content[path] = content[:1000]  # First 1000 chars per file
        
        content_summary = "\n\n".join([
            f"=== {path} ===\n{content}" 
            for path, content in limited_content.items()
        ])
        
        prompt = f"""Search through this codebase for: "{search_query}"

CODEBASE CONTENT:
{content_summary[:5000]}

SEARCH REQUIREMENTS:
1. **EXACT MATCHES**: Find exact occurrences of "{search_query}"
2. **CONTEXTUAL MATCHES**: Find related concepts, similar patterns, or relevant code
3. **FILE LOCATIONS**: Specify exact file paths where matches are found
4. **LINE CONTEXT**: Provide surrounding code context for each match
5. **FUNCTIONAL RELATIONSHIP**: Explain how matches relate to each other
6. **USAGE PATTERNS**: Describe how the searched term is used across files

FORMAT YOUR RESPONSE AS:
## Direct Matches
- File: [filepath]
  - Line: [line number]
  - Context: [surrounding code]
  - Purpose: [what this code does]

## Related Code
- File: [filepath]
  - Relationship: [how it relates to search term]
  - Description: [explanation]

## Summary
[Overall summary of findings and relationships]
"""
        
        available_models = self.llm.get_available_models()
        for model_key in ['general', 'code']:
            model_name = self.llm.models[model_key]
            if model_name in available_models:
                result = self.llm.generate(prompt, model_name, max_tokens=2000)
                if "Error:" not in result and len(result) > 50:
                    return result
        
        return self._fallback_search(files_content, search_query)
    
    def _fallback_analysis(self, file_content: str, file_path: str) -> str:
        """Fallback analysis when LLM is not available"""
        file_ext = file_path.split('.')[-1] if '.' in file_path else ''
        lines = file_content.splitlines()
        
        analysis = f"""# FALLBACK ANALYSIS: {file_path}
*Note: Detailed AI analysis unavailable. Using basic pattern recognition.*

## File Overview
- **Type**: {file_ext.upper()} file
- **Size**: {len(file_content)} characters, {len(lines)} lines
- **Complexity**: {'High' if len(lines) > 500 else 'Medium' if len(lines) > 100 else 'Low'}

## Basic Structure Analysis
"""
        
        if file_ext == 'py':
            analysis += self._analyze_python_structure(lines)
        elif file_ext in ['js', 'ts', 'jsx', 'tsx']:
            analysis += self._analyze_javascript_structure(lines)
        elif file_ext in ['html', 'htm']:
            analysis += self._analyze_html_structure(lines)
        else:
            analysis += self._analyze_generic_structure(lines)
        
        analysis += f"""
## Content Preview (First 20 lines)

{chr(10).join(lines[:20])}

*For detailed AI-powered analysis, please ensure Ollama is running with code models installed.*
"""
        return analysis
    
    def _analyze_python_structure(self, lines):
        imports = [line.strip() for line in lines if line.strip().startswith(('import ', 'from '))]
        classes = [line.strip() for line in lines if line.strip().startswith('class ')]
        functions = [line.strip() for line in lines if line.strip().startswith('def ')]
        
        return f"""
### Python Structure
- **Imports**: {len(imports)} dependencies
{chr(10).join([f'  - {imp}' for imp in imports[:10]])}

- **Classes**: {len(classes)} defined
{chr(10).join([f'  - {cls}' for cls in classes[:10]])}

- **Functions**: {len(functions)} defined
{chr(10).join([f'  - {func}' for func in functions[:10]])}
"""
    
    def _analyze_javascript_structure(self, lines):
        functions = []
        variables = []
        for line in lines:
            line = line.strip()
            if 'function ' in line or '=>' in line:
                functions.append(line[:100])
            if line.startswith(('const ', 'let ', 'var ')):
                variables.append(line[:100])
        
        return f"""
### JavaScript/TypeScript Structure
- **Functions**: {len(functions)} found
- **Variables**: {len(variables)} declared
- **Framework**: {"React" if any("react" in line.lower() for line in lines) else "Vanilla JS"}
"""
    
    def _analyze_html_structure(self, lines):
        content = ' '.join(lines).lower()
        return f"""
### HTML Structure
- **Forms**: {"Yes" if "<form" in content else "No"}
- **Scripts**: {"Yes" if "<script" in content else "No"}
- **Stylesheets**: {"Yes" if "stylesheet" in content else "No"}
"""
    
    def _analyze_generic_structure(self, lines):
        return f"""
### Generic File Analysis
- **Type**: {"Configuration" if any(char in ' '.join(lines[:5]) for char in ['=', ':', '{']) else "Documentation/Code"}
- **Lines**: {len(lines)}
"""
    
    def _fallback_search(self, files_content: Dict[str, str], search_query: str) -> str:
        """Basic text search fallback"""
        results = []
        
        for file_path, content in files_content.items():
            lines = content.splitlines()
            matches = []
            
            for i, line in enumerate(lines):
                if search_query.lower() in line.lower():
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    context = "\n".join([f"{j+1:4d}: {lines[j]}" for j in range(start, end)])
                    matches.append(f"**Line {i+1}**:\n``````")
            
            if matches:
                results.append(f"## {file_path}\nFound {len(matches)} matches:\n" + "\n\n".join(matches[:3]))
        
        return "\n\n".join(results) if results else f"No matches found for '{search_query}'"
