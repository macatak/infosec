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


  - Input - 
  - Output - 
!!!!!!!!!!!!!!  TBD !!!!!!!!!!!!!!!!!!!!!

4. Testing Initialization
    Use the heartbeat endpoint to confirm the API application is running before initiating tests.
    Prepare the list of all endpoints to test (from the parsed spec and inferred details).
5. LLM Integration - Suspicious Parameter Detection
    Query the LLM to identify suspicious parameters for mass assignment testing.
        Retry if no results are obtained, fallback to pre-defined parameter patterns, then skip if necessary.
    Save suggested parameters for each endpoint in a JSON file.
6. Payload Generation
    Use extracted schemas and LLM suggestions to generate test payloads.
        Incorporate suspicious parameters and variations for fuzzing.
        Generate both valid and intentionally malformed payloads.
    Save generated payloads to a timestamped JSON file.
7. Request Sending
    Sequentially or in parallel (based on configuration) send the generated payloads to API endpoints.
        Retry automatically for transient failures, then log warnings and continue.
    Store request/response pairs in a timestamped folder.
8. Response Analysis
    Compare responses to baseline expectations.
        Flag anomalies such as:
            Status code mismatches.
            Role escalation.
            Unexpected schema deviations or sensitive data exposure.
        Include response headers and performance metrics in the analysis.
    Save analysis results to a JSON file.
9. Reporting
    Consolidate findings from all steps into a single JSON report.
        Include all tested endpoints, suspicious parameters, and detected vulnerabilities.
        Highlight endpoints flagged as improperly defined.
        Provide a summary of test coverage and flagged anomalies.
    Save the report to a timestamped folder.

## Scripts
1. OpenAPI Validation/Parser Script
    Input: OpenAPI specification file (JSON or YAML).
    Output:
        Log file with validation results.
        Parsed JSON file containing endpoint details, parameters, and schemas (stored in a timestamped folder).
2. LLM Integration Script 1 - User/Health Analysis
    Input: OpenAPI spec (original file or parsed JSON).
    Output: JSON file with identified heartbeat and user-related endpoints (stored in a timestamped folder).
3. Payload Generation Script
    Input:
        Parsed JSON file of schemas.
        JSON file with user-related endpoint details.
    Output: JSON file with generated payloads for testing (stored in a timestamped folder).
4. Request Sending and Response Capturing Script
    Input:
        JSON file with generated payloads.
        List of API endpoints (from parsed JSON or user-specified input).
    Output: JSON file of request/response pairs (stored in a timestamped folder).
5. LLM Integration Script 2 - Suspicious Parameter Detection (Uses Actual Responses)
    Input: JSON file of request/response pairs.
    Output: JSON file with suspicious parameters identified using LLM (stored in a timestamped folder).
6. Response Analysis Script (Includes Mass Assignment Detection)
    Input:
        JSON file of request/response pairs.
        JSON file with suspicious parameters (from LLM suggestions).
    Output: JSON file with flagged anomalies and analysis results (stored in a timestamped folder).
7. Reporting Script
    Input:
        JSON files from response analysis and earlier scripts.
    Output:
        Consolidated JSON report summarizing all findings.
        Optionally, human-readable format for stakeholders.
