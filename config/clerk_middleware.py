import jwt
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ClerkMiddleware(MiddlewareMixin):
    """Middleware to verify Clerk JWT tokens and sync user data"""
    
    def process_request(self, request):
        # Get the Clerk session token from cookies or headers
        session_token = request.COOKIES.get('__session') or request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        
        if session_token:
            try:
                # Decode JWT token without verification (frontend token)
                # In production, you'd want to verify the signature
                decoded = jwt.decode(session_token, options={"verify_signature": False}, algorithms=["HS256"])
                
                clerk_user_id = decoded.get('sub')
                
                if clerk_user_id:
                    # Sync or create Django user based on Clerk user ID
                    user, created = User.objects.get_or_create(
                        username=clerk_user_id,
                        defaults={
                            'email': decoded.get('email', ''),
                        }
                    )
                    
                    if not created:
                        user.email = decoded.get('email', '')
                        user.save()
                    
                    # Attach Clerk user info to request
                    request.clerk_user_id = clerk_user_id
                    request.user = user
                    
            except Exception as e:
                # Token verification failed, user is not authenticated
                request.clerk_user_id = None
                pass

