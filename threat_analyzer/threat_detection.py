from django.utils import timezone
from .models import Threat
from log_ingestor.models import Log

def detect_threats():
    now = timezone.now()
    # Example logic for detecting threats
    # Brute Force Login + File Access (Credential Stuffing)
    failed_logins = Log.objects.filter(action='login_failed')
    for login in failed_logins:
        success_login = Log.objects.filter(user_id=login.user_id, action='login_success', timestamp__gt=login.timestamp)
        if success_login.exists():
            file_access = Log.objects.filter(user_id=login.user_id, action='file_access', timestamp__gt=success_login.first().timestamp)
            if file_access.exists():
                Threat.objects.create(
                    timestamp=file_access.first().timestamp,
                    user_id=file_access.first().user_id,
                    ip_address=file_access.first().ip_address,
                    action=file_access.first().action,
                    file_name=file_access.first().file_name,
                    threat_type='CredentialStuffing',
                    severity='High'
                )