[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Deploying FastAPI on AWS, Using PostgreSQL RDS

## Synopsis
This project details the deployment of a Python FastAPI project, which uses a PostgreSQL RDS database, to AWS. The AWS technologies used in production are:
- RDS
- Lambda
- Cloud Formation
- API Gateway
- S3

## Standing on the backs of giants
Major shoutout to [iwpnd](https://iwpnd.pw/). I followed his [tutorial](https://iwpnd.pw/articles/2020-01/deploy-fastapi-to-aws-lambda) to have a successful first basic deployment. He also provided sage advice when I got stuck in a few places. Essentially, I catered his project to my specific needs, and added the ability to connect to a PostgreSQL database.

## Motivation
I participate in a "fitness challenge" where players log daily points. The format of the collected data is not ideal, so I aim to clean this data, store it indefinitely on AWS in RDS, and make it available via FastAPI so that others can use the data for analysis.

## Files
```
.
├── app
|   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── players.py
│   │   ├── seasons.py
│   │   └── teams.py
│   └── schemas.py
├── .pre-commit.yaml
├── LICENSE
├── README.md
├── requirements.txt
└── template.yml
```

- `crud.py`: specifies crud (create, read, update, delete) actions
- `database.py`: sets up connection with PostgreSQL
- `main.py`: brings all routes together
- `models.py`: sqlalchemy models specified
- `schemas.py`: pydantic models specified, which I believe dictates the output format when API is called
- `routers/`: folder containing subsets of routes
- `.pre-commit.yaml`: config file for pre-commit tool
- `requirements.txt`: requirements to install when project is built using sam
- `template.yml`: essentially the recipe for deploying the project to AWS

## Setup (linux)
### Install and configure AWS CLI and SAM
In order to proceed with set-up and deployment, AWS CLI and SAM need to be installed and configured on your machine. 
- [Install CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [Configure CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Install SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Create AWS Role
1) IAM Console >> Roles >> Create
2) Select `AWS service` as type, and choose `Lambda` and use case
3) Add policies:
   - `AWSLambdaBasicExecutionRole`: Permission to upload logs to CloudWatch
   - `AWSLambdaVPCAccessExecutionRole`: Permission to connect our Lambda function to a VPC
4) Finish creating role, and set name as `fastapilambdarole`. This name matches role specified in `template.yml`. 

### Create S3 Bucket
When we deploy our code with AWS SAM, a zip folder of our code will be uploaded to S3. There are two options for creating an S3 bucket. 

(1) In the [AWS console](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)  
(2) With the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html)
```
aws s3api create-bucket \
--bucket {your bucket name here} \
--region eu-central-1 \
--create-bucket-configuration LocationConstraint=eu-central-1
```

Please note that S3 bucket names need to be globally unique. So the name of the bucket you create here will determine the bucket name used in later steps. Also, ensure that you change the region to your local region. 

### Clone project and test locally
```
git clone https://github.com/KurtKline/fastapi-postgres-aws-lambda.git
cd fastapi-postgres-aws-lambda
# create and activate a virtual environment
pip install -r requirements.txt
pip install uvicorn
```

In order to test locally without errors, PostgreSQL needs to be installed on your local machine, and the sample data needs to be loaded into a database table. 
[Installing PostgreSQL on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)

From the linux terminal: 
```
psql
postgres=# CREATE DATABASE fitness;
postgres=# CREATE TABLE fit (id serial, player varchar(50), team varchar(50), season varchar(50), data_date date, points float);
postgres=# \copy fit(player, team, season, data_date, points) from 'clean_fit.csv' with DELIMITER ',' CSV HEADER;
```

Start FastAPI
```
uvicorn app.main:app --reload
# click the link to open the browser at http://127.0.0.1:8000
```

Once you click the link, add /docs or /redoc to the URL `http://127.0.0.1:8000/docs`. You will then see the Swagger UI.

### Setting up RDS PostgreSQL Instance
In order to deploy to AWS, our code AND our database needs to live on AWS. Here are some basic guidelines to setting up the RDS PostgreSQL instance. 

1) In RDS instance settings, make sure `Public Accessibility` is set to `Yes`
2) Specify `initial database name`, which will be used in pg_restore below
3) Whitelist IP
   - Create new EC2 security group
   - Inbound Rules: `Type`: `All Traffic`, `Source`: `My IP`
   - Add this security group to RDS instance

How to gain access to RDS instance from Linux terminal:
```
psql \
   --host=<DB instance endpoint from AWS> \
   --port=<port> \
   --username=<master user name> \
   --password \
   --dbname=<database name>
```

Once the data is dumped into your RDS PostgreSQL instance, you can set `Public Accessibility` back to `No` if you'd like. This just prevents external sources, like your local PC, from accessing your RDS instance.


### Loading data into RDS PostgreSQL

Here are two options for loading the data into RDS PostgreSQL

#### Dump and Restore: if data already exists in local PostgreSQL
1) Dump (done from terminal line): `$ pg_dump -Fc mydb > db.dump`
2) Restore with: `pg_restore -v -h [RDS endpoint] -U [master username ("postgres" by default)] -d [RDS database name] [dumpfile].dump`
3) Verify load was successful by connecting with psql block shown above

#### From .csv file
First connect to RDS through psql as shown above. Depending on your database name, `fit=>` shown below may be different for you. 
```
fit=> create table fit (id serial, player varchar(50), team varchar(50), season varchar(50), data_date date, points float);
fit=> \copy fit(player, team, season, data_date, points) from 'clean_fit.csv' with DELIMITER ',' CSV HEADER;
COPY 105
```

More options for loading data into PostgreSQL RDS  
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html

### Deploying project with AWS SAM
The `template.yml` file is used for deployment with AWS SAM. 

(1) Replace the values in `template.yml` specified as `{replace}`.  
(2) Uncomment `# openapi_prefix="/prod"` in `app/main.py`. This allows proper access of API when deployed.  
(3) Run following steps for SAM in linux terminal  
```
sam validate
```
```
sam build --debug
```
```
sam package --s3-bucket {your bucket name here} --output-template-file out.yml --region eu-central-1
```
```
sam deploy --template-file out.yml --stack-name example-stack-name --region eu-central-1 --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM
```

## Things that stumped me
- Accessing PostgreSQL RDS instance locally: Make sure `Public Accessibility` is set to `Yes`, otherwise you will get a timeout error.

- `psycopg2-binary` instead of `psycopg2`: For some reason, AWS lambda doesn't play well with `psycopg2`, even though it works locally

- Lambda VPC: When this project is deployed as-is, VPC connection is set to none. I needed to change this to `Custom VPC`, and add my default VPC and security group here. *This has since been added directly into the template.yml file.*

- `openapi_prefix="/prod"`: This value needs to match `StageName: prod` in `template.yml`. The sample project I pulled from had `Prod` with a capital P, which would not load the /docs and /redoc properly when deployed.

- Need to add `AWSLambdaVPCAccessExecutionRole` policy to the `fastapilambdarole`, otherwise will get errors when using the `sam deploy` command.


## Next Steps
- [ ] I'm currently using Lambda environment variables to set the database credentials (including password), so I need to figure out a more secure solution. Someone recommended to use KMS for this.

- [x] Add VPC settings for Lambda to template.yml file if possible, so that no changes need to be made after deployment

- [x] Add data samples which can be used to illustrate full set-up

- [x] Add black formatting and pre-commit
