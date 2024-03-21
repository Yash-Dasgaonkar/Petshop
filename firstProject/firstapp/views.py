from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.
def home(request):
    return HttpResponse("First View")

def firstpage(request):
    return HttpResponse("<h1>First Page</h1>")

def secondpage(request):
    school={
        "id":102,
        "school_name":"xaviers",
        "age":20}
    return render(request,"second.html",school)

    return HttpResponse("<h1>second page </h1>")

def users(request):
    student={
        "id":101,
        "name":"nikita",
        "age":18}
    return render(request,"index.html",student)

def register(request):
    return render(request,"register.html")

def submit(request):
    if request.method=="POST":
       return render(request,"submit.html")
    if request.method=="GET":
        return render(request,"register.html")
    #class based view
class firstView(View):
    def get(self,request):
        return HttpResponse("Class Based View -GET")
    
class secondView(View):
    name="Nisha"
    def get(self,request):
        return  render(request,"detail.html",{"name":self.name})
    

    

