|    |              Route/URL              |  Parameter    | Number of injection trials  | Number of successful Trials |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/user/login |     email     |             18              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/user/login |    password   |             18              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/user       |     email     |             18              |             0               |
|	 |	 /register                         |               |                             |                             |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/user       |     name      |             18              |             0               |
|	 |	 /register                         |               |                             |                             |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/user       |    password   |             18              |             0               |
|    |  /register                          |               |                             |                             |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/user       |   password2   |             18              |             0               |
|    | /register                           |               |                             |                             |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |    email      |             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |   password    |             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |   username    |             18              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |shippingAddress|             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |   postalCode  |             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |    name       |             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |    desc       |             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|
|Scan| http://192.168.2.40:8081/           |    price      |             17              |             0               |
|----|-------------------------------------|---------------|-----------------------------|-----------------------------|

1. Are all the user input fileds in your application covered in all the test cases above? Any successful exploit?
The test cases covered all the input fields for the frontend pages, there were no successful exploits in any of the trials
this due to the fact that the website uses input validation in order to prevent malicious queries from being injected.

2. We did two rounds of scanning. Why the results are different? What is the purpose of adding in the session id?
The two rounds of testing ensured that the program was not vulnerable to sql injection attacks. The purpose of adding in
session id was to access the fields that could only be accessed after a successful login.

3.  Summarize the injection payload used based on the logs, and breifly discuss the purpose.
Based on the logs, sqlmap used a generic injection payload consisting of multiple injection types including boolean-based and Union-based blind SQLi. Since the website uses sqlalchemy, the frontend
is protected against most injection payloads.
