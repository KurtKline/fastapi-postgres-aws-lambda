# fastapi_aws

**Files**  
- `crud.py`: specifies crud (create, read, update, delete) actions
- `database.py`: sets up connection with PostgreSQL
- `main.py`: brings all routes together
- `models.py`: sqlalchemy models specified
- `schemas.py`: pydantic models specified, which I believe dictates the output format when API is called
- `routers/`: folder containing subsets of routes

**Setting up RDS Instance**  
Since I already had all of the data locally, I wanted to dump it into a PostgreSQL RDS instance. I had some trouble connecting to my RDS instance from my local VM, so here are the steps to make it work: 

`Public Accessibility`: set to `Yes`  
`Whitelist IP`
- Create new EC2 security group
- Inbound Rules: `Type`: `All Traffic`, `Source`: `My IP`
- Add this security group to RDS instance

Access like this:  
```
psql \
   --host=<DB instance endpoint> \
   --port=<port> \
   --username=<master user name> \
   --password \
   --dbname=<database name> 
```
                    
