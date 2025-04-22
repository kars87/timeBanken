from django import forms
from .models import TimeEntry, Material, Project, Customer

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['date', 'hours', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'quantity', 'cost', 'date_added', 'description']
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'customer', 'is_spot_service', 'hour_rate']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all().order_by('name')
        self.fields['customer'].required = False
        
        # Add a "Spot Service" option that will set is_spot_service to True
        self.fields['is_spot_service'].label = "This is a spot service"
        
        # Set default hour rate to 2000 for spot services
        if not self.instance.pk and not self.instance.hour_rate:
            self.fields['hour_rate'].initial = 2000
