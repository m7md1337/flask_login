# flask_login_sms_code
* rest API using flask with flask-limit to prevent rate limit and jwt for the auth expire within 20 minute 
* using mysql to store the data with prepared statement query to prevent sqli 
* This repositary is for a learning purpose.
* to use it start with install the requirements.txt 
* make sure the mysql is running before starting ``` service mysql start ``` for linux required root user 
* then configure the database by mysql ``` mysql -u <user> -p < database.sql ``` add the connection details to config.py
* make sure the mysql is running before the start 
* in same dir run python app.py

```
POST /users/login HTTP/1.1
Host: localhost:5000
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Content-Type: application/json
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ru;q=0.8
Connection: close
Content-Length: 45

{"email":"aa@test.com","password":"123456"}
```

* other routes found it in app.py


```
POST /users/sendsms HTTP/1.1
Host: localhost:5000
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Accept: application/json
Origin: https://geekflare.com
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://geekflare.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ru;q=0.8
Connection: close
Content-Type: application/json
Content-Length: 30

{"phone_number":"505123123"}
```

```
POST /users/loginSMScode HTTP/1.1
Host: localhost:5000
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Content-Type: text/plain
Accept: */*
Origin: https://geekflare.com
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Content-Type: application/json
Referer: https://geekflare.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ru;q=0.8
Connection: close
Content-Type: application/json
Content-Length: 46

{"phone_number":"505123123","code":"665953"}
```


```
GET /users/me  HTTP/1.1
Host: localhost:5000
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
Accept: */*
Origin: https://geekflare.com
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://geekflare.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ru;q=0.8
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJpYXQiOjE2NTI1Mzk0NzEsImV4cCI6MTY1MjU0MDY3MX0.qWQMe6WIU9jYu3PA76UXT8eCOyhRSELFwuRLkuh8m4Y
Connection: close

```
