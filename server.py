from bottle import route, request, run, post, response
import musicalStatistics 
import json

@route('/ajax')
def handleAjax():
    response.content_type = "application/json"
    response_dict = dict()
    response_dict['ip_counts'] = musicalStatistics.count_field_per_duration("packets", "source_ip", 5)
    return json.dumps(response_dict)


run(host='localhost',port='9011')
