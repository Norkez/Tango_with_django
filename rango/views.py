from datetime import datetime


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context_dict)
    return response

def about(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    visits = request.session['visits']

    context_dict = {'my_name': 'Norkez', 'visits':visits}
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form =PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)

        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

# # def register(request):
#     registered = False

#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             profile.save()
#             registered = True

#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
    
#     return render(request, 
#                 'rango/register.html', 
#                 {'user_form': user_form, 
#                 'profile_form': profile_form,
#                 'registered': registered})

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username') 
#         password = request.POST.get('password')
#         # request.POST.get('val')은 변수가 없어도 에러를 내지 않고 None을 반환함.
#         # 반면에 request.POST['val']은 변수가 없다면 KeyError를 발생시킴.
#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your Rango account is diabled.")
#         else:
#             print("Invalid login details: {0}, {1}".format(username, password))
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})
    # return HttpResponse("Since you're loggined in, you can see this text!")

@login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))

def visitor_cookie_handler(request):
    # 사이트 접속 횟수를 얻는다.
    # COOKIES.get() 함수(장고 제공 함수)를 통해서 접속 횟수 쿠리를 얻을 수 있다.
    # 쿠키가 존재한다면 그 값이 인티저 값으로 변환되어 반환.
    # 쿠기가 없다면 기본 값으로 설정한 1이 반환
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    # 만약 마지막 방문이 하루 이상 지났다면
    if (datetime.now() - last_visit_time).days > 0 :
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val