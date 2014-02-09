from bottle import route, request, run, post, response, static_file
import musicalStatistics 
import json

@route('/ajax')
def handleAjax():
    response.content_type = "application/json"
    response.status = 200
    response_dict = dict()
    response_dict['ip_counts'] = musicalStatistics.count_field_per_duration("packets", "source_ip", 60)[1:6]
    response_dict['packets_per_duration'] = musicalStatistics.get_packets_per_duration("packets", 10)
    return json.dumps(response_dict) 

@route('/html/<file_name>')
def return_file(file_name):
    return static_file(file_name, root='./html')

@route('/html/images/<img>')
def return_image(img):
    return static_file(img, root='./html/images')

def start():
    run(host='localhost', port=9011)
