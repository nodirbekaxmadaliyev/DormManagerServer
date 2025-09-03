from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from student.models import Student
import json
import requests


def send_telegram_message(text: str, chat_id: str):
    TOKEN = "8461684638:AAFL-YIZQKYPkgzqrtBdMohdlCXfTiwd0FY"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Agar xato bo'lsa, exception ko'taradi
        return True
    except Exception as e:
        print(f"Telegram xabar yuborishda xatolik: {e}")
        return False


@csrf_exempt
def stream_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST method required"}, status=405)

    try:
        # JSON formatidagi ma'lumotlarni o'qish
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

            studentid = data.get("id")
            message = data.get("message")
        else:
            # Form-data yoki x-www-form-urlencoded uchun
            studentid = request.POST.get("id")
            message = request.POST.get("message")

        print(f"Qabul qilindi: id={studentid}, message={message}")

        if not studentid or not message:
            return JsonResponse({"status": "error", "message": "id va message kerak"}, status=400)

        # Student ni topish (studentid bo'yicha)
        try:
            student = Student.objects.get(student_id=int(studentid))
            print(f"Student topildi: {student.first_name} {student.last_name}")
        except (Student.DoesNotExist, ValueError):
            return JsonResponse({"status": "error", "message": "Student topilmadi"}, status=404)

        # Subscription vaqtini tekshirish
        if student.sub_time and student.sub_time > timezone.now():
            if student.chat_id:
                # Telegramga xabar yuborish
                print(f"Telegramga xabar yuborilmoqda: {message}")
                success = send_telegram_message(text=message, chat_id=student.chat_id)
                if success:
                    print("✅ Xabar muvaffaqiyatli yuborildi")
                    return JsonResponse({"status": "ok", "message": "Xabar yuborildi"})
                else:
                    print("❌ Telegramga xabar yuborib bo'lmadi")
                    return JsonResponse({"status": "error", "message": "Telegramga xabar yuborib bo'lmadi"}, status=500)
            else:
                print("❌ Studentda chat_id mavjud emas")
                return JsonResponse({"status": "error", "message": "Student chat_id mavjud emas"}, status=400)
        else:
            print(f"❌ Subscription vaqti tugagan: {student.sub_time}")
            return JsonResponse({"status": "error", "message": "sub_time yetib bo'lgan"}, status=400)

    except Exception as e:
        print(f"Xatolik: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)