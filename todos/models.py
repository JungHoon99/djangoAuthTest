from django.db import models


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    user_id = models.ForeignKey("accounts.MyUser", on_delete=models.CASCADE, null=True, related_name='todo_user_id')
    when = models.DateTimeField(null=False, blank=False)
    how_long = models.TimeField(null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'todo'
        permissions = (
            ('access_todo', 'Can access todo'),
        )
        models.constraints.pk = []

    def __str__(self):
        return self.title