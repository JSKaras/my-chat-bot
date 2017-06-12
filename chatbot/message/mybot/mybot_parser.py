#-*- coding: utf-8 -*-
import json
import time, datetime

from message.mybot import mybot_default as default


# Command Valid Check
def command_valid(command):
	if command in default.COMMAND_LIST:
		return command
	return None

# Room Name Valid Check
def room_check(room_name):
	if room_name in default.ROOM_LIST:
		return room_name
	return None

# convert time format
def parse_time(time_str):
	#time_info = time_str.split(':')
	hour = 0 
	mins = 0
	
	if time_str == '지금' or time_str.upper() == 'NOW':
		return time.time() # return second unit

	if '오전' in time_str:
		time_str = time_str.replace('오전', 'am')
	elif '오후' in time_str:
		time_str = time_str.replace('오후', 'pm')
	if '시' in time_str:
		time_str = time_str.replace('시', ':')
	if '분' in time_str:
		time_str = time_str.replace('분', '')
	if '반' in time_str:
		time_str = time_str.replace('반', '30')

	time_s = time.localtime()
	time_info = time_str.split(':')
	if len(time_info) == 2:
		if 'am' in time_info[0]:
			hour=int(time_info[0][2:])
		elif 'pm' in time_info[0]:
			hour=12+int(time_info[0][2:])
		else :
			hour = int(time_info[0])
		if hour < 0 or hour > 23:
			return None

		if time_info[1] == '':
			mins = 0
		else:
			mins = int(time_info[1])
		if mins < 0 or mins > 59:
			return None

		#time_s.tm_hour = hour
		#time_s.tm_min = mins
		time_str=time.strftime("%Y-%m-%d", time_s)
		time_str="%s %d:%02d:00"%(time_str,hour,mins) 
		time_s=time.strptime(time_str, "%Y-%m-%d %H:%M:%S")

		# DEBUG
		#print ("%s, %d, %d"%(time_str, hour, mins))
		#print (time_s)
		#print (time.mktime(time_s))

		return time.mktime(time_s) # return second unit
	
	return None

# Get Use Time 
def parse_use_time(time_str):
	mins = 0
	hour = 0

	if '시간' in time_str:
		time_str = time_str.replace('시간', ':')
	if '분' in time_str:
		time_str = time_str.replace('분', '')
	if '반' in time_str:
		time_str = time_str.replace('반', '30')
	
	time_info = time_str.split(':')
	if len(time_info) == 2:
		hour = int(time_info[0])
		mins = int(time_info[1])
		if mins > 59:
			return None
	elif len(time_info) == 1:
		mins = int(time_info[0])
	else:
		return None

	if mins <= 0 and hour <= 0:
		return None

	return hour*3600+mins*60 # return Second unit

# Content Parser 
def parser(data):
	ret_param = {}

	# 0. None Exception
	if data == None:
		return None

	print (data)

	# 1. Split Command 
	param_list = data.split()

	# 2. Check Valid Command
	if command_valid(param_list[0]) == None:
		return None

	# Parsing Reservation
	# 예약
	reserved_val = None
	if param_list[0] == default.COMMAND_LIST[0] :
		#room_name_val = room_check(param_list[1]) # Room Name Validation
		room_name_val = param_list[1]
		reserv_time_val = parse_time(param_list[2]) # 예약 시간
		use_time_val = parse_use_time(param_list[3]) # 사용 시간
		if len(param_list) == 5:
			reserved_val = param_list[4] # Reserved Param

		# Value Check 
		if room_name_val == None or reserv_time_val == None or use_time_val == None :
			return None

		# Set Param Information
		ret_param[default.COMMAND] = default.COMMAND_LIST[0] 
		ret_param[default.ROOM_NAME] = room_name_val
		ret_param[default.RESERV_TIME] = reserv_time_val
		ret_param[default.USE_TIME] = use_time_val
		if reserved_val != None:
			ret_param[default.RESERVED] = reserved_val
		else :
			ret_param[default.RESERVED] = ''

		return ret_param

	# 예약 취소
	elif param_list[0] == default.COMMAND_LIST[1]:
		#room_name_val = room_check(param_list[1]) # Room Name Validation
		room_name_val = param_list[1]
		reserv_time_val = parse_time(param_list[2]) # 예약 시간
		
		# Value Check 
		if room_name_val == None or reserv_time_val == None:
			return None

		# Set Param Information
		ret_param[default.COMMAND] = default.COMMAND_LIST[1]
		ret_param[default.ROOM_NAME] = room_name_val
		ret_param[default.RESERV_TIME] = reserv_time_val
		
		return ret_param

	# 예약 조회
	elif param_list[0] == default.COMMAND_LIST[2]:
		room_name_val = None

		if len(param_list) == 2:
			#room_name_val = room_check(param_list[1]) # Room Name Validation
			room_name_val = param_list[1]
			
			if room_name_val == None:
				return None

		ret_param[default.COMMAND] = default.COMMAND_LIST[2]
		if room_name_val == None:
			ret_param[default.ROOM_NAME] = 'all'
		else:
			ret_param[default.ROOM_NAME] = room_name_val
		
		return ret_param

	# 사용 방법
	elif param_list[0] == default.COMMAND_LIST[3]:
		ret_param[default.COMMAND] = default.COMMAND_LIST[3]

		return ret_param

	# Exception
	return None
