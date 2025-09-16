حتماً 👌 اینم کل محتوای `README.md` که فقط کافی هست کپی کنی و بذاری توی پروژه‌ت:

---

# Notification SaaS 

یک پروژه‌ی تمرینی برای طراحی و توسعه سرویس **SaaS Notification** با قابلیت ارسال ایمیل و SMS.

---

## ویژگی‌ها

* **Authentication با API Key** (صدور کلید برای هر کاربر و مدیریت آن‌ها).
* **Quota & Plans**: تعریف پلن‌های رایگان و پولی با محدودیت تعداد پیام در ماه.
* **Queue Processing**: استفاده از Celery برای پردازش asynchronous پیام‌ها.
* **Batch Requests**: امکان ارسال پیام به چندین گیرنده در یک درخواست.
* **Notification Status API**: مشاهده وضعیت پیام‌ها (queued, sent, failed).

---

##  تکنولوژی‌ها

* Django / Django REST Framework
* Celery + Redis
* PostgreSQL (پیشنهادی، هر دیتابیس سازگار با Django قابل استفاده است)
* Docker (برای استقرار ساده‌تر - اختیاری)

---

##  API Endpoints

### ثبت‌نام (SignUp)

```http
POST /api/signup/
```

**Response:**

```json
{
  "id": 1,
  "phone": "09121234567",
  "api_key": "abcd-1234..."
}
```

---

### ارسال نوتیفیکیشن (تکی یا گروهی)

```http
POST /api/notifications/send/
```

**Request (تکی):**

```json
{
  "type": "email",
  "to": "ali@test.com",
  "subject": "سلام",
  "body": "این یک پیام تست است"
}
```

**Request (گروهی):**

```json
{
  "type": "sms",
  "to": ["09121234567", "09381234567", "09991234567"],
  "body": "سلام! این یک پیام گروهی است"
}
```

**Response:**

```json
{
  "count": 3,
  "notifications": [
    {"id": "uuid1", "to": "09121234567", "status": "queued"},
    {"id": "uuid2", "to": "09381234567", "status": "queued"},
    {"id": "uuid3", "to": "09991234567", "status": "queued"}
  ]
}
```

---

### مشاهده وضعیت نوتیفیکیشن

```http
GET /api/notifications/<id>/
```

**Response:**

```json
{
  "id": "uuid1",
  "type": "sms",
  "to": "09121234567",
  "status": "sent",
  "created_at": "2025-09-15T12:00:00Z",
  "processed_at": "2025-09-15T12:00:05Z"
}
```

---

## راه‌اندازی پروژه

1. کلون کردن ریپو:

```bash
git clone https://github.com/<username>/notification-saas.git
cd notification-saas
```

2. نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

3. اجرای مایگریشن‌ها:

```bash
python manage.py migrate
```

4. اجرای سرور:

```bash
python manage.py runserver
```

5. اجرای Celery Worker:

```bash
celery -A project_name worker -l info
```

---

##  نکات

* این پروژه صرفاً به عنوان **تمرین** ساخته شده است.
* قابلیت توسعه به سمت سرویس واقعی SaaS وجود دارد (پرداخت آنلاین، داشبورد مدیریت و ...).

---

##  Author

Ali Namavar
[LinkedIn](https://www.linkedin.com/in/ali-namavar-5ba701289/) | [GitHub](https://github.com/AliNamavar)

---


