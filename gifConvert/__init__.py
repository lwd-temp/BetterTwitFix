import base64
import os
import subprocess
import json
import sys
import tempfile

def extractStatus(url):
    return ""

def get_video_frame_rate(filename):
    result = subprocess.run(
        [
            "./ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            "-show_entries",
            "stream=r_frame_rate",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    result_string = result.stdout.decode('utf-8').split()[0].split('/')
    fps = float(result_string[0])/float(result_string[1])
    return fps

def get_video_length_seconds(filename):
    result = subprocess.run(
        [
            "./ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    result_string = result.stdout.decode('utf-8').split()[0]
    return float(result_string)

def loop_video_until_length(filename, length):
    # use stream_loop to loop video until it's at least length seconds long
    video_length = get_video_length_seconds(filename)
    if video_length < length:
        loops = int(length/video_length)
        new_filename = tempfile.mkstemp(suffix=".mp4")[1]
        out = subprocess.call(["./ffmpeg","-stream_loop",str(loops),"-i",filename,"-c","copy",new_filename],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        print("out: " + str(out))
        return new_filename
    else:
        return filename



def lambda_handler(event, context):
    if ("queryStringParameters" not in event):
        return {
            "statusCode": 400,
            "body": "Invalid request."
        }
    
    url = event["queryStringParameters"].get("url","")

    # download video
    videoLocation = tempfile.mkstemp(suffix=".mp4")[1]
    subprocess.call(["wget","-O",videoLocation,url],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

    maxWidth = 400
    maxHeight = 267
    maxWidth=maxWidth*2
    maxHeight=maxHeight*2
    threads=16
    fps=get_video_frame_rate(videoLocation)
    outgif = tempfile.mkstemp(suffix=".gif")[1]
    out = subprocess.call(["timeout","3","sh","./conv.sh", "-u", videoLocation, "-w", str(maxWidth), "-h", str(maxHeight), "-t", str(threads),"-f",str(fps),outgif],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

    if (out != 0):
        if (out==124):
            # plan b: loop video until it's at least 60 seconds long
            videoLocationLooped = loop_video_until_length(videoLocation, 60)
            os.remove(videoLocation)
            videoLocation = videoLocationLooped
            with open(videoLocation, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('ascii')
            os.remove(videoLocation)
            return {
                'statusCode': 200,
                "headers": 
                {
                    "Content-Type": "video/mp4"
                },
                'body': encoded_string,
                'isBase64Encoded': True
            }
        else:
            return {
                "statusCode": 500,
                "body": "Conversion error."
            }

    with open(outgif, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    os.remove(outgif)
    return {
        'statusCode': 200,
        "headers": 
        {
            "Content-Type": "image/gif"
        },
        'body': encoded_string,
        'isBase64Encoded': True
    }