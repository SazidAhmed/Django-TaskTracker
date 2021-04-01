# Import Python
from datetime import datetime

# Import Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Import models
from .models import Project, Task, Entry
from apps.team.models import Team

# Project List and Create
@login_required
def projectList(request):
    # Check if active team
    if not request.user.userprofile.active_team_id:
        return redirect('team:teamList')
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.all()

    # Create Project
    if request.method == "POST":
        title = request.POST.get('title')

        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            
            messages.info(request, 'The Project was saved')
            return redirect('project:projectList')

    return render(request, 'project/projectList.html', {'team': team, 'projects': projects})

# Project Update
@login_required
def projectEdit(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == "POST":
        title = request.POST.get('title')

        if title:
            project.title = title
            project.save()
            messages.info(request, 'The changes was saved')
            return redirect('project:projectList')

    return render(request, 'project/projectEdit.html', {'team': team, 'project': project})

# Project Delete
@login_required
def projectDelete(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    project.delete()

    messages.info(request, 'Project is deleted')
    return redirect('project:projectList')

# Task List
@login_required
def taskList(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    # Create Task
    if request.method == 'POST':
        title= request.POST.get('title')

        if title:
            task = Task.objects.create(team=team, project=project, created_by=request.user, title=title)
            
            messages.info(request, 'The Task was saved')
            return redirect('project:taskList', project_id=project.id)
           
    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)

    return render(request, 'project/taskList.html', {'team': team, 'project': project, 'tasks_todo': tasks_todo, 'tasks_done': tasks_done})

# Task Update
@login_required
def taskEdit(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == "POST":
        title = request.POST.get('title')
        status = request.POST.get('status')

        if title:
            task.title = title
            task.status = status
            task.save()
            messages.info(request, 'The changes was saved')
            return redirect('project:taskList', project_id=project.id)

# Task Delete
@login_required
def taskDelete(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    task.delete()

    messages.info(request, 'Project is deleted')
    return redirect('project:taskList', project_id=project.id)

# Task Details
@login_required
def taskDetails(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    # Entry Time
    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        minutes_total = (hours * 60) + minutes

        entry = Entry.objects.create(team=team, project=project, task=task, minutes =  minutes_total, created_by=request.user, created_at=date, is_tracked=True)
        messages.info(request, 'Entry is Saved')

    return render(request, 'project/taskDetails.html', {'team': team, 'project': project, 'task': task, 'today': datetime.today()})


# Schedule Entry Update
@login_required
def entryEdit(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)

    # entry Time
    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        
        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()
        messages.info(request, 'The Changes Was Saved')
        return redirect('project:taskDetails', project_id=project.id, task_id=task.id)

    hours, minutes = divmod(entry.minutes, 60)

    context = {'team': team, 'project': project, 'task': task, 'entry':entry, 'hours':hours, 'minutes':minutes}
    return render(request, 'project/taskDetails.html', context)

# Schedule Entry Update
@login_required
def entryDelete(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, 'Entry Was deleted')
    return redirect('project:taskDetails', project_id=project.id, task_id=task.id)



@login_required
def untrackedEntryDelete(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, 'The entry was deleted!')

    return redirect('dashboard')

@login_required
def track_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    projects = team.projects.all()
    print(entry.id)
    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = request.POST.get('project')
        task = request.POST.get('task')

        if project and task:
            entry.project_id = project
            entry.task_id = task
            entry.minutes = (hours * 60) + minutes
            entry.created_at = '%s %s' % (request.POST.get('date'), entry.created_at.time())
            entry.is_tracked = True
            entry.save()

            messages.info(request, 'The time was tracked')

            return redirect('dashboard')
    
    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'hours': hours,
        'minutes': minutes,
        'team': team,
        'projects': projects,
        'entry': entry
    }

    return render(request, 'project/track_entry.html', context)