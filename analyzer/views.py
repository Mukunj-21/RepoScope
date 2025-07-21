from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Repository, RepositoryFile, CodeSearch
from .services.github_service import GitHubService
from .services.llm_service import FileAnalyzer
from .services.memory_service import MemoryService
from datetime import datetime
import json

def index(request):
    """Main application page"""
    return render(request, 'analyzer/index.html')

@api_view(['POST'])
def analyze_repository(request):
    """Load and analyze a GitHub repository"""
    github_url = request.data.get('github_url')
    if not github_url:
        return Response({'error': 'GitHub URL required'}, status=400)
    
    github_service = GitHubService()
    owner, repo_name = github_service.parse_repo_url(github_url)
    
    if not owner or not repo_name:
        return Response({'error': 'Invalid GitHub URL format'}, status=400)
    
    # Get repository info
    repo_info = github_service.get_repo_info(owner, repo_name)
    
    # Create or get repository
    repository, created = Repository.objects.get_or_create(
        github_url=github_url,
        defaults={
            'owner': owner, 
            'repo_name': repo_name,
            'description': repo_info.get('description', ''),
            'language': repo_info.get('language', '')
        }
    )
    
    # Clear existing files if repository was recreated
    if not created:
        RepositoryFile.objects.filter(repository=repository).delete()
    
    # Get files from GitHub
    files = github_service.get_repo_files(owner, repo_name)
    
    if not files:
        return Response({'error': 'Unable to fetch repository files. Check if the repository exists and is public.'}, status=400)
    
    processed_files = []
    for file_data in files:
        if file_data['type'] == 'blob' and github_service.is_text_file(file_data['path']):
            file_path = file_data['path']
            content = github_service.get_file_content(owner, repo_name, file_path)
            
            if content and len(content.strip()) > 0 and "Error" not in content:
                file_ext = file_path.split('.')[-1] if '.' in file_path else ''
                
                repo_file = RepositoryFile.objects.create(
                    repository=repository,
                    file_path=file_path,
                    file_type=file_ext,
                    file_size=len(content),
                    content=content
                )
                
                processed_files.append({
                    'id': repo_file.id,
                    'file_path': file_path,
                    'file_type': file_ext,
                    'file_size': len(content),
                    'analyzed': False
                })
    
    return Response({
        'repository_id': repository.id,
        'repository_info': {
            'owner': owner,
            'name': repo_name,
            'description': repository.description,
            'language': repository.language
        },
        'files': processed_files,
        'total_files': len(processed_files)
    })

@api_view(['GET'])
def preview_file(request, file_id):
    """Get file preview with syntax highlighting info"""
    try:
        repo_file = get_object_or_404(RepositoryFile, id=file_id)
        preview = repo_file.get_preview(lines=100)
        
        return Response({
            'file_id': file_id,
            'file_path': repo_file.file_path,
            'file_type': repo_file.file_type,
            'file_size': repo_file.file_size,
            'preview': preview,
            'total_lines': len(repo_file.content.splitlines()),
            'analyzed': bool(repo_file.analysis)
        })
    except RepositoryFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=404)

@api_view(['POST'])
def analyze_file(request):
    """Analyze a specific file using local LLM"""
    file_id = request.data.get('file_id')
    
    try:
        repo_file = get_object_or_404(RepositoryFile, id=file_id)
    except RepositoryFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=404)
    
    # Initialize analyzer
    analyzer = FileAnalyzer()
    
    # Perform analysis
    analysis = analyzer.analyze_file(repo_file.content, repo_file.file_path)
    
    # Store analysis
    MemoryService.store_analysis(repo_file, analysis)
    repo_file.analyzed_at = datetime.now()
    repo_file.save()
    
    return Response({
        'file_id': file_id,
        'file_path': repo_file.file_path,
        'analysis': analysis,
        'analyzed_at': repo_file.analyzed_at.isoformat()
    })

@api_view(['POST'])
def search_code(request):
    """Search code across repository"""
    repository_id = request.data.get('repository_id')
    search_query = request.data.get('search_query')
    
    if not repository_id or not search_query:
        return Response({'error': 'Repository ID and search query required'}, status=400)
    
    try:
        repository = get_object_or_404(Repository, id=repository_id)
    except Repository.DoesNotExist:
        return Response({'error': 'Repository not found'}, status=404)
    
    # Get all files content
    files = RepositoryFile.objects.filter(repository=repository)
    files_content = {f.file_path: f.content for f in files}
    
    # Perform AI search
    analyzer = FileAnalyzer()
    search_results = analyzer.search_code(files_content, search_query)
    
    # Store search results
    CodeSearch.objects.create(
        repository=repository,
        search_query=search_query,
        results=search_results
    )
    
    return Response({
        'search_query': search_query,
        'results': search_results,
        'files_searched': len(files_content)
    })

@api_view(['GET'])
def llm_status(request):
    """Check LLM service status"""
    analyzer = FileAnalyzer()
    
    return Response({
        'ollama_available': analyzer.llm.is_available(),
        'available_models': analyzer.llm.get_available_models(),
        'recommended_models': list(analyzer.llm.models.values())
    })
