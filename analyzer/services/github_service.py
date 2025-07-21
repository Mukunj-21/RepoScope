import requests
import base64
import re
from django.conf import settings
from typing import Tuple, Optional, List, Dict

class GitHubService:
    def __init__(self):
        self.token = getattr(settings, 'GITHUB_TOKEN', None)
        self.headers = {'Authorization': f'token {self.token}'} if self.token else {}
        self.base_url = 'https://api.github.com'
    
    def parse_repo_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract owner and repo name from GitHub URL"""
        patterns = [
            r'github\.com/([^/]+)/([^/]+)/?$',
            r'github\.com/([^/]+)/([^/]+)\.git',
            r'github\.com/([^/]+)/([^/]+)/tree/',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                if repo.endswith('.git'):
                    repo = repo[:-4]
                return owner, repo
        return None, None
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get repository information"""
        url = f'{self.base_url}/repos/{owner}/{repo}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'description': data.get('description', ''),
                'language': data.get('language', ''),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
            }
        return {}
    
    def get_repo_files(self, owner: str, repo: str, branch: str = 'main') -> List[Dict]:
        """Get all files in repository"""
        url = f'{self.base_url}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get('tree', [])
        
        # Try 'master' if 'main' fails
        if branch == 'main':
            return self.get_repo_files(owner, repo, 'master')
        
        return []
    
    def is_text_file(self, file_path: str) -> bool:
        """Enhanced text file detection"""
        text_extensions = {
            # Programming languages
            'py', 'js', 'ts', 'jsx', 'tsx', 'java', 'cpp', 'c', 'h', 'hpp',
            'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt', 'scala', 'clj',
            'hs', 'elm', 'dart', 'lua', 'perl', 'r', 'matlab', 'm',
            'cpp', 'cc', 'cxx', 'c++', 'cp', 'hpp', 'h++', 'hxx',
            
            # Web technologies
            'html', 'htm', 'css', 'scss', 'sass', 'less', 'vue', 'svelte',
            
            # Data formats
            'json', 'xml', 'yaml', 'yml', 'toml', 'ini', 'cfg', 'conf',
            'csv', 'tsv', 'sql',
            
            # Documentation
            'md', 'txt', 'rst', 'asciidoc', 'org',
            
            # Shell and scripts
            'sh', 'bash', 'zsh', 'fish', 'bat', 'cmd', 'ps1',
            
            # Build and config
            'dockerfile', 'makefile', 'cmake', 'gradle', 'maven',
            'package', 'lock', 'gitignore', 'gitattributes',
            
            # Other
            'log', 'env', 'example', 'template', 'spec'
        }
        
        # Get file extension
        if '.' in file_path:
            ext = file_path.split('.')[-1].lower()
            if ext in text_extensions:
                return True
        
        # Check special filenames
        filename = file_path.split('/')[-1].lower()
        special_files = {
            'readme', 'license', 'changelog', 'contributing', 'authors',
            'dockerfile', 'makefile', 'rakefile', 'gemfile', 'requirements'
        }
        
        return filename in special_files
    
    def get_file_content(self, owner: str, repo: str, file_path: str) -> Optional[str]:
        """Get file content with encoding handling"""
        if not self.is_text_file(file_path):
            return None
        
        url = f'{self.base_url}/repos/{owner}/{repo}/contents/{file_path}'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if file is too large
            if data.get('size', 0) > 1_000_000:  # 1MB limit
                return "File too large for analysis"
            
            content = data.get('content', '')
            if not content:
                return None
            
            try:
                # Decode base64 content
                decoded_bytes = base64.b64decode(content)
                
                # Try different encodings
                encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        return decoded_bytes.decode(encoding)
                    except UnicodeDecodeError:
                        continue
                
                # If all fail, return error message
                return "Unable to decode file content"
                
            except Exception as e:
                return f"Error reading file: {str(e)}"
        
        return None
