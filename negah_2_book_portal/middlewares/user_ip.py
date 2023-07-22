import threading

from ip_logs.models import IPLog

EXCLUDE_FROM_MIDDLEWARE = []


class UserIpMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = '.'.join((view_func.__module__, view_func.__name__))
        if view_name in EXCLUDE_FROM_MIDDLEWARE:
            return None

    def __call__(self, request):
        UserIpLoggerThread(request).start()
        return self.get_response(request)


class UserIpLoggerThread(threading.Thread):
    def __init__(self, request):
        super().__init__()
        self.request = request

    def run(self):
        if self.request.user.is_authenticated:
            try:
                ip = get_client_ip(self.request)
                new_ip_log = IPLog(
                    user=self.request.user,
                    visited_url=self.request.get_full_path(),
                    ip=ip
                )
                new_ip_log.save()
                # ip_logs = IPLog.objects.filter(id__in=IPLog.objects.filter()[:2500])
            except:
                pass
        else:
            pass


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
