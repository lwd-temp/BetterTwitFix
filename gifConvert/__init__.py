import base64
import os
import subprocess

def extractStatus(url):
    return ""

def lambda_handler(event, context):
    if ("queryStringParameters" not in event):
        return {
            "statusCode": 400,
            "body": "Invalid request."
        }
    
    url = event["queryStringParameters"].get("url","")

    maxWidth = 400
    maxHeight = 267
    maxWidth=maxWidth*2
    maxHeight=maxHeight*2
    threads=8

    subprocess.call(["sh","./conv.sh", "-u", url, "-w", str(maxWidth), "-h", str(maxHeight), "-t", str(threads), "/tmp/out.gif"])

    with open("/tmp/out.gif", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')

    return {
        'statusCode': 200,
        "headers": 
        {
            "Content-Type": "image/gif"
        },
        'body': encoded_string,
        'isBase64Encoded': True
    }