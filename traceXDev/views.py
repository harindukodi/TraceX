from boto3.dynamodb.conditions import Key
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import json
import pandas as pd
import datetime
import os
import logging
import requests
import boto3
from botocore.exceptions import ClientError
import datetime

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
# from requests_aws4auth import AWS4Auth
from requests_aws4auth import AWS4Auth
# from aws_requests_auth.aws_auth import AWSRequestsAuth
from commute.models import commute_table
from traceXDev.forms import Form
from traceXDev.models import test_table_new
from traceXusers.models import user_info_table
from users.models import user_tracking_table


@csrf_exempt
def render_index(request):
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    print('TEST DB')
    table_obj = test_table_new.objects.get(name='harindu')
    print(table_obj)
    table_obj_name = table_obj.name
    # connect_with_quicksight()
    return render(request, 'index.html', {'test': table_obj_name})


@csrf_exempt
def admin_page(request):
    user_id = request.session.get('user_id')
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    return render(request, 'administrator.html', {'user_id': user_id})


@csrf_exempt
def admin_add_commute_page(request):
    user_id = request.session.get('user_id')
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    return render(request, 'admin_add_commute.html', {'user_id': user_id})


@csrf_exempt
def admin_view_all_commutes_page(request):
    user_id = request.session.get('user_id')
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    return render(request, 'admin_view_all_commutes.html', {'user_id': user_id})


@csrf_exempt
def admin_search_commutes_page(request):
    user_id = request.session.get('user_id')
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    return render(request, 'admin_search_commutes.html', {'user_id': user_id})


@csrf_exempt
def subscription_page(request):
    return render(request, 'subscription_page.html')


@csrf_exempt
def query_page(request):
    return render(request, 'query_page.html')


@csrf_exempt
def user_view_all_commutes(request):
    return render(request, 'user_view_all_commutes.html')


@csrf_exempt
def user_login_submit(request):
    request.session['user_id'] = ''
    request.session['user_name'] = ''
    login_response = ''
    data_json = json.loads(request.body)
    user_id = data_json['user_id']
    user_password = data_json['user_password']

    # admin_email = 'harindukodi@outlook.com'
    # admin_password = '1234'

    try:
        if user_info_table.objects.filter(user_email=str(user_id), user_password=user_password).exists():
            print('User exists')
            user_info_table_obj = user_info_table.objects.filter(user_email=str(user_id), user_password=user_password)

            for user in user_info_table_obj:
                if user.user_access_level == 'admin':
                    login_response = 'admin'
                    request.session['user_id'] = user_id
                else:
                    login_response = 'success'
                    request.session['user_id'] = user_id
        else:
            login_response = 'invalid'
        # if user_id == admin_email and user_password == admin_password:
        #     print('Admin login Success')
        #
        #     login_response = 'admin'
        #     request.session['user_id'] = user_id
        # else:
        #     login_response = 'success'
        #     request.session['user_id'] = user_id
    except Exception as e:
        login_response = 'invalid'
        print('exception')
        print(e)

    print(login_response)

    return JsonResponse(login_response, safe=False)


@csrf_exempt
def add_commute(request):
    print('add_commute method')
    commute_table_creation_response = ''
    data_json = json.loads(request.body)
    new_commute_type = data_json['new_commute_type']
    new_commute_name = data_json['new_commute_name']
    new_commute_month = data_json['new_commute_month']
    new_commute_day = data_json['new_commute_day']
    new_commute_year = data_json['new_commute_year']
    new_commute_hour = data_json['new_commute_hour']
    new_commute_minute = data_json['new_commute_minute']
    new_commute_ampm = data_json['new_commute_ampm']
    new_commute_alert = data_json['new_commute_alert']

    commute_table_obj = commute_table(
        commute_type=str(new_commute_type), commute_name=str(new_commute_name),
        commute_month=str(new_commute_month),
        commute_day=str(new_commute_day),
        commute_year=str(new_commute_year),
        commute_hour=str(new_commute_hour),
        commute_minutes=str(new_commute_minute),
        commute_ampm=str(new_commute_ampm),
        commute_alert=str(new_commute_alert),
        commute_passenger_count=str(0),
    )
    commute_table_obj.save()
    commute_table_creation_response = 'success'
    print(commute_table_creation_response)

    return JsonResponse(commute_table_creation_response, safe=False)


@csrf_exempt
def get_all_commute_data(request):
    load_music_data_response = ''

    commute_objects = commute_table.objects.all().values()
    df = pd.DataFrame(commute_objects)
    print(df)
    df = df.drop('id', 1)
    json_converted = df.to_json(orient='records')
    print(json_converted)
    return JsonResponse(json_converted, safe=False)


@csrf_exempt
def get_user_commute_data(request):
    user_commute_data = []
    user_id = request.session.get('user_id')

    if user_tracking_table.objects.filter(user_email=user_id).exists():
        user_tracking_objects = user_tracking_table.objects.filter(user_email=user_id)
        print(user_tracking_objects)
        for obj in user_tracking_objects:
            user_commute_data.append(
                {'commute_type': obj.commute_type, 'commute_name': obj.commute_name, 'commute_year': obj.commute_year,
                 'commute_month': obj.commute_month, 'commute_day': obj.commute_day, 'commute_hour': obj.commute_hour,
                 'commute_minutes': obj.commute_minutes, 'commute_ampm': obj.commute_ampm,
                 'commute_alert': obj.commute_alert})

        print(user_commute_data)
        json_data = json.dumps(user_commute_data)
    else:
        print('No User data')
        json_data = 'No Data'

    print(json_data)

    # df = pd.DataFrame.from_records(user_tracking_objects)
    # df = pd.DataFrame(user_tracking_objects)
    # print(df)
    # df = df.drop('id', 1)
    # json_converted = df.to_json(orient='records')
    # print(json_converted)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def mark_commute_action(request):
    json_converted = ''
    email_count = ''
    user_email_list = []

    data_json = json.loads(request.body)
    commute_type = data_json['commute_type']
    commute_name = data_json['commute_name']
    commute_year = data_json['commute_year']
    commute_month = data_json['commute_month']
    commute_day = data_json['commute_day']
    commute_hour = data_json['commute_hour']
    commute_minutes = data_json['commute_minutes']
    commute_ampm = data_json['commute_ampm']
    commute_alert = data_json['commute_alert']
    action = data_json['action']

    print(commute_type)
    print(commute_year)
    print(action)

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='ap-southeast-1')

    commute_table_obj = commute_table.objects.filter(
        commute_type=str(commute_type), commute_name=str(commute_name),
        commute_month=str(commute_month),
        commute_day=str(commute_day),
        commute_year=str(commute_year),
        commute_hour=str(commute_hour),
        commute_minutes=str(commute_minutes),
        commute_ampm=str(commute_ampm),
        commute_alert=str(commute_alert))

    if not commute_table_obj:
        print('No matching commute data')
        response = 'no_data'
    else:
        for obj in commute_table_obj:
            print('Matching record')
            print(obj.commute_name)
            commute_table.objects.filter(
                commute_type=str(commute_type), commute_name=str(commute_name),
                commute_month=str(commute_month),
                commute_day=str(commute_day),
                commute_year=str(commute_year),
                commute_hour=str(commute_hour),
                commute_minutes=str(commute_minutes),
                commute_ampm=str(commute_ampm),
                commute_alert=str(commute_alert)).update(commute_alert=str(action))

            user_tracking_table_obj = user_tracking_table.objects.filter(
                commute_type=str(commute_type), commute_name=str(commute_name),
                commute_month=str(commute_month),
                commute_day=str(commute_day),
                commute_year=str(commute_year),
                commute_hour=str(commute_hour),
                commute_minutes=str(commute_minutes),
                commute_ampm=str(commute_ampm))

            if not user_tracking_table_obj:
                print('No matching user tracking data')
                response = 'no_data'
            else:
                for user_obj in user_tracking_table_obj:
                    print('Matching user tracking record')
                    print(user_obj.user_email)
                    user_email_list.append(user_obj.user_email)

            # payload = {'user_email_list': user_email_list}
            # lambda_client = session.client('lambda')
            #
            # response = lambda_client.invoke(FunctionName='TracexSendUserEmail',
            #                                 Payload=json.dumps(payload))
            # payload = (response['Payload'])
            # print(payload)

            # auth = AWSRequestsAuth(aws_access_key='AKIAZ5SN7YW33BSZ2MML',
            #                        aws_secret_access_key='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',
            #                        # aws_token=credentials.token,
            #                        aws_host='pnoe7c6ci9.execute-api.ap-southeast-1.amazonaws.com',
            #                        aws_region='ap-southeast-1',
            #                        aws_service='execute-api')
            #
            # response = requests.get('https://pnoe7c6ci9.execute-api.ap-southeast-1.amazonaws.com/default'
            #                         '/TracexSendUserEmail?user_email_list=" + str(user_email_list)', auth=auth)
            #
            # print(response.content)

            if len(user_email_list) > 0:
                url = "https://pnoe7c6ci9.execute-api.ap-southeast-1.amazonaws.com/default/TracexSendUserEmail" \
                      "?user_email_list=" + str(user_email_list) + "&commute_type=" + \
                      str(commute_type) + "&commute_name=" + str(commute_name) + "&commute_month=" + \
                      str(commute_month) + "&commute_day=" + str(commute_day) + "&commute_year=" + \
                      str(commute_year) + "&commute_hour=" + str(commute_hour) + "&commute_minutes=" + \
                      str(commute_minutes) + "&commute_ampm=" + str(commute_ampm) + "&action=" + \
                      str(action)

                auth = AWS4Auth('AKIAZ5SN7YW33BSZ2MML', 'SixER2DjIxvC0ON7S47fKkHX6XCzH9940zuaoSYI', 'ap-southeast-1',
                                'execute-api')

                response = requests.post(url, auth=auth)
                print(response)
                print(response.text)
                json_converted = response.text
                email_count = len(user_email_list)
            else:
                print('Obj empty')
                email_count = len(user_email_list)

    print(user_email_list)

    return JsonResponse(email_count, safe=False)


@csrf_exempt
def user_subscribe_commute(request):
    json_converted = ''
    email_count = ''
    user_email_list = []
    user_id = request.session.get('user_id')

    data_json = json.loads(request.body)
    commute_type = data_json['commute_type']
    commute_name = data_json['commute_name']
    commute_year = data_json['commute_year']
    commute_month = data_json['commute_month']
    commute_day = data_json['commute_day']
    commute_hour = data_json['commute_hour']
    commute_minutes = data_json['commute_minutes']
    commute_ampm = data_json['commute_ampm']
    commute_alert = data_json['commute_alert']
    action = data_json['action']

    print(commute_type)
    print(commute_year)
    print(action)

    user_tracking_obj = user_tracking_table(user_email=str(user_id),
                                            commute_type=str(commute_type), commute_name=str(commute_name),
                                            commute_month=str(commute_month),
                                            commute_day=str(commute_day),
                                            commute_year=str(commute_year),
                                            commute_hour=str(commute_hour),
                                            commute_minutes=str(commute_minutes),
                                            commute_ampm=str(commute_ampm),
                                            commute_alert=str(commute_alert),
                                            )
    user_tracking_obj.save()

    commute_table_obj = commute_table.objects.filter(
        commute_type=str(commute_type), commute_name=str(commute_name),
        commute_month=str(commute_month),
        commute_day=str(commute_day),
        commute_year=str(commute_year),
        commute_hour=str(commute_hour),
        commute_minutes=str(commute_minutes),
        commute_ampm=str(commute_ampm),
        commute_alert=str(commute_alert))

    if not commute_table_obj:
        print('No matching commute data')
        response = 'no_data'
    else:
        for obj in commute_table_obj:
            print('Matching record')
            print(obj.commute_passenger_count)
            new_count = int(obj.commute_passenger_count) + 1
            commute_table.objects.filter(
                commute_type=str(commute_type), commute_name=str(commute_name),
                commute_month=str(commute_month),
                commute_day=str(commute_day),
                commute_year=str(commute_year),
                commute_hour=str(commute_hour),
                commute_minutes=str(commute_minutes),
                commute_ampm=str(commute_ampm),
                commute_alert=str(commute_alert)).update(commute_passenger_count=str(new_count))

    print('user_subscribe_commute completed')

    return JsonResponse('done', safe=False)


@csrf_exempt
def download_artist_images(request):
    download_artist_images_response = ''

    create_bucket('s3763840-artist-images')

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    s3_client = session.client('s3')

    try:
        file_path = 'media/a2.json'
        with open(file_path) as json_file:
            song_list = json.load(json_file)

    except Exception as e:
        print('Exception in loading JSON')
        print(e)

    try:
        for song in song_list['songs']:
            img_url = str(song['img_url'])
            artist = str(song['artist'])
            r = requests.get(img_url)

            if not os.path.exists('media/images/'):
                os.makedirs('media/images/')

            file_path = 'media/images/' + artist + '.jpg'

            with open(file_path, "wb") as f:
                f.write(r.content)

            print("download image: ", artist)

            S3_BUCKET = 's3763840-artist-images'
            key = artist + '.jpg'
            s3_client.upload_file(file_path, S3_BUCKET, key)
            os.remove(file_path)

        download_artist_images_response = 'success'

    except Exception as e:
        download_artist_images_response = 'error'
        print('download_artist_images exception')
        print(e)

    return JsonResponse(download_artist_images_response, safe=False)


@csrf_exempt
def user_home_page(request):
    user_id = request.session.get('user_id')
    print(user_id)

    return render(request, 'user_home_page.html',
                  {'user_id': user_id})


@csrf_exempt
def create_bucket(bucket_name, region=None):
    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    s3_client = session.client('s3')
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            # s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            # s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name)
        print(bucket_name + ' created.')
    except ClientError as e:
        logging.error(e)
        return False
    return True


@csrf_exempt
def registration_page(request):
    return render(request, 'registration.html')


@csrf_exempt
def register_user(request):
    register_response = ''
    data_json = json.loads(request.body)
    reg_user_id = data_json['reg_user_id']
    reg_password = data_json['reg_password']
    print(reg_user_id)
    print(reg_password)

    if user_info_table.objects.filter(user_email=str(reg_user_id)).exists():
        print('User exists')
        register_response = 'invalid_userid'
    else:
        print('User does not exist')
        user_info_table_obj = user_info_table(user_email=reg_user_id, user_password=str(reg_password),
                                              user_access_level='user')
        user_info_table_obj.save()
        register_response = 'valid_user'

        url = "https://59pq4rfmoi.execute-api.ap-southeast-1.amazonaws.com/default/TracexNewUserEmail" \
              "?user_email=" + str(reg_user_id)

        auth = AWS4Auth('AKIAZ5SN7YW33BSZ2MML', 'SixER2DjIxvC0ON7S47fKkHX6XCzH9940zuaoSYI', 'ap-southeast-1',
                        'execute-api')

        response = requests.post(url, auth=auth)
        print(response)
        print(response.text)

    return JsonResponse(register_response, safe=False)


@csrf_exempt
def connect_with_quicksight():
    print('connect_with_quicksight')
    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')

    # session = botocore.session.get_session()
    quicksight_client = session.client('quicksight', region_name='us-east-1')
    # quicksight_client = session.resource('quicksight')
    # client = session.create_client("quicksight", region_name='us-east-1')
    response = quicksight_client.get_dashboard_embed_url(AwsAccountId="681989621175",
                                                         DashboardId="2624b7cd-c80a-4bea-96ff-ea0416a64315",
                                                         IdentityType="IAM", SessionLifetimeInMinutes=100,
                                                         ResetDisabled=True,
                                                         UndoRedoDisabled=True)
    print(response)

    return JsonResponse('', safe=False)


@csrf_exempt
def get_subscription_data(request):
    send_data = ''
    json_data_list = []
    user_id = request.session.get('user_id')
    print(datetime.datetime.now())
    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.resource('dynamodb')
    table = dynamodb_client.Table('subscriptions')
    table_data = table.query(KeyConditionExpression=Key('email').eq(user_id))

    if len(table_data['Items']) > 0:
        print(table_data['Items'])
        print(table_data['Items'][0]['year'])

        for item in table_data['Items']:
            print(item)
            image_title = item['artist'].replace(' ', '+')
            print(image_title)
            user_image_path = "https://s3763840-artist-images.s3.amazonaws.com/" + image_title + ".jpg"

            json_data_list.append(
                {'title': item['title'], 'artist': item['artist'], 'year': int(item['year']),
                 'subTimeStamp': item['subTimeStamp'],
                 'email': item['email'], 'artist_image': user_image_path})

        print(json_data_list)
        send_data = json.dumps(json_data_list)
        print(send_data)

    else:
        print(table_data['Items'])
        send_data = 'no_data'

    return JsonResponse(send_data, safe=False)


@csrf_exempt
def remove_subscription_item(request):
    user_id = request.session.get('user_id')
    data_json = json.loads(request.body)
    title = data_json['title']
    artist = data_json['artist']
    subTimeStamp = data_json['subTimeStamp']

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.resource('dynamodb')
    table = dynamodb_client.Table('subscriptions')

    table_data = table.delete_item(Key={'email': str(user_id), 'subTimeStamp': subTimeStamp})
    print(table_data)

    return JsonResponse('done', safe=False)


@csrf_exempt
def submit_query(request):
    json_data_list = []
    user_id = request.session.get('user_id')
    data_json = json.loads(request.body)
    message_title = data_json['message_title']
    message_year = data_json['message_year']
    message_artist = data_json['message_artist']

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.resource('dynamodb')
    table = dynamodb_client.Table('music')

    # table_data = table.query(KeyConditionExpression=Key('email').eq(user_id))
    if message_title:
        print('Harindu')
        print(message_title)
        if message_year:
            if message_artist:
                print(message_title)
                print(message_year)
                print(message_artist)
                table_data = table.query(
                    KeyConditionExpression=
                    Key('title').eq(message_title) & Key('artist').eq(message_artist),
                    FilterExpression=Key('year').eq(int(message_year)),
                )
            else:
                table_data = table.scan(
                    FilterExpression=Key('year').eq(int(message_year)) & Key('title').eq(message_title),
                )
        elif message_artist:
            table_data = table.query(
                KeyConditionExpression=
                Key('title').eq(message_title) & Key('artist').eq(message_artist)
            )
        else:
            table_data = table.scan(
                FilterExpression=
                Key('title').eq(message_title)
            )
    elif message_year:
        if message_artist:
            table_data = table.query(
                KeyConditionExpression=
                Key('artist').eq(message_artist),
                FilterExpression=Key('year').eq(int(message_year)),
            )
        else:
            table_data = table.scan(
                FilterExpression=Key('year').eq(int(message_year)),
            )
    else:
        if message_artist:
            table_data = table.query(
                KeyConditionExpression=
                Key('artist').eq(message_artist)
            )
        else:
            send_data = 'no_data'

    try:
        if len(table_data['Items']) > 0:
            print(table_data['Items'])
            print(table_data['Items'][0]['year'])

            for item in table_data['Items']:
                print(item)
                image_title = item['artist'].replace(' ', '+')
                print(image_title)
                user_image_path = "https://s3763840-artist-images.s3.amazonaws.com/" + image_title + ".jpg"

                json_data_list.append(
                    {'title': item['title'], 'artist': item['artist'], 'year': int(item['year']),
                     'artist_image': user_image_path})

            print(json_data_list)
            send_data = json.dumps(json_data_list)
            print(send_data)

        else:
            print(table_data['Items'])
            send_data = 'no_data'
            print('No Data')
    except Exception as e:
        print(e)
        send_data = 'no_data'

    return JsonResponse(send_data, safe=False)


@csrf_exempt
def subscribe_item(request):
    user_id = request.session.get('user_id')
    data_json = json.loads(request.body)
    title = data_json['title']
    artist = data_json['artist']
    year = data_json['year']
    timeStamp = datetime.datetime.now()

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    # dynamodb_client = session.resource('dynamodb')
    # table = dynamodb_client.Table('music')
    dynamodb_client = session.client('dynamodb')
    response = dynamodb_client.put_item(TableName='subscriptions', Item={
        "email": {"S": str(user_id)},
        "artist": {"S": str(artist)},
        "title": {"S": str(title)},
        "subTimeStamp": {"S": str(timeStamp)},
        "year": {"S": str(year)}
    })
    print(response)

    return JsonResponse("done", safe=False)


@csrf_exempt
def handle_uploaded_file(f):
    with open('media/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
def admin_upload_analytics_page(request):
    print('admin_upload_analytics_page')
    if request.method == 'POST':
        student = Form(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            print(request.FILES['file'])
            admin_upload_analytics(request, request.FILES['file'])
            return HttpResponse("File uploaded successfuly")
    else:
        student = Form()
        return render(request, 'admin_upload_analytics.html', {'form': student})
    # return render(request, 'admin_upload_analytics.html')


@csrf_exempt
def admin_upload_analytics(request, name):
    download_artist_images_response = ''
    name_new = str(name)
    # create_bucket('s3763840-artist-images')

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    s3_client = session.client('s3')

    try:
        file_path = 'media/' + name_new
        S3_BUCKET = 'elasticbeanstalk-us-east-1-681989621175'
        path = 'media/'
        key = path + name_new
        s3_client.upload_file(file_path, S3_BUCKET, key)
        os.remove(file_path)

        download_artist_images_response = 'success'

    except Exception as e:
        download_artist_images_response = 'error'
        print('download_artist_images exception')
        print(e)

    return JsonResponse(download_artist_images_response, safe=False)
