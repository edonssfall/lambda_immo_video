## Quick Start
1. Clone it
```sh
git clone https://github.com/edonssfall/Lambda_immo_video.git
```

2. Make .env and fill, as in example
```python
WORK_DIRECTORY="/global/path/to/this/project/"
CLIENT_SECRETS_FILE="/global/path/to/google/secreata/file.json"
AWS_ACCESS_KEY="YourKey_AWS_access"
AWS_SECRET_ACCESS_KEY="AWS_SecreteKeyAccess"
REGION_NAME="aws-regeon-0-eu"
```

3. Create and choose virtual environment and install requirements
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create s3 bucket on aws
```sh
aws s3api create-bucket --bucket your-bucket-name --region your-region-name --create-bucket-configuration LocationConstraint=your-region-name
```

5. Package code
```sh
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket your-bucket-name
```

6. Deploy lambda
```sh
sam deploy --template-file packaged.yaml --stack-name lambda-function-name
```
