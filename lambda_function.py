import json
import boto3

def lambda_handler(event, contex):
    # Retrieve the email and event data from the event object
    email = event['body']['email']
    eventData = event['body']['eventData']
    
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')
    
    # Write the email and event data to the DynamoDB table
    try:
        response = dynamodb.put_item(
            TableName='RegisteredEmails',
            Item={
                'email': {'S': email},
                'eventData': {'S': json.dumps(eventData)}
            }
        )
    except Exception as e:
        # Handle DynamoDB write errors
        return {
            'statusCode': 500,
            'body': json.dumps('Error writing email and event data to DynamoDB: {}'.format(str(e)))
        }
    
    # Subscribe the user's email to an SNS topic
    sns = boto3.client('sns')
    
    # Replace the sns_topic_arn with your SNS topic ARN
    sns_topic_arn = 'arn:aws:sns:us-east-1:748795926248:emailsubtest'
    
    try:
        response = sns.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='email',
            Endpoint=email
        )
        
        # Customize the notification message with the selected event data
        notification_message = f'Thank you for subscribing to Funtube. You have selected the following event:\n\nName: {eventData[0]}\nLocation: {eventData[1]}\nVenue: {eventData[2]}\nDate: {eventData[3]}\nTime: {eventData[4]}\nPrice: {eventData[5]}'
        
        # Send the customized notification to the user
        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=notification_message
        )
        
        # Return a successful response
        return {
            'statusCode': 200,
            'body': json.dumps('Email registered successfully, and user subscribed to notifications with the selected event')
        }
    except Exception as e:
        # Handle any errors that occur during the subscription process
        return {
            'statusCode': 500,
            'body': json.dumps('Error subscribing user to notifications: {}'.format(str(e)))
        }