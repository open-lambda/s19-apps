# rm function.zip
# cd stt_packages
# zip -r9 ../function.zip .
# cd ..

zip -g function.zip lambda_function.py
aws lambda update-function-code --function-name speechToText --zip-file fileb://function.zip
