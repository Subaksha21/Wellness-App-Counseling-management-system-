from django.contrib import admin

# Register your models here.
from .models import CounselingMaterial, Counselor

class CounselingMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'upload_date')
    search_fields = ('title',)

admin.site.register(CounselingMaterial, CounselingMaterialAdmin)



@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    


#class Appointment(models.Model):
#    list_display = ['user', 'bio']