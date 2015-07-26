from time import time

class TimerMiddleware:
    def process_request(self, request):
        request._tm_start_time = time()

    def process_response(self, request, response):
        if not hasattr(request, "_tm_start_time"):
            return response

        total = (time() - request._tm_start_time) * 1000

        if total > 200:
            print 'Long time request %10sms %s' % (total, request.path)
        response['X-Request-Time'] = '%fsms' % total
        return response

