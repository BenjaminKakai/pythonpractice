from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def health_check(request):
    # Check database connection
    try:
        db_conn = connections['default']
        db_conn.cursor()
        db_status = "healthy"
    except OperationalError:
        db_status = "unhealthy"
    
    # Overall status is healthy only if all checks pass
    status_code = 200 if db_status == "healthy" else 503
    
    response_data = {
        "status": "healthy" if status_code == 200 else "unhealthy",
        "database": db_status,
    }
    
    return JsonResponse(response_data, status=status_code)