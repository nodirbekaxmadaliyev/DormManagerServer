from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StudentSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
import json

# === CREATE ===
@api_view(["POST"])
def add_student(request):
    data = request.data.copy()

    # id -> student_id mapping
    if "id" in data:
        val = data.pop("id")
        if isinstance(val, list):
            val = val[0]  # list bo‘lsa faqat 1-elementini olamiz
        data["student_id"] = int(val)

    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("❌ Xatolik:", serializer.errors)  # DEBUG uchun
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["PUT"])
def update_student(request, student_id):
    try:
        data = json.loads(request.body)
        student = Student.objects.get(student_id=student_id)

        student.first_name = data.get("first_name", student.first_name)
        student.last_name = data.get("last_name", student.last_name)
        student.phone_number = data.get("phone_number", student.phone_number)
        student.is_in_dormitory = data.get("is_in_dormitory") in ["true", "1", True]
        student.parent_full_name = data.get("parent_full_name", student.parent_full_name)
        student.arrival_time = data.get("arrival_time") or student.arrival_time
        student.checkout_time = data.get("checkout_time") or student.checkout_time
        student.save()

        return JsonResponse({"message": "Student updated"}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])  # client POST yuboryapti
def delete_student(request):
    try:
        data = json.loads(request.body)
        student_id = data.get("id")  # ✅ id emas, student_id
        student = Student.objects.get(student_id=student_id)
        student.delete()
        return JsonResponse({"message": "Student deleted"}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)