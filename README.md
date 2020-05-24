# Deploying FastAPI on AWS, Using PostgreSQL RDS

**Synopsis**  
This project details the deployment of a Python FastAPI project, which uses a PostgreSQL database, to AWS. The AWS technologies used in production are:
- RDS (relational database service)
- Lambda
- Cloud Formation
- API Gateway
- S3

**Standing on the backs of giants**  
Major shoutout to [iwpnd](https://iwpnd.pw/). I followed his [tutorial](https://iwpnd.pw/articles/2020-01/deploy-fastapi-to-aws-lambda) to have a successful first basic deployment. He also provided sage advice when I got stuck in a few places. Essentially, I catered his project to my specific needs, and added the ability to connect to a PostgreSQL database. 

**Motivation**  
I participate in a "fitness challenge" where data is collected. The format of this collected data is not ideal, so I aim to clean this data, store it indefinitely on AWS in RDS, and make it available via FastAPI so that others can use the data for data analysis. 

**Files**  
- `crud.py`: specifies crud (create, read, update, delete) actions
- `database.py`: sets up connection with PostgreSQL
- `main.py`: brings all routes together
- `models.py`: sqlalchemy models specified
- `schemas.py`: pydantic models specified, which I believe dictates the output format when API is called
- `routers/`: folder containing subsets of routes
- `requirements.txt`: Requirements to install when project is built using sam
- `template.yml`: Essentially the recipe for deploying the project to AWS

**Setting up RDS Instance**  
Since I already had all of the data locally, I wanted to dump it into a PostgreSQL RDS instance. I had some trouble connecting to my RDS instance from my local VM, so here are the steps to make it work: 

1) In RDS instance settings, make sure `Public Accessibility` is set to `Yes`  
2) `Whitelist IP`
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
                    
               
**Dump and Restore - Local PostgreSQL to RDS PostgreSQL**
1) Dump (done from terminal line): `$ pg_dump -Fc mydb > db.dump`
2) Connect to RDS as shown above
3) Restore with: `pg_restore -v -h [endpoint of RDS instance] -U [master username] -d [new database name] [database].dump`


**Things that stumped me**  
- Accessing PostgreSQL RDS instance locally: Make sure `Public Accessibility` is set to `Yes`, otherwise you will get a timeout error. 

- `psycopg2-binary` instead of `psycopg2`: For some reason, AWS lambda doesn't play well with `psycopg2`, even though it works locally  

- Lambda VPC: When this project is deployed as-is, VPC connection is set to none. I needed to change this to `Custom VPC`, and add my default VPC and security group here. 

- `openapi_prefix="/prod"`: This value needs to match `StageName: prod` in `template.yml`. The sample project I pulled from had `Prod` with a capital P, which would not load the /docs and /redoc properly when deployed. 


**Next Steps**  
I'm currently using Lambda environment variables to set the database credentials (including password), so I need to figure out a more secure solution. Someone recommended to use KMS for this. 


**Random Notes**  
I originally added `AWSLambdaVPCAccessExecutionRole` policy to the `fastapilambdarole`, but I tested without it and it doesn't appear necessary. 
