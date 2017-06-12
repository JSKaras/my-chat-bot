from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
USAGE_STRING = 	"'Command Format\n"\
			    " [command] [Options]\n"\
				"    command : 예약 - Reservate Pray & Fellowship Room\n"\
				"              에약취소 - Cancel Reservation\n"\
				"              예약조회 - Search Reservations\n\n"\
				"     예약 Command Format\n"\
				"     [Room Name] [Reservate Time] [Use Time] (Name or Gender)\n"\
				"        Room Name - 기도실1~3, 201~208호\n"\
				"        Reservate Time - ex: 오후3시반, 오후3시20분, 15:30, 오후3:30, 지금...\n"\
				"        Use Time - 1시간20분, 40분, 1:30 ..\n"\
				"        Name or Gender - Not Decided\n"\
				"     예약취소 Command Format\n\n"\
				"        [Room Name] [Reservate Time]\n"\
				"        Reservate Time - ex: 오후3시반, 오후3시20분, 15:30, 오후3:30...\n\n"\
				" Example:\n"\
				"        예약 기도실1 오후3시반 40분\n"\
				"        예약조회 기도실1 \n"\
				"        예약취소 기도실1 오후3시반'"



@csrf_exempt
def response(request):
	return JsonResponse({
		'type' : 'text'
#		'buttons' : [USAGE_STRING]
	})
	
