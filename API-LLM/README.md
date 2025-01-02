# API Testing
Focuses on detecting Mass Assignment vulnerabilities and other API security issues (e.g., from the OWASP API Security Top 10) by combining static analysis, 
LLM-powered insights, and dynamic endpoint testing.  
It leverages:
-  OpenAPI Spec Analysis: To identify and prepare endpoints for testing.
-  LLM Integration: To detect suspicious or hidden parameters in schemas and actual API responses.
-  Dynamic Testing: By generating and sending test payloads to endpoints and analyzing their responses for anomalies.
-  Reporting: Aggregating findings into a clear, actionable report detailing vulnerabilities, affected endpoints, and potential exploit vectors.

## Environment Details
  - Using a local Ollama service
  - Paths are identified for the API spec and file storage
    - Will be created


## Workflow
1. Environment Configuration
Declare all paths and required variables

2. OpenAPI Specification Analysis/Parse  
Originally thought this would be more useful than it seems to be.  
Sometimes it makes sense to use the API Spec.  
Functions
    - Load and validate the OpenAPI specification.
    - Log validation results without halting execution for failures.
    - Parse the spec to extract endpoints, parameters, and schemas.
    - Attempt to infer endpoint details for incomplete definitions.
    - Flag endpoints that are not properly defined.
    - Save parsed results in a timestamped JSON file.

3. LLM Integration - User/Health Analysis
Analyze the parsed JSON created above to:
    - Identify heartbeat endpoints (returns 200 OK with no parameters).
    - If no explicit heartbeat endpoint is found, infer one dynamically.
    - Save identified endpoints to a JSON file (endpoints_health.json).

4. Test Health Checks
Test the endpoints identified above.
    - Updates endpoints_health.json with results

5. Determine User Registration Endpoints



## Scripts
1. Environment
  - Paths - set up for the API spec and the output folder to store the generated files
  - Model - define the LLM to use
  - Test Data - Things like an email domain or user name. Not required but useful to trace traffic from the test.

2. Validate and parse the spec
  - Input - OpenAPI spec
  - Output - parsed_spec.json file in the output folder

3. Health Checks - LLM Assisted
Has a JSON parsing error that doesn't seem to impact the result
  - Input - parsed_spec.json
  - Output - endpoints_health.json

4. Test Health Check Endpoints
  - Input - endpoints_health.json
  - Output - endpoints_health.json updates with successful requests

5. Determine User Registration Endpoints
  - Input - 
  - Output - 

