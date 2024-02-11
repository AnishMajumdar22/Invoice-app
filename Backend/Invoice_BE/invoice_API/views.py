from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class Signup(APIView):
    def post(self, request):
        bodyData = request.data
        serializer = UserSerializer(data=bodyData)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created!"}, status=201)
        return Response(serializer.errors, status=400)


class Login(APIView):
    def post(self, request):
        bodyData = request.data
        serializer = LoginSerializer(data=bodyData)

        if serializer.is_valid():
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login Success!",
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                }
            )

        return Response(
            {"message": "Incorrect user-name or password", "error": serializer.errors},
            status=401,
        )


class Invoice_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invoice = Invoice.objects.all()
        serializer = InvoiceSerializer(invoice, many=True).data
        return Response(serializer, status=200)

    def post(self, request):
        bodyData = request.data
        serializer = InvoiceSerializer(data=bodyData)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Invoice added!", "data": serializer.data}, status=201
            )
        return Response(serializer.errors, status=400)


class Invoice_details(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        invoice = Invoice.objects.get(id=id)
        serializer = InvoiceSerializer(invoice).data
        return Response(serializer, status=201)


class Items_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        invoice = Invoice.objects.get(id=id)
        if invoice:
            bodyData = request.data
            serializer = ItemListSerializer(data=bodyData)
            if serializer.is_valid():
                serializer.save(invoice=invoice)
                return Response(
                    {"message": "Item has been added", "data": serializer.data},
                    status=201,
                )
            return Response(serializer.errors, status=400)
        return Response({"message": "Invoice not found!"}, status=404)
