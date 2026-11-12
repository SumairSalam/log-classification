import re


def classify_with_regex(log_message):
        log_message = ' '.join(log_message.split())  # normalize whitespace

        regex_patterns = {
            r"User User\d+ logged (in|out).*": "User Action",
            r".*GET /v2/.*/servers/detail.*": "API Request - List Servers",
            r"Backup (started|ended) at .*": "System Notification",
            r"Backup completed successfully.*": "System Notification",
            r"System updated to version .*": "System Notification",
            r"File .* uploaded successfully by user .*": "System Notification",
            r"Disk cleanup completed successfully.*": "System Notification",
            r"System reboot initiated by user .*": "System Notification",

            r"Account with ID .* created by .*": "User Action",

            # Additional Patterns for OpenStack logs and common messages:
            r"nova\.compute\.resource_tracker .*": "Resource Tracker",

            r"nova\.osapi_compute\.wsgi\.server\s+-\s+GET\s+/v2(?:/[^/]+)?/servers/detail": "API Request - List Servers",
            r"nova\.osapi_compute\.wsgi\.server\s+-\s+DELETE\s+/v2/.+/servers/.+": "API Request - Delete Server",

            r"nova\.compute\.claims .*disk limit.*": "Resource Claim",
            r"nova\.metadata\.wsgi\.server .*": "Metadata Request",
            r".*SSL certificate errors.*": "Security Error",
            r".*API access control system blocked user.*": "Access Control",
            r".*Critical system unit error.*": "System Error",

            r".*Input to module .* was not in the expected format.*": "Data Format Error"
        }

        for pattern, label in regex_patterns.items():
            if re.search(pattern, log_message, re.IGNORECASE):
                return label

        return "Other"


    # Test block (optional)
if __name__ == "__main__":
        test_logs = [
            "User User123 logged in",
            "Backup started at 12:00",
            "Backup completed successfully",
            "System updated to version 12.3.1",
            "File report.txt uploaded successfully by user admin",
            "Disk cleanup completed successfully",
            "System reboot initiated by user root",
            "Account with ID 12345 created by admin",
            "nova.compute.resource_tracker update",
            "nova.osapi_compute.wsgi.server - GET /v2/servers/detail",
            "nova.metadata.wsgi.server processing metadata",
            "SSL certificate errors detected",

            "Input to module DataProcessor was not in the expected format",
            "Random message that doesn’t match"
        ]

        for log in test_logs:
            print(f"{log} -> {classify_with_regex(log)}")
