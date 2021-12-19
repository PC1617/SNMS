import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

############graph#############3
# import matplotlib.pyplot as plt, mpld3


##############################Flask#########

from flask import render_template
from flask import Flask, render_template, send_file, make_response, url_for, Response, redirect, request 

#############################################

token = "OaUUKLPah7ISItDYY78HGIIImMe9-NPyX6AYS7yctOTEadbS3VCPAZuggwPsgjDSk9JWDmht2kjzhPaMh4ZIxA=="
org = "SSIPMT"
bucket = "Pro-tik"
client = InfluxDBClient(url="http://localhost:8086", token=token , org=org)

query = '''from(bucket: "Pro-tik")
|> range(start:-48h)\
|> filter(fn: (r) => r["_measurement"] == "my_data")\
|> filter(fn: (r) => r["DB"] == "db2")\
|> filter(fn: (r) => r["_field"] == "VolumeNorm")\
|> aggregateWindow(every: 1s, fn: mean, createEmpty: false)\
|> yield(name: "mean")'''

query_api = client.query_api()

#initialise app
app = Flask(__name__)
@app.route("/")
def index():
    while True:
        flag=0
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
           for record in table.records:
               results.append((record.get_time(), record.get_field(), record.get_value()))

        return render_template("index.html",to_send=results)
if __name__ == '__main__':
    app.run(debug = True)