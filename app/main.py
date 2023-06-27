from flask import Flask, request

app = Flask(__name__)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

@app.route('/metrics', methods=['POST'])
def processMetric():
    empty_values = 0
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
       try:
           result=request.get_json()
          if "server" not in result:
             app.logger.error("Missing server parameter!")
             empty_values += 1

          if "host" not in result:
             app.logger.error("Missing host parameter!")
             empty_values += 1

          if "key" not in result:
             app.logger.error("Missing key parameter!")
             empty_values += 1

          if "value" not in result:
             app.logger.error("Missing value parameter")
             empty_values += 1
       except:
             app.logger.error("Issue with parameters!")
             return 'Problem with Parameters!'

       if empty_values == 0:
          try:
             packet = [
                ZabbixMetric(str(result['host']), str(result['key']), str(result['value']))
             ]
             getvalues = ZabbixSender(str(result['server'])).send(packet)
             #app.logger.info(getvalues)
             if getvalues.processed == 1:
                app.logger.info("Key Updated: " + str(result['key']) + " processed in: " + str(getvalues.time) + "s")
                return 'Update Successful!'
             else:
                app.logger.error("Upload unsuccesseful!")
                return 'Metric no Uploaded!'
          except:
             app.logger.error("Unable to send data to Zabbix Server")
             return 'Error Sending Data!'
       else:
          app.logger.error("Missing one or more Parameters!")
          return 'Missing Parameters!'

    else:
       app.logger.error("Content-Type not supported!")
       return 'Content-Type not supported!'
