from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework import serializers
from main import models


@extend_schema(
    summary="Obtain JWT token pair (access and refresh) for user authentication.",
    description="""
    Endpoint to log in users and receive a JWT access and refresh token pair.
    Requires username and password to be provided in the request body.
    """,
    request=inline_serializer( # Describe the expected request body
        name='TokenObtainRequestSerializer',
        fields={
            'username': serializers.CharField(help_text="Username for authentication"),
            'password': serializers.CharField(help_text="Password for authentication"),
        }
    ),
    responses={
        200: inline_serializer( # Document successful 200 response
            name='TokenObtainResponseSerializer',
            fields={
                'refresh': serializers.CharField(help_text="JWT refresh token"),
                'access': serializers.CharField(help_text="JWT access token"),
            }
        ),
        400: inline_serializer(  # Document 400 error response (bad request)
            name='TokenObtainError400Serializer',
            fields={'error': serializers.CharField(help_text="Error message, e.g., 'Please provide both username and password.'")}
        ),
        401: inline_serializer( # Document 401 error (unauthorized)
            name='TokenObtainError401Serializer',
            fields={'error': serializers.CharField(help_text="Error message, e.g., 'Invalid credentials' or 'User account is inactive.'")}
        ),
    },
    examples=[  # Example request and response for Swagger/Redoc UI
        OpenApiExample(
            name='Valid Login Request', # Example for request only
            description='Example of a successful login attempt request.',
            request_only=True, # This is a REQUEST example
            value={         # This 'value' is for the REQUEST
                'username': 'testuser',
                'password': 'password123',
            },
        ),
        OpenApiExample(
            name='Valid Login Response', # Separate example for response
            description='Example of a successful login response with tokens.',
            response_only=True, # This is a RESPONSE example
            status_codes=['200'],
            value={         # This 'value' is for the RESPONSE
                'refresh': '...',
                'access': '...',
            },
        ),
        OpenApiExample( # Error Example is a response example
            name='Invalid Credentials Error',
            description='Example error for invalid login.',
            response_only=True,
            status_codes=['401'],
            value={'error': 'Invalid credentials'},
        ),
    ],
    tags=['Authentication'], # Tag this endpoint for OpenAPI schema
)
@api_view(['POST'])
@permission_classes([AllowAny])
def getTokensForUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"error": "Please provide both username and password."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password) 

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {"error": "User account is inactive."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user) 
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


    return Response(tokens, status=status.HTTP_200_OK)


@extend_schema(
    summary="Refresh an access token using a refresh token.",
    description="""
    Endpoint to obtain a new access token by providing a valid refresh token in the request body.
    The refresh token must be valid and not expired.
    """,
    request=inline_serializer(  # Describe refresh token request body
        name='TokenRefreshRequestSerializer',
        fields={'refresh': serializers.CharField(help_text="Valid JWT refresh token")}
    ),
    responses={
        200: inline_serializer(  # Document successful 200 response
            name='TokenRefreshResponseSerializer',
            fields={'access': serializers.CharField(help_text="New JWT access token")}
        ),
        400: inline_serializer( # Document 400 (missing refresh token)
            name='TokenRefreshError400Serializer',
            fields={'error': serializers.CharField(help_text="Error message, e.g., 'Refresh token is required.'")}
        ),
        401: inline_serializer(  # Document 401 (invalid or expired refresh)
            name='TokenRefreshError401Serializer',
            fields={'error': serializers.CharField(help_text="Error message, e.g., 'Invalid or expired refresh token.'")}
        ),
    },
    examples=[ # Example request/response for refresh endpoint
        OpenApiExample(
            name='Valid Refresh Request', # Clearer name: REQUEST only
            description='Example of a valid refresh token request body.',
            request_only=True, # IMPORTANT:  request_only=True
            value={'refresh': 'your_refresh_token_value...'} # 'value' for REQUEST only
        ),
        # 2. SUCCESSFUL RESPONSE EXAMPLE (Status 200)
        OpenApiExample(
            name='Successful Refresh Response', # Clearer name: RESPONSE only
            description='Example of a successful refresh, providing a new access token.',
            response_only=True,
            status_codes=['200'],
            value={'access': 'new_access_token_value...'}
        ),
        OpenApiExample(
            name='Invalid Refresh Token Error', 
            description='Example of an error when an invalid refresh token is provided.',
            response_only=True,
            status_codes=['401'],
            value={'error': 'Invalid or expired refresh token.'} 
        ),
    ],
    tags=['Authentication'], 
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refreshAccessToken(request):

    refresh_token_value = request.data.get('refresh')

    if not refresh_token_value:
        return Response(
            {"error": "Refresh token is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh = RefreshToken(refresh_token_value) 
        access_token = refresh.access_token  
        return Response({
            'access': str(access_token),
            }, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response(
            {"error": "Invalid or expired refresh token."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    







    