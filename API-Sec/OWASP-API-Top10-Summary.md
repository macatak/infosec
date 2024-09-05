# OWASP API Top 10 Summary

## 1. Broken Object Level Authorization (BOLA)

- **Summary**:
  - Occurs when the API does not properly verify user permissions for accessing or modifying objects (e.g., by replacing `userID` or `objectID`).
  - The vulnerability is related to insufficient validation of all object references, not just user or object IDs.
- **Causes**:
  - Lack of validation on object access, particularly around object references (userID, objectID, or other object references).
- **Detection**:
  - Test unauthorized access across all HTTP methods (GET, POST, DELETE, etc.).
  - Replace objectIDs and tokens with those from other users and attempt unauthorized actions.
  - Ensure every object reference and all endpoints are protected.
- **Can Detection Be Automated?**: **Partially**
  - Automated testing can be used to replace objectIDs or userIDs and check for unauthorized access. Tools like Burp Suite or Postman can automate some aspects, but testing every objectID across all endpoints might require manual effort to fully test authorization.

## 2. Broken User Authentication (BUA)

- **Summary**:
  - Allows unauthorized access due to improper authentication mechanisms (e.g., brute force, weak passwords, or improper token handling).
- **Causes**:
  - Invalid implementation of authentication or missing security mechanisms like headers or tokens.
  - Failure to implement account lockouts, strong password policies, or CAPTCHA.
- **Detection**:
  - Test for weak passwords, missing CAPTCHA, improper use or validation of tokens (like JWT), and lack of expiration handling.
  - Ensure JWT tokens are properly validated, including signature, expiration, and algorithm.
- **Can Detection Be Automated?**: **Yes**
  - Brute-force attacks, weak password detection, missing CAPTCHA, and improper token handling can be automated using tools like OWASP ZAP, Burp Suite, or custom scripts.

## 3. Excessive Data Exposure

- **Summary**:
  - APIs return more data than necessary, allowing attackers to extract sensitive information from responses.
- **Causes**:
  - APIs exposing unnecessary data, relying on clients to filter the data, instead of enforcing restrictions on the server-side.
- **Detection**:
  - Ensure the API only returns the required data and no sensitive information.
  - Review API responses for metadata leaks or unintentional exposure of sensitive data.
  - Use scanners but manually review what’s being returned.
- **Can Detection Be Automated?**: **Partially**
  - Tools can scan API responses to check for excessive data exposure (e.g., using OWASP ZAP or Burp Suite). However, automated tools may struggle to differentiate between legitimate and sensitive data, requiring manual review.

## 4. Lack of Resources & Rate Limiting

- **Summary**:
  - APIs do not limit resource consumption, enabling attackers to send excessive requests or large payloads to exhaust system resources.
- **Causes**:
  - Missing restrictions on request frequency, payload size, and resource consumption, which can lead to Denial of Service (DoS) attacks.
- **Detection**:
  - Test file uploads and large data requests for size limitations.
  - Check if rate limiting is applied to all endpoints.
  - Ensure input/output size restrictions are enforced to prevent oversized data transmissions.
- **Can Detection Be Automated?**: **Yes**
  - Automated tools can simulate high-frequency requests to test rate limiting and excessive data requests (e.g., large file uploads). Tools like JMeter, Burp Suite, or custom scripts can stress-test APIs.

## 5. Broken Function Level Authorization

- **Summary**:
  - Lower-privileged users gain access to higher-privileged functions or data due to missing or weak authorization checks.
- **Causes**:
  - Insufficient checks on function access, especially if higher-privilege endpoints are predictable (e.g., `/admin` endpoints).
- **Detection**:
  - Use tools like Burp Suite to manipulate URLs, parameters, and HTTP methods (GET, POST, PUT, DELETE) to access higher-privileged functions.
  - Test for hidden endpoints using brute force and analyze all available HTTP methods for each endpoint.
- **Can Detection Be Automated?**: **Partially**
  - Some aspects of function-level authorization can be automated (e.g., testing access to higher-privileged functions via URL manipulation and HTTP methods). However, identifying all possible unauthorized endpoints may require manual testing.

## 6. Mass Assignment

- **Summary**:
  - Client-side data is automatically bound to server-side objects or variables, leading to unintended changes in the backend.
- **Causes**:
  - Automatic binding of client-side data to server objects, often exploited by modifying properties that should not be accessible, especially in frameworks like Node.js and Ruby.
- **Detection**:
  - Identify sensitive properties in API responses and attempt to modify them in subsequent requests.
  - Test if users can modify server-side properties they shouldn’t have access to, such as changing user roles or product prices.
- **Can Detection Be Automated?**: **No**
  - Mass assignment detection typically requires an understanding of business logic, making it difficult to automate. Manual testing is usually required to check if server-side properties are properly restricted.

## 7. Security Misconfiguration

- **Summary**:
  - Weak or improper security configurations expose the API to attacks. This includes poorly configured TLS, CORS policies, or error messages exposing sensitive information.
- **Causes**:
  - Improper configuration of API security settings (e.g., TLS, CORS, error handling), leaving APIs vulnerable to attacks.
  - Failure to patch systems or restrict unnecessary HTTP methods.
- **Detection**:
  - Scan for open ports, improper CORS settings, public access to sensitive data, and incorrect TLS configurations.
  - Test if sensitive information (e.g., stack traces, error details) is exposed in error messages.
- **Can Detection Be Automated?**: **Yes**
  - Automated scanning tools like OWASP ZAP, Burp Suite, or security scanners can detect security misconfigurations, such as open ports, improper CORS settings, missing security headers (CSP, HSTS), and improper TLS configurations.

## 8. Injection

- **Summary**:
  - User input is not properly sanitized, leading to SQL, XML, or OS injections.
- **Causes**:
  - Failure to validate and sanitize user input, allowing attackers to inject malicious queries or commands.
- **Detection**:
  - Test all input fields, including those for file uploads, to identify if user input can lead to SQL, OS, or XML injections.
  - Use payloads such as `';select * from users;--` for SQL injection testing.
  - Use tools like Burp Suite to attempt OS command injections.
- **Can Detection Be Automated?**: **Yes**
  - Tools like OWASP ZAP, Burp Suite, and SQLmap can automate the detection of SQL, XML, and OS injection vulnerabilities.

## 9. Improper Assets Management

- **Summary**:
  - Exposure of outdated API versions or unused endpoints, leading to potential exploitation.
- **Causes**:
  - Lack of inventory management for APIs, resulting in the exposure of deprecated or undocumented API versions.
- **Detection**:
  - Test if older versions of the API can be accessed by changing the version number in the URL.
  - Ensure that all API versions are documented, and brute force test hidden or deprecated endpoints (e.g., `/v1/admin`).
- **Can Detection Be Automated?**: **Partially**
  - Tools can automate the discovery of API versions by altering the URL (e.g., changing `/v2/` to `/v1/`). However, detecting outdated or deprecated APIs might require manual verification.

## 10. Insufficient Logging & Monitoring

- **Summary**:
  - Failure to log important events and monitor API activity, making it difficult to detect and respond to attacks.
- **Causes**:
  - Lack of proper logging of critical API interactions, such as login attempts, access to sensitive data, or suspicious activities.
- **Detection**:
  - Ensure logging includes IP addresses, timestamps, input data, and the endpoints accessed, while avoiding logging sensitive information like PII.
  - Regularly review logs for suspicious activities and test for potential log injection attacks.
- **Can Detection Be Automated?**: **No**
  - While monitoring tools can automate log generation and analysis, detecting insufficient logging itself requires manual review. Identifying missing log entries, incomplete logs, or logging of sensitive information often requires a manual audit.
