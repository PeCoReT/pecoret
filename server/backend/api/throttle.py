from rest_framework.throttling import UserRateThrottle


class AuthFlowThrottle(UserRateThrottle):
    """throttle the authentication flow.
    This tries to make brute forcing credentials a bit harder for the attacker.
    """
    scope = "auth_flow_throttle"
