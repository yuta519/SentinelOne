#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
import settings

def main ():
	url      = settings.url
	username = settings.username
	password = settings.password
	account  = {"username": username, "password": password}

	token = get_token(url, account)
	if not token:
		print('Fault')
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
		sum_of_events = len(unnecessary_events)
		response_code = mark_as_resolved(url, token, unnecessary_events)
		if (response_code == 200):
			print('Automatically resolved ' + str(sum_of_events) + ' events.')
		else:
			print('Failed. Something went wrong. Please contact System Administrator.')


# get token for useing SentinelOne api
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

# get SentinelOne events
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

# extract unnecessary events
def extract_unnecessary_events(events):
	unnecessary_events = []
	for item in events['data']:
		for engine in item['engines']:
			if (engine == 'reputation' or engine == 'pre_execution'):
				if (item['mitigationReport']['quarantine']['status'] == 'success'):
					unnecessary_events.append(item['id'])
					# print(item['fileDisplayName'])
	return unnecessary_events

#  mark as resolved
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
		return response.getcode()


#############################
# execution
#############################
if __name__ == "__main__":
    main()