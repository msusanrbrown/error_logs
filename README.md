
I created the logger folder on VS Code, locally on my Mac, because I thoought of making some changes and deploying it to AWS, but I ended up editing the files using the AWS lambda editor.

The file that I created in the AWS editor is located in lambda_function.py.

I used the two files contained in the seeds folder to create the two S3 buckets.

The file policies.json contains information necessary for the lambda functions.

To run the tests:

1. Open a terminal and create an environment by typing:

pipenv shell

2. Then type:

python3 -m pytest