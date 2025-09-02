from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from student.models import Student
import requests

def send_telegram_message(text: str, chat_id: str):
    TOKEN = "8461684638:AAGy3Eq-EKGZnTAmMVNPtj_TQSkHrgTqJec"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Xatolik: {e}")

@csrf_exempt
def stream_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST method required"}, status=405)

    try:
        student_id = request.POST.get("id") or request.GET.get("id")
        message = request.POST.get("message") or request.GET.get("message")
        print(student_id, message)

        if not student_id or not message:
            return JsonResponse({"status": "error", "message": "id va message kerak"}, status=400)

        student = Student.objects.filter(student_id=int(student_id)).first()
        if not student:
            return JsonResponse({"status": "error", "message": "Student topilmadi"}, status=404)

        if student.sub_time and student.sub_time > timezone.now():
            if student.chat_id:
                send_telegram_message(text=message, chat_id=student.chat_id)
                return JsonResponse({"status": "ok", "message": "Xabar yuborildi"})
            else:
                return JsonResponse({"status": "error", "message": "Student chat_id mavjud emas"}, status=400)
        else:
            return JsonResponse({"status": "error", "message": "sub_time yetib bo‘lgan"}, status=400)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
