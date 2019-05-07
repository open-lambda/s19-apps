# speech_to_text_aws_lambda

You'll need to create a "stt_packages" folder which contains the packages needed for linux (not mac). Can download .whl file directly from pip page and unzip in that folder.

Use update.sh to uplaod the code to your aws account (assuming you have aws credentials set up)

This used to use mozilla deepspeech but now it just forwards things on to Google Speech.

was useful:
https://medium.com/@dwdraju/python-function-on-aws-lambda-with-api-gateway-endpoint-288eae7617cb
https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py
https://progur.com/2018/02/how-to-use-mozilla-deepspeech-tutorial.html
