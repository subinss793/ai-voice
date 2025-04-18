from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PronunciationRecord,TestProgress,Question

# admin.site.unregister(User)  # Unregister default User if registered
admin.site.register(User, UserAdmin)
admin.site.register(PronunciationRecord)


# # Check if User is already registered
# if not admin.site.is_registered(User):
#     admin.site.register(User, UserAdmin)
@admin.register(TestProgress)
class TestProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'progress', 'level')  # Shows these fields in the list view
    search_fields = ('user__username',)  # Enables search by username
    list_filter = ('level',)  # Adds a filter for levels in the admin panel


# Register Question model with custom admin interface
@admin.register(Question)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "level", "answer_key", "hint")