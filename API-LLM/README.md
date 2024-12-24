# API Testing
Focuses on detecting Mass Assignment vulnerabilities and other API security issues (e.g., from the OWASP API Security Top 10) by combining static analysis, 
LLM-powered insights, and dynamic endpoint testing.  
It leverages:
-  OpenAPI Spec Analysis: To identify and prepare endpoints for testing.
-  LLM Integration: To detect suspicious or hidden parameters in schemas and actual API responses.
-  Dynamic Testing: By generating and sending test payloads to endpoints and analyzing their responses for anomalies.
-  Reporting: Aggregating findings into a clear, actionable report detailing vulnerabilities, affected endpoints, and potential exploit vectors.

## Workflow
1. OpenAPI Specification Analysis
    Load and validate the OpenAPI specification.
        Log validation results without halting execution for failures.
    Parse the spec to extract endpoints, parameters, and schemas.
        Attempt to infer endpoint details for incomplete definitions.
        Flag endpoints that are not properly defined.
    Save parsed results in a timestamped JSON file.
2. LLM Integration - User/Health Analysis
    Analyze the parsed JSON or original spec to:
        Identify a heartbeat endpoint (returns 200 OK with no parameters).
            If no explicit heartbeat endpoint is found, infer one dynamically.
            Run the heartbeat periodically to ensure API availability.
        Locate user-related endpoints (e.g., login, registration, authentication).
    Save identified endpoints to a timestamped JSON file.
3. Testing Initialization
    Use the heartbeat endpoint to confirm the API application is running before initiating tests.
    Prepare the list of all endpoints to test (from the parsed spec and inferred details).
4. LLM Integration - Suspicious Parameter Detection
    Query the LLM to identify suspicious parameters for mass assignment testing.
        Retry if no results are obtained, fallback to pre-defined parameter patterns, then skip if necessary.
    Save suggested parameters for each endpoint in a JSON file.
5. Payload Generation
    Use extracted schemas and LLM suggestions to generate test payloads.
        Incorporate suspicious parameters and variations for fuzzing.
        Generate both valid and intentionally malformed payloads.
    Save generated payloads to a timestamped JSON file.
6. Request Sending
    Sequentially or in parallel (based on configuration) send the generated payloads to API endpoints.
        Retry automatically for transient failures, then log warnings and continue.
    Store request/response pairs in a timestamped folder.
7. Response Analysis
    Compare responses to baseline expectations.
        Flag anomalies such as:
            Status code mismatches.
            Role escalation.
            Unexpected schema deviations or sensitive data exposure.
        Include response headers and performance metrics in the analysis.
    Save analysis results to a JSON file.
8. Reporting
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
