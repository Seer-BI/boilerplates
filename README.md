# Usage
Ensure a valid GitHub access token is saved as an environment variable with alias _"GIT_ACCESS_TOKEN"_.
## Important Notice
Before commencing the project, ensure all necessary access credentials are stored securely. The following conventions should be adopted.
### For AWS keys:
<companyName>_AWS_ACCESS (eg SeerBI_AWS_ACCESS)
{"key": "AKIA_XXXXXXXXXX", "secret": "secret", "region": "region", "owner": "owner_number", "arn": "arn"}
and can be called thus:

```
import os, ast
session = boto3.Session(
        aws_access_key_id=ast.literal_eval(os.getenv("SeerBI_AWS_ACCESS"))["key"],
        aws_secret_access_key=ast.literal_eval(os.getenv("SeerBI_AWS_ACCESS"))["secret"],
        region_name=ast.literal_eval(os.getenv("SeerBI_AWS_ACCESS"))["region"]
    )
# Services can be called
textract = session.client('textract')

s3 = session.client('s3', region_name=ast.literal_eval(os.getenv("SeerBI_AWS_ACCESS"))["region"])

```
For microsoft azure or pyodbc related credentials, let them be saved as connection strings thus:
```
Variable name: <CompanyName>_<databaseName>_CONNSTR
Value: DRIVER={ODBC Driver 17 for SQL Server};SERVER=XXX.XX.XX.XXX;DATABASE=databaseName;UID=userID;PWD=password <br>
and they can be called thus:
```

```
    import os
    import pyodbc
    conn = pyodbc.connect(os.environ.get(<CompanyName>_<databaseName>_CONNSTR))
    print("Connected to Microsoft SQL Server")
```

for aws hosted or other databases where you could use psycopg2, please also use a similar convention as above
```
Variable name: <CompanyName>_<databaseName>_CONNSTR <br>
Value: host='databaseHost.xxxxxx.eu-west-x.rds.amazonaws.com' port=xxxx dbname='databaseName' user='databaseUser' password='p@ssword' <br> and can be connected thus:
```
```
    import os
    import psycopg2
    conn = psycopg2.connect(os.environ.get(<CompanyName>_<databaseName>_CONNSTR))
    print("Connected to Server")
```
You might want to do something in the lines of
```
with open psycopg2.connect(os.environ.get(<CompanyName>_<databaseName>_CONNSTR)) as conn:
        cursor = conn.cursor()
        # write query here
        cursor.execute(query)
        conn.commit()
```

using the style above would ensure that db is closed after running those lines. <be>

The kickstart script is to be called thus: <br>

*python -u "path/to/kickstart.py" --job-path "<desired/location/of/the/job>"*




## How to set up if you want it easier, run as cmd as admin:
1. *copy "path\to\kickstart.py" "c:\"* (or wherever safer you want it)
2. *notepad $PROFILE*
3. add this line to the file: *function kickstart {python -u "c:\kickstart.py" --job-path $args[0]}*
4. save and close
5. restart PowerShell
6. run *"kickstart Folder"*
The folder is a folder name or path.

A folder called "Projects" must exist in your home directory. where it does not exist, it will be created.

Note: You may need to enable script execution in PowerShell. You can do this by opening an elevated PowerShell session (Run as Administrator) and running the following command:
*Set-ExecutionPolicy RemoteSigned*
