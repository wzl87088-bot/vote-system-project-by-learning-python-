from django.shortcuts import render,redirect
from polls.models import Subject,Teacher
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from polls.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from polls.utils import generate_captcha
def show_subjects(request):
    subjects = Subject.objects.all().order_by('no')
    return render(request,'subjects.html',{'subjects': subjects})

def show_teachers(request):
    try:
        sno = int(request.GET.get('sno'))
        subject = Subject.objects.get(no=sno)
        teachers = Teacher.objects.filter(subject=subject).order_by('no')
    except(TypeError,ValueError,Subject.DoesNotExist):
        return redirect('/')

    return render(request,'teachers.html',{
        'subject':subject,
        'teachers':teachers,
    })
# Create your views here.
@require_POST
def praise_or_criticize(request):
    if not request.session.get('userid'):
        return JsonResponse({
            'code': 20002,
            'mesg': '请先登录',
        }, status=401)
    try:
        tno=int(request.POST.get('tno'))
        teacher = Teacher.objects.get(no=tno)
    except(TypeError,ValueError,Teacher.DoesNotExist):
        return JsonResponse({
            'code':20001,
            'mesg':'老师编号无效',
        },status=400)

    if request.path =='/praise/':
        teacher.good_count +=1
        count = teacher.good_count
    else:
        teacher.bad_count +=1
        count = teacher.bad_count

    teacher.save()

    return JsonResponse({
        'code':20000,
        'mesg':'操作成功',
        'count':count,
    })
def login(request):
    hint = ''

    if request.method == 'POST':
        captcha = request.POST.get('captcha', '').strip().upper()
        expected = request.session.pop('captcha', '')

        if not expected or captcha != expected:
            return render(request, 'login.html', {
                'hint': '验证码错误或已失效，请重新输入',
            })
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            request.session.cycle_key()
            request.session['userid'] = user.no
            request.session['username'] = user.username
            return redirect('/')

        hint = '用户名或密码错误'

    return render(request, 'login.html', {'hint': hint})

@require_POST
def logout(request):
    request.session.flush()
    return redirect('/')

@never_cache
def get_captcha(request):
    code, image_data = generate_captcha()
    request.session['captcha'] = code
    return HttpResponse(image_data, content_type='image/png')
