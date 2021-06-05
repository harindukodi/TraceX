from boto3.dynamodb.conditions import Key
from django.http import JsonResponse
from django.shortcuts import render
import json
import datetime
import os
import logging
import requests
import boto3
from botocore.exceptions import ClientError
import datetime

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def render_index(request):
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    return render(request, 'index.html')


@csrf_exempt
def admin_page(request):
    user_name = request.session.get('user_name')
    # request.session['Test'] = 'harindukodi'
    # Test = request.session.get('Test')
    # print(Test)
    # args['mytext'] = text
    return render(request, 'admin_page.html', {'user_name': user_name})


@csrf_exempt
def subscription_page(request):
    return render(request, 'subscription_page.html')


@csrf_exempt
def query_page(request):
    return render(request, 'query_page.html')


@csrf_exempt
def user_login_submit(request):
    request.session['user_id'] = ''
    request.session['user_name'] = ''
    login_response = ''
    data_json = json.loads(request.body)
    user_id = data_json['user_id']
    user_password = data_json['user_password']

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.client('dynamodb')

    try:
        table_data = dynamodb_client.get_item(TableName='login', Key={'email': {"S": str(user_id)}})
        print(table_data)
        data = table_data['Item']
        print(data)

        if str(data['email'].get('S')) == str(data['email'].get('S')) and str(data['password'].get('S')) == str(
                user_password):
            print('Login Success')

            if str(data['status'].get('S')) == "admin":
                login_response = 'admin'
            else:
                login_response = 'success'

            request.session['user_id'] = user_id
            request.session['user_name'] = data['user_name'].get('S')
        else:
            print('Invalid credentials')
            login_response = 'invalid'
    except Exception as e:
        login_response = 'invalid'
        print('exception')
        print(e)

    print(login_response)

    return JsonResponse(login_response, safe=False)

@csrf_exempt
def create_music_table(request):
    table_creation_response = ''

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.client('dynamodb')

    try:
        table = dynamodb_client.create_table(TableName='music', KeySchema=[
            {
                'AttributeName': 'artist',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ], AttributeDefinitions=[
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ], ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
                                             )

        print(table)
        table_creation_response = 'success'

    except Exception as e:
        table_creation_response = 'error'
        print('create_music_table exception')
        print(e)

    return JsonResponse(table_creation_response, safe=False)

@csrf_exempt
def load_music_data(request):
    load_music_data_response = ''

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.client('dynamodb')

    try:
        file_path = 'media/a2.json'
        with open(file_path) as json_file:
            song_list = json.load(json_file)

    except Exception as e:
        print('Exception in loading JSON')
        print(e)

    try:
        for song in song_list['songs']:
            dynamodb_client.put_item(TableName='music', Item={
                "title": {"S": song['title']},
                "artist": {"S": song['artist']},
                "year": {"N": song['year']},
                "web_url": {"S": song['web_url']},
                "img_url": {"S": song['img_url']}
            })
            title = song['title']
            artist = song['artist']
            print("Adding song: ", title, artist)

        load_music_data_response = 'success'

    except Exception as e:
        load_music_data_response = 'error'
        print('create_music_table exception')
        print(e)

    return JsonResponse(load_music_data_response, safe=False)

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
def forum_page(request):
    user_name = request.session.get('user_name')
    print(user_name)

    return render(request, 'forum.html',
                  {'user_name': user_name})

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
    verified_user = 'no'
    data_json = json.loads(request.body)
    reg_user_id = data_json['reg_user_id']
    reg_username = data_json['reg_username']
    reg_password = data_json['reg_password']

    session = boto3.Session(
        aws_access_key_id='AKIAZ5SN7YW33BSZ2MML',
        aws_secret_access_key='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',
        region_name='us-east-1')
    dynamodb_client = session.client('dynamodb')

    try:
        table_data = dynamodb_client.get_item(TableName='login', Key={'email': {"S": str(reg_user_id)}})
        print(table_data)
        data = table_data['Item']
        print(data)
        print(data['email'].get('S'))
        verified_user = 'no'
        register_response = 'invalid_userid'
    except Exception as e:
        verified_user = 'yes'
        print('exception')
        print(e)

    if verified_user == 'yes':
        print('Verified user')
        response = dynamodb_client.put_item(TableName='login', Item={
            "email": {"S": str(reg_user_id)},
            "password": {"S": str(reg_password)},
            "status": {"S": "user"},
            "user_name": {"S": str(reg_username)}
        })
        print(response)
        register_response = 'valid_user'

    return JsonResponse(register_response, safe=False)

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