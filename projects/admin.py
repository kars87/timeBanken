from django.contrib import admin
from .models import Project, TimeEntry, Material, Customer
from datetime import date, timedelta
from django.utils import timezone

admin.site.site_header = "TimePortal Administration"
admin.site.site_title = "TP Admin"

@admin.action(description="Mark selected projects as finished")
def mark_projects_finished(modeladmin, request, queryset):
    queryset.update(end_date=date.today())

@admin.action(description="Mark selected projects as active")
def mark_projects_active(modeladmin, request, queryset):
    queryset.update(end_date=None)

class TimeEntryInline(admin.TabularInline):
    model = TimeEntry
    extra = 1

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

class ProjectFinishedListFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('finished', 'Finished'),
            ('active', 'Active'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'finished':
            return queryset.filter(end_date__isnull=False)
        if self.value() == 'active':
            return queryset.filter(end_date__isnull=True)
        return queryset

class TimeEntryDateListFilter(admin.SimpleListFilter):
    title = 'time period'
    parameter_name = 'date_period'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This week'),
            ('this_month', 'This month'),
            ('this_year', 'This year'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        
        if self.value() == 'today':
            return queryset.filter(date=today)
        
        if self.value() == 'this_week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(date__gte=start_of_week, date__lte=end_of_week)
            
        if self.value() == 'this_month':
            return queryset.filter(date__year=today.year, date__month=today.month)
            
        if self.value() == 'this_year':
            return queryset.filter(date__year=today.year)
            
        return queryset

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'default_hour_rate')
    search_fields = ('name', 'contact_person', 'email')
    fieldsets = (
        (None, {
            'fields': ('name', 'contact_person', 'email', 'phone', 'address')
        }),
        ('Invoice Information', {
            'fields': ('invoice_email', 'invoice_address', 'org_number', 'default_hour_rate')
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'user', 'is_spot_service', 'start_date', 'end_date', 'hour_rate', 'total_hours', 'total_material_cost')
    search_fields = ('name', 'customer__name', 'user__username')
    list_filter = ('customer', 'user', 'is_spot_service', 'start_date', ProjectFinishedListFilter)
    inlines = [TimeEntryInline, MaterialInline]
    actions = [mark_projects_finished, mark_projects_active]

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'date', 'hours', 'description')
    list_filter = ('project', 'user', TimeEntryDateListFilter, 'date')
    search_fields = ('project__name', 'user__username', 'description')
    date_hierarchy = 'date'

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'quantity', 'cost', 'date_added')
    list_filter = ('project', 'date_added')
