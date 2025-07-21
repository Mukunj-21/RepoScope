from ..models import RepositoryFile, Repository
from typing import Dict, List

class MemoryService:
    @staticmethod
    def store_analysis(repo_file: RepositoryFile, analysis: str):
        """Store analysis result in database"""
        repo_file.analysis = analysis
        repo_file.save()

    @staticmethod
    def get_repo_context(repository: Repository) -> Dict[str, str]:
        """Get all analyzed files as context"""
        files = RepositoryFile.objects.filter(
            repository=repository, 
            analysis__isnull=False
        ).exclude(analysis='')
        
        return {f.file_path: f.analysis for f in files}

    @staticmethod
    def get_file_relationships(repository: Repository, target_file_path: str) -> List[Dict]:
        """Find files that might be related to target file"""
        target_file = RepositoryFile.objects.filter(
            repository=repository,
            file_path=target_file_path
        ).first()
        
        if not target_file:
            return []
        
        # Simple relationship detection based on imports/references
        relationships = []
        other_files = RepositoryFile.objects.filter(repository=repository).exclude(id=target_file.id)
        
        for file in other_files:
            score = 0
            
            # Check if target file is referenced in this file
            if target_file_path in file.content:
                score += 3
            
            # Check common directory
            if '/'.join(target_file_path.split('/')[:-1]) == '/'.join(file.file_path.split('/')[:-1]):
                score += 1
            
            # Check similar file types
            if target_file.file_type == file.file_type:
                score += 1
            
            if score > 0:
                relationships.append({
                    'file_path': file.file_path,
                    'relationship_score': score,
                    'file_type': file.file_type
                })
        
        return sorted(relationships, key=lambda x: x['relationship_score'], reverse=True)[:10]
