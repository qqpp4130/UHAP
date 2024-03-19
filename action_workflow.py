class ActionResult:
    def __init__(self, success, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error

def validate(input_params):
    # Example validation logic
    if "key" not in input_params:
        raise ValueError("Input parameters must include 'key'")

def fetch_data(input_params):
    # Example data fetching logic
    return {"fetched_data": input_params["key"]}

def process_data(data):
    # Example data processing logic
    return data.get("fetched_data", "").upper()  # Let's just uppercase the data for this example

def execute_action(processed_data):
    # Example core action logic
    if processed_data == "EXPECTED":
        return "Action was successful"
    else:
        return "Action received unexpected input"

def format_result(result):
    # Example result formatting logic
    return f"Formatted result: {result}"

def log_error(error):
    # Print out error information for debugging purposes
    print(f"An error occurred: {error}")

def action_workflow(input_params):
    try:
        # Validate input parameters
        validate(input_params)

        # Fetch data based on input parameters
        data = fetch_data(input_params)

        # Process the data
        processed_data = process_data(data)

        # Execute the core action
        result = execute_action(processed_data)

        # Format the result for output
        formatted_result = format_result(result)

        # Return the successful action result
        return ActionResult(success=True, data=formatted_result)
    except Exception as error:
        # Log error for debugging purposes
        log_error(error)

        # Return the error information
        return ActionResult(success=False, error=str(error))

# Example usage
input_parameters = {
    "key": "expected"  # This should be the expected input to test the positive case
}
result = action_workflow(input_parameters)
if result.success:
    print("Action succeeded with data:", result.data)
else:
    print("Action failed with error:", result.error)