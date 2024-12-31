# API Testing
Focuses on detecting Mass Assignment vulnerabilities (other API security issues to follow from the OWASP API Security Top 10) by combining static analysis, 
LLM-powered insights, and dynamic endpoint testing.  
It leverages:
-  OpenAPI Spec Analysis: To identify and prepare endpoints for testing.
-  LLM Integration: To detect suspicious or hidden parameters in schemas and actual API responses.
-  Dynamic Testing: By generating and sending test payloads to endpoints and analyzing their responses for anomalies.
-  Reporting: Aggregating findings into a clear, actionable report detailing vulnerabilities, affected endpoints, and potential exploit vectors.

## Files
  - ApiTestingLlmAssist_working - Working notebook
  - API-LLM-sandbox - Beta testing

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
