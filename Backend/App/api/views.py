from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, ChatMessage, Conversation
from .serializers import ProductSerializer, ChatMessageSerializer, ConversationSerializer


# -----------------------------
# 🟢 JWT Token & Auto-Create
# -----------------------------
class AutoCreateTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        else:
            if not user.check_password(password):
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


# -----------------------------
# 🟢 User Registration
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        password=make_password(password)
    )
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


# -----------------------------
# 🟢 Product Endpoints
# -----------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query)
    return Response(ProductSerializer(results, many=True).data)


# -----------------------------
# 🟢 Chatbot (Authenticated)
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_response(request):
    user_input = request.data.get("message", "").lower()
    user = request.user

    # Save user message
    Conversation.objects.create(user=user, sender="user", message=user_input)

    # Basic logic
    if any(word in user_input for word in ["hi", "hello", "hey"]):
        bot_reply = "Hi there! How can I help you today?"
    elif "thank" in user_input:
        bot_reply = "You're welcome!"
    else:
        matches = Product.objects.filter(Q(name__icontains=user_input) | Q(description__icontains=user_input))
        if matches.exists():
            serializer = ProductSerializer(matches, many=True)
            return Response({"products": serializer.data})

        bot_reply = "Sorry, I couldn't find anything matching your query."

    # Save bot response
    Conversation.objects.create(user=user, sender="bot", message=bot_reply)

    return Response({"message": bot_reply})


# -----------------------------
# 🟢 Chat History
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_history(request):
    history = Conversation.objects.filter(user=request.user).order_by('timestamp')
    serializer = ConversationSerializer(history, many=True)
    return Response(serializer.data)


# -----------------------------
# 🟢 Save ChatMessage (Optional)
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_chat_message(request):
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request):
    messages = ChatMessage.objects.all().order_by('timestamp')
    return Response(ChatMessageSerializer(messages, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = User.objects.all().values('id', 'username')
    return Response(list(users))

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=username)
        user.set_password(password)  # IMPORTANT: hashes password
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)