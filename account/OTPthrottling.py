from rest_framework.throttling import SimpleRateThrottle





class OTPThrottle(SimpleRateThrottle):
    scope = 'otp'

    def get_cache_key(self, request, view):
        phone = request.data.get('phone')
        if not phone:
            return self.get_ident(request)  
        return f"throttle_otp_{phone}"


