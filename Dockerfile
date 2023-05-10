FROM public.ecr.aws/lambda/python:3.8

WORKDIR /lambda
COPY . /lambda

RUN pip install --no-cache-dir -r requirements.txt
CMD ["main.lambda_handler"]