#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

def lambda_handler(event, context):
	url    = "https://euce1-110-nfr.sentinelone.net"
	obj    = {"username": "yuta.kawamura.697@ctc-g.co.jp", "remember_me": "true", "password": "aae$5mn.fr"}
	token = get_token(url, obj)
	if not token:
		fault = 'fault'
		return fault
	else:
		events = get_all_events(url, token, cursor=0)
		unnecessary_events = []
		while events['pagination']['nextCursor']:
			unnecessary_ids = extract_unnecessary_events(events)
			for event_id in unnecessary_ids:
				unnecessary_events.append(event_id)
				events = get_all_events(url, token, events['pagination']['nextCursor'])
		else:
			unnecessary_ids = extract_unnecessary_events(events)
			for event_id in unnecessary_ids:
				unnecessary_events.append(event_id)
	if unnecessary_events:
		return unnecessary_events
		# mark_as_resolved(url, token, unnecessary_events)

# API利用のためのトークンを発行
def get_token(url, obj):
    url    = url + "/web/api/v2.0/users/login"
    method = "POST"
    json_data = json.dumps(obj).encode("utf-8")
    headers   = {"Content-Type" : "application/json"}
    request   = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        token_json    = json.loads(response_body)
        return token_json['data']['token']

# イベント取得関数
def get_all_events(url, token, cursor):
	url = url + '/web/api/v2.0/threats?limit=100&resolved=False&token='
	if cursor:
		response = urllib.request.urlopen(url + token + '&cursor=' + cursor)
	else:
		response = urllib.request.urlopen(url + token)
	html   = response.read()
	data   = html.decode('utf-8')
	events = json.loads(data)
	return events

# Mark as resolved したいイベントを抽出
def extract_unnecessary_events(events):
	unnecessary_events = []
	for item in events['data']:
		for engine in item['engines']:
			# 検出エンジンがレピュテーションか静的ファイル解析の場合
			if (engine == 'reputation' or engine == 'pre_execution'):
				# 対応として隔離処理が行われている場合
				if (item['mitigationReport']['quarantine']['status'] == 'success'):
					unnecessary_events.append(item['id'])
	return unnecessary_events

#  Mark as resolved の実施
def mark_as_resolved(url, token, events):
	url       = url + '/web/api/v2.0/threats/mark-as-resolved?token=' + token
	method    = "POST"
	obj       = {"filter": {"ids" : events}}
	json_data = json.dumps(obj).encode("utf-8")
	headers   = {"Content-Type" : "application/json"}
	request   = urllib.request.Request(url, data=json_data, headers=headers, method=method)
	with urllib.request.urlopen(request) as response:
		response_body = response.read().decode("utf-8")
		token_json    = json.loads(response_body)