import boto3
import json
import time, datetime
from jinja2 import Template

client = boto3.client('service-quotas')

response = client.list_services()
services = []

while True:
  print("Gathering AWS Services")
  for service in response['Services']:
    # print("%s - %s"%(service['ServiceName'], service["ServiceCode"]))
    quotaresponse =client.list_service_quotas(ServiceCode=service['ServiceCode'])
    quota_list = []
    while True:
      if len(quotaresponse['Quotas']) == 0:
        break
      for quota in quotaresponse['Quotas']:
        quota_list.append({"QuotaName":quota['QuotaName'], "QuotaCode":quota['QuotaCode']})
        # print("%s: %s"% (quota['QuotaName'], quota['QuotaCode']))
      time.sleep(1)
      if ('NextToken' in quotaresponse):
        quotaresponse = client.list_service_quotas(ServiceCode=service['ServiceCode'],NextToken=quotaresponse['NextToken'])
      else:
        break
    services.append({"ServiceName": service['ServiceName'], "ServiceCode":service["ServiceCode"], "Quotas": quota_list})
  if ('NextToken' in response):
    response = client.list_services(NextToken=response['NextToken'])
  else:
    break

print("Rendering page")
template = Template(open('template.html', 'r').read())
rendered = template.render(services=services, generated=datetime.datetime.now())
with open("index.html", "w") as fh:
    fh.write(rendered)
