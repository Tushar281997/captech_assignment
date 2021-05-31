# captech_assignment

**CREATE USER**
Pyload in create user api:
{
    "email": "tushar.n@gmail.com",
    "first_name": "TusharN",
    "last_name": "Nachan",
    "password": "7768847156",
    "mobile_number": 7768847156
}

**LOGIN API**
payload in Login Api if user requestes otp:
{
"mobile_number":7768847156,
"action":"GENERATE OTP",
"otp":""
}

Payload in Login if user sends verification otp:
{
"mobile_number":7768847156,
"action":"",
"otp":"286777"
}
