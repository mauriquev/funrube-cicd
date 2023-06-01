import json
import boto3
def lambda_handler(event, context):
    #showID = next(iter(event.keys()))
    # Retrieve the email data from the event object
    #email = event[showID]['email']
    # Create a DynamoDB client
    
    dynamodb = boto3.client('dynamodb')
 
    # Write the email to the DynamoDB table
    response = dynamodb.put_item(
        TableName='funtubeDB2',
        Item={
        'id': {'S': event['id']},
        'email': {'S': event['payload']['email']},
        'name': {'S': event['payload']['eventData']['name']},
        'location': {'S': event['payload']['eventData']['location']},
        'date': {'S': event['payload']['eventData']['date']},
        'time': {'S': event['payload']['eventData']['time']},
        'min': {'S': event['payload']['eventData']['min']},
        'max': {'S': event['payload']['eventData']['max']}
                }
            )
    # Subscribe the user's email to an SNS topic
    sns = boto3.client('sns')
    # Replace the sns_topic_arn with your SNS topic ARN
    sns_topic_arn = 'arn:aws:sns:us-east-1:035082996281:email'
    try:
        response = sns.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='email',
            Endpoint=event['payload']['email']
        )
        # Customize the notification message here
        notification_message = 'Thank you for subscribing to Funtube, we  keep you updated on you selected events price.'
        # Send the customized notification to the user
        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=notification_message
        )

        # Return a response
        return {
            'statusCode': 200,
            'body': json.dumps('Email registered successfully and user subscribed to notifications')
        }
    except Exception as e:
        # Handle any errors that occur during the subscription process
        return {
            'statusCode': 500,
            'body': json.dumps('Error subscribing user to notifications: {}'.format(str(e)))
        }
