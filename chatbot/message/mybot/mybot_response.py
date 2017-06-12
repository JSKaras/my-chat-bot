#-*- coding: utf-8 -*-

def get_resbody(comment):
	res_body={}
	text_dict={}
	text_dict['text']=comment
	res_body['message'] = text_dict

	return res_body
