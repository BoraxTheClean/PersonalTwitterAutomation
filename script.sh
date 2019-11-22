mkdir dist
cp src/* dist/

pip install -r requirements.txt -t dist/
aws cloudformation package --template-file template.yaml --s3-bucket owen-lambda-bucket --s3-prefix personal-twitter-bot --output-template processed.template.yaml
aws cloudformation deploy --template-file processed.template.yaml --stack-name personal-twitter-automation --capabilities CAPABILITY_IAM

rm processed.template.yaml
rm -rf dist/
