from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import dotenv_values

env = dotenv_values(".env")


class InfluxDB:
    localhost = env.get('INFLUXDB_HOSTNAME')
    port = env.get('INFLUXDB_PORT')
    token = env.get('INFLUXDB_TOKEN')
    bucket = env.get('INFLUXDB_BUCKET')
    org = env.get('INFLUXDB_ORG')

    def connect(self):
        client = InfluxDBClient(url=f"http://{self.localhost}:{self.port}", token=self.token, org=self.org)
        return client
    
    def write_json_data(self, json_data):
        write_api = self.connect().write_api(write_options=SYNCHRONOUS)
        write_api.write(org=self.org, bucket=self.bucket, record=json_data, write_precision=WritePrecision.NS)
        self.connect().close()
        return write_api


if __name__ == '__main__':
    pass