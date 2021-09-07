# -*- coding: utf-8 -*-

import os
import re
from os import path
import json
import time
import logging
import tornado.web
import tornado.httpclient
import datetime as dt

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor  
from tornado.escape import json_encode
from datetime import datetime, timedelta

from app.webapp.BaseHandler import *
from app.webapp import route

from app.config.settings import _config

@route('/metrics', name = 'Show metric UPS prometheus style')
class Alerts(BaseHandler):
    executor = ThreadPoolExecutor(max_workers = 4)

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        data = yield self.backgroud_task()
        self.set_header('Content-Type','text/plain; version=0.0.4; charset=utf-8')
        for line in data:
            self.write('{}\n'.format(line))
        self.finish()

    @run_on_executor
    def backgroud_task(self):
        data = []
        request = tornado.httpclient.HTTPRequest(
            url="{}/listJson".format(_config.ipponURL),
            method="GET",
            validate_cert=False
        )        
        try:
            response = tornado.httpclient.HTTPClient().fetch(request)
            for ups in json.loads(response.body):
                request = tornado.httpclient.HTTPRequest(
                    url="{}/{}/json".format(_config.ipponURL, ups['id']),
                    method="GET",
                    validate_cert=False
                )
                resp = tornado.httpclient.HTTPClient().fetch(request)
                data_ups = json.loads(resp.body)
                data.append('ups_input_voltage{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['inVolt'])))
                data.append('ups_input_frequency{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['inFreq'])))
                data.append('ups_output_voltage{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['outVolt'])))
                data.append('ups_output_frequency{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['outFreq'])))
                data.append('ups_output_active_power{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['outW'])))
                data.append('ups_output_apparent_power{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['outVA'])))
                data.append('ups_output_load{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['loadPercent'])))
                data.append('ups_battery_voltage{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['batV'])))
                data.append('ups_battery_time_remaining{{name="{0}"}} {1}'.format(ups['key'], get_total_seconds(data_ups['batTimeRemain'])))
                data.append('ups_battery_capacity{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['batCapacity'])))
                data.append('ups_temp{{name="{0}"}} {1}'.format(ups['key'], re.sub(r'[^\d.]','', data_ups['upsTemp'])))
        except Exception as e:
            logging.warn(str(e))
        
        return data


def get_total_seconds(stringHMS):
    if 'h' in stringHMS:
        timedeltaObj = dt.datetime.strptime(stringHMS, "%Hh%Mm%Ss") - dt.datetime(1900,1,1)
        return int(timedeltaObj.total_seconds())
    elif 'm' in stringHMS:
        timedeltaObj = dt.datetime.strptime(stringHMS, "%Mm%Ss") - dt.datetime(1900,1,1)
        return int(timedeltaObj.total_seconds())
    elif 's' in stringHMS:
        timedeltaObj = dt.datetime.strptime(stringHMS, "%Ss") - dt.datetime(1900,1,1)
        return int(timedeltaObj.total_seconds())
    else:
        return 0


def make_app():
    settings = {
    'default_handler_class': ErrorHandler,
    'default_handler_args': dict(status_code=404),
    'debug': True,    
    }
    urls = route.urls
    application = tornado.web.Application(
    urls,
    **settings)    
    return application
