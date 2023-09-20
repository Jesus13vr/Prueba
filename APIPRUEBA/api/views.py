from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class login(APIView):
    template_name="login.html"
    def get(self, request):
        return render(request,self.template_name)
class inicio(APIView):
    template_name="inicio.html"
    def get(self, request):
        return render(request,self.template_name)