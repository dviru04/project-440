from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Home view to check if the server is running
def home(request):
    return HttpResponse("Welcome to TechConnect!")

@csrf_exempt
def upload_project(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request
            data = json.loads(request.body)
            return JsonResponse({"message": "Project uploaded successfully!", "data": data}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)  # Corrected syntax issue
