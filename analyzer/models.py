from django.db import models
import json

class Repository(models.Model):
    github_url = models.URLField()
    owner = models.CharField(max_length=100)
    repo_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner}/{self.repo_name}"
    
    class Meta:
        unique_together = ['owner', 'repo_name']

class RepositoryFile(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='files')
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField(default=0)
    content = models.TextField()
    content_preview = models.TextField(blank=True)  # First 50 lines for preview
    analysis = models.TextField(blank=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['repository', 'file_path']
    
    def get_preview(self, lines=50):
        """Get file preview with line numbers"""
        if self.content_preview:
            return self.content_preview
        
        lines_list = self.content.splitlines()[:lines]
        preview = "\n".join([f"{i+1:4d} | {line}" for i, line in enumerate(lines_list)])
        
        if len(self.content.splitlines()) > lines:
            preview += f"\n\n... ({len(self.content.splitlines()) - lines} more lines)"
        
        self.content_preview = preview
        self.save()
        return preview

class CodeSearch(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=200)
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Search: {self.search_query} in {self.repository}"
