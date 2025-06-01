import time
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class RequestTimeMiddleware(MiddlewareMixin):
    """记录每个请求的耗时"""

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Request {request.method} {request.path} "
                f"took {duration:.3f} seconds "
                f"and returned {response.status_code}"
            )
            response['X-Request-Duration'] = f"{duration:.3f}"
        return response