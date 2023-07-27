import time
import boto3

def update_dns_records(hosted_zone_id, changes):
    # Replace 'your_access_key' and 'your_secret_key' with your AWS credentials.
    route53_client = boto3.client('route53', aws_access_key_id='AKIAUTMPNZQXMPQNIF5X', aws_secret_access_key='rqV1MZ9XYqHPKYNxMX1RHHcSXSRigQdejN7I64Rx')

    response = route53_client.change_resource_record_sets( 
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': changes
        }
    )

    return response


def wait_for_change_status(client, change_id):
    while True:
        response = client.get_change(Id=change_id)
        status = response['ChangeInfo']['Status']

        if status == 'SUCCESSFUL':
            print("The status is successful. The changes have been applied.")
            break
        elif status == 'PENDING':
            print("The status is pending. Waiting for the changes to take effect...")
        else:
            print(f"The status is {status}. The changes might have encountered an error.")
            break

        time.sleep(10)  # Wait for 10 seconds before checking again

# Replace 'your_access_key' and 'your_secret_key' with your AWS credentials.
route53_client = boto3.client('route53', aws_access_key_id='AKIAUTMPNZQXMPQNIF5X', aws_secret_access_key='rqV1MZ9XYqHPKYNxMX1RHHcSXSRigQdejN7I64Rx')

# Example usage:
if __name__ == "__main__":
    # Replace 'your_hosted_zone_id' with the actual hosted zone ID.
    hosted_zone_id = 'Z08244843TCCLOU8V7RFO'
    changes = [
        # Add the changes you want to make here
		  {
              'Action': 'UPSERT',
              'ResourceRecordSet': {
                  'Name': 'test.nagendrareddy.live',  # Replace with the DNS record name you want to update
                  'Type': 'A',            # Replace with the record type (e.g., A, CNAME, etc.)
                  'TTL': 300,             # Replace with the Time-to-Live value
                  'ResourceRecords': [
                      {
                          'Value': '18.191.59.14'  # Replace with the updated record value
                      },
                  ]
              }
          },
        #   {
        #       'Action': 'UPSERT',
        #       'ResourceRecordSet': {
        #           'Name': 'example.nagendrareddy.live',  # Replace with the DNS record name you want to update
        #           'Type': 'A',            # Replace with the record type (e.g., A, CNAME, etc.)
        #           'TTL': 100,             # Replace with the Time-to-Live value
        #           'ResourceRecords': [
        #               {
        #                   'Value': '18.191.59.14'  # Replace with the updated record value
        #               },
        #           ]
        #       }
        #   }
          
    ]

    response = update_dns_records(hosted_zone_id, changes)
    print(response)

    change_id = response['ChangeInfo']['Id']
    wait_for_change_status(route53_client, change_id)
    
   
