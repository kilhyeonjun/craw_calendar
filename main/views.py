from django.shortcuts import render
from .models import Craw
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from .forms import LoginForm
from .Craw_inha import Craw_inha
from django.db import connections
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.models import User
# index.html 페이지를 부르는 index 함수
def index(request):
    return render(request, 'main/index.html')

def logout(request):
    django_logout(request)
    return render(request, 'main/index.html')

def login(request):
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            a = Craw_inha(username, password)
            b = a.crawStart()
            # 인증에 성공했을 경우
            if (b == "로그인 성공"):
                user = authenticate(
                    username=username,
                    password=password
                )
                if user:
                    print("user존재")
                else:
                    #회원가입
                    user = User.objects.create_user(**login_form.cleaned_data)
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)

                craw_list = a.craw()
                conn = None
                cur = None
                sql = ""
                try:
                    # db연결
                    conn = connections['default']
                    cur = conn.cursor()

                    # db 테이블 비우기
                    cur.execute("truncate craw")
                    conn.commit()
                except Exception as ex:
                    return render(request, 'main/login.html', {'err': '데이터베이스연동을 실패했습니다.'})
                else:
                    print("db connect")

                # db 데이터 입력
                try:
                    for temp in craw_list:
                        print(temp)
                        sql = "INSERT INTO craw (id, lName, title, degree, aCheck, con, sDate, eDate) VALUES('" + username + "', '" + \
                              temp[0] + "', '" + temp[1] \
                              + "', '" + temp[2] + "', '" + temp[3] + "', '" + temp[4] + "', '" + temp[5] + "', '" + \
                              temp[
                                  6] + "')"

                        cur.execute(sql)
                        conn.commit()
                except Exception as ex:
                    print("data err", ex)
                    conn.close()
                    return render(request, 'main/login.html', {'err': '서버오류'})
                else:
                    print("data good")
                    conn.close()
                    return render(request, 'main/calendar.html')
            else:
                return render(request, 'main/login.html', {'err': '로그인 실패! 아이디와 패스워드를 확인해주세요.'})
        else:
            login_form = LoginForm()
            context = {
                'login_form': login_form,
            }
        return render(request, 'main/login.html', context)
    return render(request, 'main/login.html')


def calendar(request):
    if request.user.is_authenticated:
        return render(request, 'main/calendar.html')
    else:
        return render(request, 'main/login.html')

def craw_list_db(request):
    Craws = Craw.objects.all()
    craw_lists = []
    for craw in Craws:
        if (craw.degree != "[마감]") and (craw.acheck != "제출정보보기"):
            craw_list = {}
            craw_list["title"]=craw.lname
            craw_list["start"]=(craw.sdate).strftime('%Y-%m-%dT%H:%M:%S')
            craw_list["end"]=(craw.edate).strftime('%Y-%m-%dT%H:%M:%S')
            craw_list["extendedProps"]=        {
                'lname' : craw.title,
                'acheck ': craw.acheck ,
                'con': craw.con,

            }
            craw_lists.append(craw_list)
    return JsonResponse(craw_lists, safe=False)

def test(request):
    return render(request, 'main/test.html')