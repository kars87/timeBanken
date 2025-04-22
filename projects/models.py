from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Invoice information
    invoice_email = models.EmailField(blank=True)
    invoice_address = models.TextField(blank=True)
    org_number = models.CharField(max_length=20, blank=True)
    default_hour_rate = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    is_spot_service = models.BooleanField(default=False)
    hour_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
        
    def total_hours(self):
        return sum(entry.hours for entry in self.timeentry_set.all())
        
    def total_material_cost(self):
        return sum(material.cost for material in self.material_set.all())
        
    def total_labor_cost(self):
        return self.total_hours() * self.hour_rate
        
    def total_cost(self):
        return self.total_labor_cost() + self.total_material_cost()
        
class TimeEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.hours}h on {self.date}"
        
class Material(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.quantity} units at ${self.cost}"
