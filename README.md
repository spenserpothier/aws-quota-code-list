# AWS Quota Code List

Simple python/boto script to get the list of quota codes for use in quering service quotas.

Example of using a quota code to find out the current quota for `Number of EIPs - VPC EIPs`

```python
response = client.get_service_quota(
    ServiceCode='ec2',
    QuotaCode='L-0263D0A3'
)

print(response['Quota']['Value'])
```

This runs on a weekly schedule via github actions and published at: [https://spenserpothier.github.io/aws-quota-code-list/](https://spenserpothier.github.io/aws-quota-code-list/)
