#-*- coding: utf-8 -*-
import time
from message.mybot import mybot_default as default
from message.mybot import mybot_response

from message.models import Reservation as reserv
from message.models import History as history
from message.models import Room as rooms

# Get Success String
def get_reserv_success(room_name, start_time, end_time):
	return room_name+" 예약이 완료 되었습니다.\n시간은 "+start_time+"부터 "+end_time+"까지입니다.\n은혜로운 시간 되세요."

# Reservation Operation
def reserv_operation(param_list):
	# 1. Make Time (START, END) String (format : YYYY-MM-DD HH:MM:SS)
	#print("Operation : %s, %s"%(param_list[default.RESERV_TIME], param_list[default.RESERV_TIME]+param_list[default.USE_TIME]))
	start_time_s = time.localtime(param_list[default.RESERV_TIME])
	end_time_s = time.localtime(param_list[default.RESERV_TIME]+param_list[default.USE_TIME])
	start_time_str = time.strftime("%Y-%m-%d %H:%M:00", start_time_s)
	end_time_str = time.strftime("%Y-%m-%d %H:%M:00", end_time_s)
	reqtime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	# for DEBUG
	#print (start_time_s, end_time_s)
	#print ("%s, %s, %s"%(start_time_str, end_time_str, reqtime_str))

	# 2. Reservation Exist Check
	room_name = param_list[default.ROOM_NAME]

	# Get Room ID
	row = rooms.objects.filter(name = room_name)
	if not row.exists():
		#return mybot_response.get_resbody("존재하지 않는 방입니다.")
		return "존재하지 않는 방입니다."

	room_id = row[0].id
	room_obj = row[0]

	# 2.1 End Time Exist Between Reserv Time & End Time
	count = reserv.objects.filter(room = room_id, reserv_time__lte = end_time_str, end_time__gte = end_time_str).count()
	#print (count)
	if count > 0:
		#return mybot_response.get_resbody("이미 예약하신 분이 계시네요, 다른 시간을 이용해 보세요.")
		return "이미 예약하신 분이 계시네요, 다른 시간을 이용해 보세요."

	# 2.2 Start Time Exist Between Reserv Time & End Time
	count = reserv.objects.filter(room = room_id, reserv_time__lte = start_time_str, end_time__gte = start_time_str).count()
	if count > 0:
		#return mybot_response.get_resbody("이미 예약하신 분이 계시네요, 다른 시간을 이용해 보세요.")
		return "이미 예약하신 분이 계시네요, 다른 시간을 이용해 보세요."

	# 3. Set Reservation
	if param_list[default.RESERVED] != "":
		new_reserv = reserv(room = room_obj, reserv_time = start_time_str, request_time = reqtime_str, end_time = end_time_str, reserved_field = param_list[defult.RESERVED])
	else :
		new_reserv = reserv(room = room_obj, reserv_time = start_time_str, request_time = reqtime_str, end_time = end_time_str)
	
	new_reserv.save()

	# 4. Send Response
	return get_reserv_success(room_name, start_time_str, end_time_str)
	#return mybot_response.get_resbody(get_reserv_success(room_name, start_time_str, end_time_str))

# Cancel Operation
def cancel_operation(param_list):
	# 1. Make Time String (format : YYYY-MM-DD HH:MM:SS)
	room_name = param_list[default.ROOM_NAME]
	reserved_time = time.strftime("%Y-%m-%d %H:%M:00", time.localtime(param_list[default.RESERV_TIME]))

	# 2. Get Room ID
	row = rooms.objects.filter(name = room_name)
	if not row.exists():
		#return mybot_response.get_resbody("존재하지 않는 방입니다.")
		return "존재하지 않는 방입니다."

	room_id = row[0].id
	room_obj = row[0]

	#print("%s : %s" %(room_obj.name, reserved_time))
	
	# 3. Reservation Delete
	del_reserv = reserv.objects.filter(room=room_id, reserv_time=reserved_time)
	if not del_reserv.exists():
		return "요청하신 예약정보가 없습니다."
		#return mybot_response.get_resbody("요청하신 예약정보가 없습니다.")
	
	del_reserv.delete()
	resp_body = room_name + " "+reserved_time+" "+"예약이 취소 되었습니다."
	
	return resp_body

# Search Operation
def search_operation(param_list):
	# 1. Get Reservation List By Room Name
	room_name = param_list[default.ROOM_NAME]
	curtime = time.strftime('%Y-%m-%d %H:%M:00', time.localtime())  

	print (room_name)

	if room_name == 'all':
		rows = reserv.objects.all().filter(end_time__gte = curtime).order_by('room', 'reserv_time')
	else:
		row = rooms.objects.filter(name = room_name)
		if not row.exists():
			return mybot_response.get_resbody("존재하지 않는 방입니다.")
		room_id = row[0].id
		room_obj = row[0]
		
		rows = reserv.objects.filter(room = room_id, end_time__gte = curtime).order_by('reserv_time')

	resbody = " %-12s %10s %10s\n"%("장소", "예약시간", "만료시간")
	resbody = resbody+"----------------------------------------------\n"
	
	for row in rows:
		temp = " %-12s %10s %10s\n"%(row.room.name, str(row.reserv_time)[11:], str(row.end_time)[11:])
		resbody = resbody + temp

	return resbody

# Usage Operation
def usage_operation():
	room_list = ''

	# Get All Room List
	rows = rooms.objects.all()
	for row in rows:
		if len(room_list) != 0:
			room_list = room_list + ', '
		room_list = room_list + row.name
	resp_body=default.DEFAULT_USAGE%(room_list)

	return resp_body

# Command Operation
def operation(param_list):
	resp_body = None
	print (param_list[default.COMMAND])
	if param_list[default.COMMAND] == default.COMMAND_LIST[0] : # Reservation
		resp_body =reserv_operation(param_list)

	elif param_list[default.COMMAND] == default.COMMAND_LIST[1] : # Cancel
		resp_body = cancel_operation(param_list)

	elif param_list[default.COMMAND] == default.COMMAND_LIST[2] : # Search
		resp_body = search_operation(param_list)

	elif param_list[default.COMMAND] == default.COMMAND_LIST[3] : # Usage
		resp_body = usage_operation()

	else: # Invalid
		return None
	
	# Make Response Fail
	if resp_body == None:
		return None

	print (resp_body)

	return mybot_response.get_resbody(resp_body)
	
# Set History
def setHistory():
	# 1. Get Current Time 
	#curtime = time.strftime('%Y-%m-%d %H:00:00', time.localtime()) # For DEBUG
	curtime = time.strftime('%Y-%m-%d %00:00:00', time.localtime())

	# 2. Get All Reservations
	rows = reserv.objects.all().filter(reserv_time__lt = curtime)

	# 3. Set All Reservations To History
	for row in rows:
		entry = history(room = row.room, request_time = row.request_time, reserv_time = row.reserv_time, end_time = row.end_time, reserved_field = row.reserved_field)
		entry.save()
		row.delete()
	return 0

# Delete History
def deleteHistory():
	# 1. Get Calc Time 
	calc_time = time.time()-(default.DAY_SECOND*default.EXPIRE_MIN) # 3 Days Histories
	curtime = time.strftime('%Y-%m-%d 00:00:00', time.localtime(calc_time))
	
	print ("History Delete Base Time : "+curtime)

	# 2. Get All Historeis
	rows = history.objects.all().filter(reserv_time__lt = curtime)

	# 3. Delete 
	rows.delete()

	return 0
