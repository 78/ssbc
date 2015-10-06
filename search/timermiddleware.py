from time import time

class TimerMiddleware:
    def process_request(self, request):
        ua_string = request.META.get('HTTP_USER_AGENT', u'')
        request.is_mobile = u'iP' in ua_string or u'Android' in ua_string
        request._tm_start_time = time()

    def process_response(self, request, response):
        if not hasattr(request, "_tm_start_time"):
            return response

        total = (time() - request._tm_start_time) * 1000

        if total > 200:
            print 'Long time request %10sms %s' % (total, request.path)
        response['X-Request-Time'] = '%fsms' % total
        return response

