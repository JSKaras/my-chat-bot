#-*- coding: utf-8 -*-
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from message.models import Reservation, History

import json
import sys

#sys.path.insert(0, './mybot')
from .mybot import mybot_parser
from .mybot import mybot_response
from .mybot import mybot_operation
'''
	Command Format
	[command] [Options]
	command : 예약 - Reservate Pray & Fellowship Room 
			  에약취소 - Cancel Reservation
			  예약조회 - Search Reservations
	          ETC  - Not Decided 

		예약 Command Format
		[Room Name] [Reservate Time] [Use Time] (Name or Gender)
			Room Name - 기도실1~3, 201~208호
			Reservate Time - ex: 오후3시반, 오후3시20분, 15:30, 오후3:30, 지금...
			Use Time - 1시간20분, 40분, 1:30 ..
			Name or Gender - Not Decided
		
		예약취소 Command Format
		[Room Name] [Reservate Time]
			Reservate Time - ex: 오후3시반, 오후3시20분, 15:30, 오후3:30...

	Example:
		예약 기도실1 오후3시반 40분
		예약조회 기도실1 
		예약취소 기도실1 오후3시반
'''

USAGE_STRING = "'Command Format\n"\
               " [command] [Options]\n"\
			   " 	command : 예약 - Reservate Pray & Fellowship Room\n"\
			   "    		  에약취소 - Cancel Reservation\n"\
			   "			  예약조회 - Search Reservations\n\n"\
			   "	 예약 Command Format\n"\
			   "	 [Room Name] [Reservate Time] [Use Time] (Name or Gender)\n"\
			   "		Room Name - 기도실1~3, 201~208호\n"\
			   "		Reservate Time - ex: 오후3시반, 오후3시20분, 15:30, 오후3:30, 지금...\n"\
			   "		Use Time - 1시간20분, 40분, 1:30 ..\n"\
			   "		Name or Gender - Not Decided\n"\
			   "	 예약취소 Command Format\n\n"\
			   "		[Room Name] [Reservate Time]\n"\
			   "		Reservate Time - ex: 오후3시반, 오후3시20분, 15:30, 오후3:30...\n\n"\
			   " Example:\n"\
			   "		예약 기도실1 오후3시반 40분\n"\
			   "		예약조회 기도실1 \n"\
			   "		예약취소 기도실1 오후3시반'"

@csrf_exempt
def response(request):
	method = request.method

	print ("/message/")

	if method == 'POST': # Request From User
		json_str = ((request.body).decode('utf-8')) # Get body String
		try :
			json_data = json.loads(json_str) # Load Json
			param_list = mybot_parser.parser(json_data['content']) # Parse bot command
		except Exception as err:
			print ('Error (%s)'%str(err))
			return JsonResponse(mybot_response.get_resbody('알수없는 명령 입니다.')) 


		if param_list == None:
			return JsonResponse(mybot_response.get_resbody('잘못된 명령 입니다.')) 
		req_commnd = param_list['command']
		# TODO : Command Dictionary Set
		resbody = mybot_operation.operation(param_list)
		if resbody == None:
			return JsonResponse(mybot_response.get_resbody('잘못된 명령 입니다.')) 
		return JsonResponse(resbody) # Send Reponse

	# Not Supported Methods
	elif method == 'GET':
		return JsonResponse(mybot_response.get_resbody('잘못된 명령 입니다.'))
	elif method == 'DELETE': 
		return JsonResponse(mybot_response.get_resbody('잘못된 명령 입니다.'))
	elif method == 'PUT':
		return JsonResponse(mybot_response.get_resbody('잘못된 명령 입니다.'))
	else:
		return JsonResponse(mybot_response.get_resbody('잘못된 명령 입니다.'))

@csrf_exempt
def history_response(request):
	method = request.method

	print ("/message/history/")

	if method == 'POST':
		if mybot_operation.setHistory() == 0 :	
			return HttpResponse(status=200)
	elif method == 'GET':
		return HttpResponse(status=400, reason='Not Supported Method')
	elif method == 'DELETE':
		if mybot_operation.deleteHistory() == 0:
			return HttpResponse(status=200)
	elif method == 'PUT':
		return HttpResponse(status=400, reason='Not Supported Method')
	return HttpResponse(status=400, reason='Not Supported Method')

