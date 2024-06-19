from django.core.cache import cache

from .models import VisitLog


def log_to_cache(data):
    log_id = f"log_{data['date'].timestamp()}"
    cache.set(log_id, data, timeout=60 * 60)  # Хранение в кэше 1 час


def save_log():
    logs = VisitLog.objects.all()
    print(logs)
    keys = cache.keys("log_*")
    for key in keys:
        try:
            data = cache.get(key)
            if data:
                user_log = VisitLog.objects.create(**data)
                print(user_log)

                cache.delete(key)
        except Exception as e:
            print(e)



