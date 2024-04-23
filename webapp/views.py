from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cx_Oracle
import json
import platform
# import sqlalchemy
import sqlalchemy

db = sqlalchemy.create_engine(
    'oracle+cx_oracle://BULLFLIX_PY/usf1956!@reade.forest.usf.edu:1521/cdb9', echo=False)


def index(request):
    return render(request, 'index.html')


def login(request):
    # render html from file
    return render(request, 'login.html')


@csrf_exempt
def signup_post(request):
    # check for post request

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method. Use POST.'})

    if request.content_type != 'application/json':
        return JsonResponse({'success': False, 'message': 'Invalid request format. Content-Type must be application/json.'})

    if not request.body:
        return JsonResponse({'success': False, 'message': 'Invalid request format. Request body is empty.'})

    # fetch body from request
    body = request.body.decode('utf-8')

    if not body:
        return JsonResponse({'success': False, 'message': 'Invalid request format. Request body is empty.'})

    # check if request body is json

    try:
        body = json.loads(body)
    except json.decoder.JSONDecodeError:

        return JsonResponse({'success': False, 'message': 'Invalid request format. Request body is not valid JSON.'})

    if body is not None:
        USER_NAME = body.get('name')
        EMAIL = body.get('email')
        passphrase = body.get('passphrase')

    else:
        return JsonResponse({'success': False, 'message': 'Invalid request format. Content-Type must be application/json.'})

    # Check if the user already exists
    # existing_user = USERS.query.filter_by(EMAIL=EMAIL.lower()).first()
    # if existing_user:
    #     return JsonResponse({'success': False, 'message': 'User already exists'})

        # Call the add_user stored procedure
    # connection = cx_Oracle.connect(user='BULLFLIX_PY', password='usf1956!', dsn='reade.forest.usf.edu:1521/cdb9')

    # connection = cx_Oracle.connect('BULLFLIX_PY/usf1956!@reade.forest.usf.edu:1521/cdb9')
    # cursor = connection.cursor()

    connect = db.connect()
    cur = connect.cursor()

    # Prepare the call to the stored procedure
    return_int = cur.var(cx_Oracle.NUMBER)
    cur.callproc('BULLFLIX.ADD_USER', [
                 USER_NAME, EMAIL, passphrase, return_int])
    connect.commit()

    # Check the return_int value to determine success
    if return_int.getvalue() == 1:
        print("success")
    else:
        print("updation failed")

    cur.close()
    connect.close()
    return redirect('login')


def signup(request):
    # check for post request
    if request.method == 'POST':
        print(request.POST)
        return signup_post(request)

    # render html from file
    return render(request, 'signup.html')


def logout(request):
    # render html from file
    return render(request, 'login.html')


def profile(request):
    # render html from file
    return render(request, 'profile.html')
