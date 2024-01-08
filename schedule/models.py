from django.db import models
from django.contrib.auth.models import User

class FileModel(models.Model):
    file = models.FileField(upload_to='event_files/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    memo = models.TextField(blank=True, null=True)
    meeting = models.BooleanField(default=False)
    files = models.ManyToManyField(FileModel)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    meeting_text = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    def delete(self, using=None, keep_parents=False):
        # 일정 삭제 시 연결된 파일도 함께 삭제
        for file in self.files.all():
            file.file.delete()
            file.delete()

        super().delete(using=using, keep_parents=keep_parents)