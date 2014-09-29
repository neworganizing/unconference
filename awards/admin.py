from django.contrib import admin
from awards.models import (MostValuableOrganizer, MostValuableTechnology,
                           MostValuableCampaign)


class AwardAdmin(admin.ModelAdmin):
    list_filter = ('approved', 'contacted', 'unconference')
    list_display = (
        'name', 'approved',
        'contacted', 'unconference',
    )


admin.site.register(MostValuableOrganizer, AwardAdmin)
admin.site.register(MostValuableTechnology, AwardAdmin)
admin.site.register(MostValuableCampaign, AwardAdmin)
