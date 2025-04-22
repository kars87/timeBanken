from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, TimeEntry, Material, Customer
from .forms import TimeEntryForm, MaterialForm, ProjectForm
from datetime import date
from django.utils import timezone
import zoneinfo
from datetime import datetime, timedelta

def home(request):
    if request.user.is_authenticated:
        return redirect('project_list')
    return redirect('login')

@login_required
def project_list(request):
    # Show active projects (those not marked as finished)
    projects = Project.objects.filter(is_finished=False).order_by('start_date')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    entries = project.timeentry_set.filter(user=request.user).order_by('-date')
    materials = project.material_set.all().order_by('-date_added')
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'entries': entries,
        'materials': materials
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            
            # If it's a spot service, ensure customer is None
            if project.is_spot_service:
                project.customer = None
            # If customer is selected, use their default hour rate if not specified
            elif project.customer and not form.cleaned_data.get('hour_rate'):
                project.hour_rate = project.customer.default_hour_rate
            
            # Set the user to the current user
            project.user = request.user
            
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    customers = Customer.objects.all()
    return render(request, 'projects/create_project.html', {
        'form': form,
        'customers': customers,
    })

@login_required
def add_time_entry(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.project = project
            entry.user = request.user
            entry.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TimeEntryForm()
    
    return render(request, 'projects/add_time_entry.html', {
        'form': form,
        'project': project
    })

@login_required
def add_material(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.project = project
            material.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = MaterialForm()
    
    return render(request, 'projects/add_material.html', {
        'form': form,
        'project': project
    })

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            if project.is_spot_service:
                project.customer = None
            # Don't change the user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required
def edit_time_entry(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk)
    project = entry.project
    
    # Ensure users can only edit their own entries
    if entry.user != request.user:
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TimeEntryForm(instance=entry)
    
    return render(request, 'projects/edit_time_entry.html', {
        'form': form,
        'entry': entry,
        'project': project
    })

@login_required
def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    project = material.project
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'projects/edit_material.html', {
        'form': form,
        'material': material,
        'project': project
    })

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    
    return render(request, 'projects/delete_project.html', {'project': project})

@login_required
def delete_time_entry(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk)
    project = entry.project
    
    # Ensure users can only delete their own entries
    if entry.user != request.user:
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        entry.delete()
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'projects/delete_time_entry.html', {'entry': entry, 'project': project})

@login_required
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    project = material.project
    
    if request.method == 'POST':
        material.delete()
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'projects/delete_material.html', {'material': material, 'project': project})

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('name')
    return render(request, 'projects/customer_list.html', {'customers': customers})

@login_required
def mark_project_finished(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        # Set the end date to today if not already set
        if not project.end_date:
            project.end_date = date.today()
        
        # Mark the project as finished
        project.is_finished = True
        project.save()
        return redirect('project_detail', pk=project.pk)
    
    return redirect('project_detail', pk=project.pk)

@login_required
def mark_project_active(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        # Mark the project as active (not finished)
        project.is_finished = False
        project.save()
        return redirect('project_detail', pk=project.pk)
    
    return redirect('project_detail', pk=project.pk)

@login_required
def project_archive(request):
    # Show only finished projects
    projects = Project.objects.filter(is_finished=True).order_by('-end_date')
    return render(request, 'projects/project_archive.html', {'projects': projects})

@login_required
def user_hours_overview(request):
    # Default to current date
    today = timezone.now().date()
    
    # Get filter parameters
    filter_type = request.GET.get('filter', 'week')
    
    # Calculate date range based on filter
    if filter_type == 'day':
        start_date = today
        end_date = today
        title = f"Hours for {today}"
    elif filter_type == 'week':
        # Start from Monday of current week
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        title = f"Hours for week {start_date} to {end_date}"
    elif filter_type == 'month':
        start_date = today.replace(day=1)
        # Get last day of month
        if today.month == 12:
            end_date = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month+1, day=1) - timedelta(days=1)
        title = f"Hours for {start_date.strftime('%B %Y')}"
    elif filter_type == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
        title = f"Hours for {today.year}"
    else:
        # Custom date range
        try:
            start_date = datetime.strptime(request.GET.get('start_date', today.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.GET.get('end_date', today.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
            title = f"Hours from {start_date} to {end_date}"
        except ValueError:
            start_date = today
            end_date = today
            title = "Hours overview"
    
    # Get time entries for the user within the date range
    entries = TimeEntry.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Calculate total hours
    total_hours = sum(entry.hours for entry in entries)
    
    # Group entries by project
    projects_data = {}
    for entry in entries:
        if entry.project.id not in projects_data:
            projects_data[entry.project.id] = {
                'name': entry.project.name,
                'hours': 0,
                'entries': []
            }
        projects_data[entry.project.id]['hours'] += entry.hours
        projects_data[entry.project.id]['entries'].append(entry)
    
    return render(request, 'projects/user_hours_overview.html', {
        'title': title,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
        'entries': entries,
        'total_hours': total_hours,
        'projects_data': projects_data.values(),
    })
