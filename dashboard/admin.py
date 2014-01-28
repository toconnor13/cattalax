from dashboard.models import Customer, Day, Hour
from django.contrib import admin

class HourInline(admin.TabularInline):
	model=Hour

class DayAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['day']}),
	]
	inlines=[HourInline]
	list_display = ('day', 'month', 'year')

admin.site.register(Day, DayAdmin)
