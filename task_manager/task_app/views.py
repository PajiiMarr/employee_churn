from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from .models import Task
import joblib
import pickle
import os

# Path to the model
# MODEL_PATH = '/Users/mar/.cache/kagglehub/models/qadeer884/emplyee-chrun-prediction/scikitLearn/default/1/Hiring_classifier/Rf_classifier.pkl'
# Load the classifier (real model)

CLASSIFIER_PATH = '/Users/mar/.cache/kagglehub/models/qadeer884/emplyee-chrun-prediction/scikitLearn/default/1/Hiring_classifier/Rf_classifier.pkl'

try:
    classifier = joblib.load(CLASSIFIER_PATH)

    feature_names = ['satisfaction_level', 'last_performance_rating', 'number_of_projects',
                     'avg_monthly_hours', 'years_at_company', 'had_work_accident',
                     'promoted_in_last_5_years', 'salary_level']
except Exception as e:
    print(f"Error loading classifier: {e}")
    classifier = None
    feature_names = []



def predict_view(request):
    if request.method == 'POST':
        try:
            # Extract all needed features from the form
            features = []
            for feature in feature_names:
                # Convert form inputs to appropriate types
                value = request.POST.get(feature, 0)
                
                # Handle different data types
                if feature in ['had_work_accident', 'promoted_in_last_5_years']:
                    # Boolean fatures
                    features.append(int(value == 'True' or value == '1'))
                elif feature in ['satisfaction_level']:
                    features.append(float(value))
                else:
                    features.append(int(value))

            if classifier.predict([features])[0] == 1:
                prediction = 'Employee will leave'
            else:
                prediction = 'Employee will stay'
            
            # prediction = classifier.predict([features])[0]
            
            return render(request, 'tasks/prediction_result.html', {
                'prediction': prediction,
                'features': dict(zip(feature_names, features))
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'tasks/prediction_form.html', {'features': feature_names})

def task_list(request):
    tasks = Task.objects.all()

    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        assigned_personnel = request.POST.get('assigned_personnel', '')
        due_date = request.POST.get('due_date')

        if title and due_date:
            try:
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                return HttpResponse("Invalid date format", status=400)

            Task.objects.create(title=title, description=description, assigned_personnel=assigned_personnel , due_date=due_date)
            return redirect('task_list')

    return render(request, 'tasks/task_form.html')


# def task_update(request, task_id):;
#     task = get_object_or_404(Task, id=task_id)

#     if request.method == "POST":
#         task.title = request.POST.get('title')
#         task.description = request.POST.get('description', '')
#         # task.status = request.POST.get('status')
#         task.assigned_personnel = request.POST.get('assigned_personnel', '')
#         due_date = request.POST.get('due_date')

#         if task.title and due_date:
#             try:
#                 task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
#             except ValueError:
#                 return HttpResponse("Invalid date format", status=400)

#             task.save()
#             return redirect('task_list')

#     return render(request, 'tasks/task_form.html', {'task': task})

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.status = request.POST.get('status', 'Complete')

    task.save()
    return redirect('task_list')

