# API Security Testing Guide

This guide outlines the testing methods for detecting OWASP API vulnerabilities, focusing on where automated tools can help and when manual testing is necessary. Where applicable, specific tools and usage examples are provided.

## 1. Broken Object Level Authorization (BOLA)

- **Automated Detection**: **Low probability** of detection via automated tools.
  - Tools: Difficult to automate due to the need to identify different object IDs across endpoints.

- **Manual Testing**:
  - **Steps**:
    1. Attempt read, update, and delete actions on objects you should not have access to.
    2. Replace objectIDs (e.g., `userID`, `productID`) with IDs from other users.
    3. Swap your authentication token with another user’s token and test access to objects.
  
  - **Example Code**:
    ```bash
    # Attempt to access another user's object by modifying the object ID
    curl -X GET http://api.example.com/objects/456 -H "Authorization: Bearer <YourToken>"
    ```

  - **Things to Try**:
    - **Tool**: Postman
      - Use Postman to modify object IDs and send API requests. Switch tokens and object IDs to check for unauthorized access.
      - How to use: In Postman, set the Authorization header and modify the URL object IDs in the request path.
    - Replace your JWT or API token with another user’s token and try to view or modify resources.

## 2. Broken User Authentication (BUA)

- **Automated Detection**: **High probability** of detection using automated tools.
  - Tools: Burp Suite, OWASP ZAP, custom scripts for brute-force detection.

- **Manual Testing**:
  - **Steps**:
    1. Test for weak passwords or missing CAPTCHA during login.
    2. Check if tokens (e.g., JWT) are validated properly, including signature and expiration.
    3. Try sending credentials via GET requests and check for leakage in URLs.
  
  - **Example Code**:
    ```bash
    # Test for weak passwords (use with caution)
    curl -X POST http://api.example.com/login -d "username=admin&password=12345"
    
    # Check if token expiration is validated
    curl -X GET http://api.example.com/resource -H "Authorization: Bearer <ExpiredJWT>"
    ```

  - **Things to Try**:
    - **Tool**: Hydra
      - Use Hydra for brute-force attacks on authentication endpoints.
      - How to use: `hydra -l admin -P /path/to/wordlist.txt api.example.com http-post-form "/login:username=^USER^&password=^PASS^"`
    - Attempt credential stuffing or brute-force attacks using different username/password combinations.

## 3. Excessive Data Exposure

- **Automated Detection**: **Medium probability** of detection by automated tools.
  - Tools: OWASP ZAP or Burp Suite can help analyze API responses.

- **Manual Testing**:
  - **Steps**:
    1. Review API responses to ensure only the necessary data is returned.
    2. Check for sensitive metadata that might be unintentionally exposed.
  
  - **Example Code**:
    ```bash
    # Inspect the API response for sensitive or unnecessary data
    curl -X GET http://api.example.com/user/123 -H "Authorization: Bearer <YourToken>"
    ```

  - **Things to Try**:
    - **Tool**: Burp Suite
      - Use Burp Suite to intercept API responses and manually review the data for sensitive information.
      - How to use: Enable the Burp proxy, browse the API, and inspect intercepted responses for excess data.

## 4. Lack of Resources & Rate Limiting

- **Automated Detection**: **High probability** of detection via automated tools.
  - Tools: JMeter, Burp Suite, or custom scripts to flood the API with requests.

- **Manual Testing**:
  - **Steps**:
    1. Test rate limits by sending a large number of requests in a short time frame.
    2. Attempt to upload files larger than the expected limit or request large datasets.
  
  - **Example Code**:
    ```bash
    # Simulate sending a large number of requests in quick succession
    for i in {1..1000}; do curl -X GET http://api.example.com/resource; done

    # Send a file larger than the expected limit
    curl -X POST http://api.example.com/upload -F "file=@largefile.txt"
    ```

  - **Things to Try**:
    - **Tool**: JMeter
      - Use JMeter to create load tests that simulate high traffic and stress-test the API.
      - How to use: Set up a HTTP Request sampler in JMeter and configure multiple threads to simulate high request volumes.
    - Test if large file uploads are properly restricted by sending oversized files.

## 5. Broken Function Level Authorization

- **Automated Detection**: **Low probability** of detection via automated tools.
  - Tools: Manual testing or brute-force URL manipulation is often necessary.

- **Manual Testing**:
  - **Steps**:
    1. Test for unauthorized access to higher-privileged functions by manipulating URLs and HTTP methods.
    2. Perform directory brute-forcing to identify hidden or unprotected endpoints.
  
  - **Example Code**:
    ```bash
    # Change the HTTP method from GET to DELETE and test unauthorized access
    curl -X DELETE http://api.example.com/admin/user/123 -H "Authorization: Bearer <UserToken>"

    # Attempt to brute-force hidden paths
    curl -X GET http://api.example.com/admin/
    ```

  - **Things to Try**:
    - **Tool**: Dirbuster
      - Use Dirbuster to brute-force directory paths and uncover hidden endpoints.
      - How to use: Run Dirbuster and point it at the API URL to discover unprotected paths.
    - Manipulate HTTP methods (e.g., using `DELETE` or `PUT` instead of `GET`).

## 6. Mass Assignment

- **Automated Detection**: **Low probability** of detection via automated tools.
  - Tools: Manual testing is typically required to find business logic flaws.

- **Manual Testing**:
  - **Steps**:
    1. Review API responses for fields that should not be modifiable by the user (e.g., product prices, roles).
    2. Test by submitting additional parameters in the request that were not part of the original response.
  
  - **Example Code**:
    ```json
    # Modify this request to include unauthorized fields
    {
      "name": "Item",
      "price": "100",
      "admin": true
    }
    ```

  - **Things to Try**:
    - **Tool**: Burp Suite (Repeater)
      - Use Burp Repeater to modify API requests and add fields that shouldn’t be modifiable by the client.
      - How to use: Send a request to Burp Repeater, modify the parameters, and resend the request to check the server response.

## 7. Security Misconfiguration

- **Automated Detection**: **High probability** of detection via automated tools.
  - Tools: OWASP ZAP, Burp Suite, or other security scanners can detect misconfigurations.

- **Manual Testing**:
  - **Steps**:
    1. Scan for open ports, improper CORS settings, or missing security headers (CSP, HSTS).
    2. Test file upload endpoints to see if anonymous users can upload malicious files.
  
  - **Example Code**:
    ```bash
    # Test for open ports and misconfigurations
    nmap -p 1-65535 api.example.com

    # Test CORS policies
    curl -X OPTIONS http://api.example.com/resource -H "Origin: http://evil.com"
    ```

  - **Things to Try**:
    - **Tool**: OWASP ZAP
      - Use OWASP ZAP to scan for security misconfigurations like missing headers, weak CORS policies, and more.
      - How to use: Run an automated scan in OWASP ZAP and review the security report for misconfigurations.

## 8. Injection

- **Automated Detection**: **High probability** of detection via automated tools.
  - Tools: Burp Suite, OWASP ZAP, SQLmap can automate the detection of injection vulnerabilities.

- **Manual Testing**:
  - **Steps**:
    1. Test input fields for SQL, XML, or OS injections by submitting crafted payloads.
    2. Check if the API improperly processes user inputs, especially in file uploads or search queries.
  
  - **Example Code**:
    ```bash
    # Test for SQL Injection
    curl -X POST http://api.example.com/search -d "query=1' OR '1'='1"
    
    # Test for OS Injection
    curl -X GET http://api.example.com/execute?cmd=ping%20127.0.0.1
    ```

  - **Things to Try**:
    - **Tool**: SQLmap
      - Use SQLmap to automatically detect SQL injection vulnerabilities in API parameters.
      - How to use: `sqlmap -u "http://api.example.com/search?query=test" --dbs`
    - **Tool**: Burp Suite (Intruder)
      - Use Burp Intruder to test for OS injections by sending payloads to command-executing endpoints.

## 9. Improper Assets Management

- **Automated Detection**: **Medium probability** of detection via automated tools.
  - Tools: Burp Suite and manual brute-forcing techniques.

- **Manual Testing**:
  - **Steps**:
    1. Check if older versions of the API are still accessible by changing the version number in the URL.
    2. Perform brute-force attacks to discover deprecated endpoints or hidden admin URLs.
  
  - **Example Code**:
    ```bash
    # Test if old API versions are accessible
    curl -X GET http://api.example.com/v1/resource
    
    # Try to access the admin interface
    curl -X GET http://api.example.com/v1/admin
    ```

  - **Things to Try**:
    - **Tool**: Burp Suite
      - Use Burp Suite to brute-force different API versions or hidden paths by modifying the request URLs.
      - How to use: Send requests to Burp Repeater and try different URL versions (`/v1/`, `/v2/`).

## 10. Insufficient Logging & Monitoring

- **Automated Detection**: **Low probability** of detection via automated tools.
  - Tools: Manual review is usually required to check logging mechanisms.

- **Manual Testing**:
  - **Steps**:
    1. Test for log injection attacks (e.g., inserting a malicious character like a comma to cause issues in CSV logs).
    2. Ensure all critical actions (login attempts, access to sensitive data, etc.) are logged with proper details (e.g., IP address, timestamp).
  
  - **Example Code**:
    ```bash
    # Insert malicious input to test logging system
    curl -X POST http://api.example.com/log -d "name=John,Smith"
    ```

  - **Things to Try**:
    - **Tool**: Manual Review
      - Manually inspect logs and ensure sensitive data (PII) is not being logged, and critical actions are properly recorded.
      - How to use: Review logs for log injection attacks and check for anomalies in logging behavior.
