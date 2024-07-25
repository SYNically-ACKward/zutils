#!/bin/bash

# Check if the websites text file exists
if [ ! -f websites.txt ]; then
    echo "Websites file (websites.txt) not found!"
    exit 1
fi

# Read the websites from a text file into an array
readarray -t websites < websites.txt

# User agents to simulate different browsers
user_agents=(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
)

# Function to simulate a single session
simulate_session() {
    local duration=$1  # Duration of the session in seconds
    local end_time=$((SECONDS + duration))

    while [ $SECONDS -lt $end_time ]; do
        # Randomly select a website and a user agent
        website=${websites[$RANDOM % ${#websites[@]}]}
        user_agent=${user_agents[$RANDOM % ${#user_agents[@]}]}

        # Provide feedback to user
        echo "Connecting to: $website"
        echo "Using User Agent: $user_agent"
        echo "Session Duration: $duration seconds"
        echo ""

        # Use wget or curl to visit the website
        if [ $((RANDOM % 2)) -eq 0 ]; then
            wget -q -O /dev/null --user-agent="$user_agent" "$website"
        else
            curl -s -A "$user_agent" "$website" > /dev/null
        fi

        # Random sleep between requests to mimic user behavior
        sleep $((RANDOM % 10 + 1))
    done
}

# Main loop to start multiple sessions
main() {
    while true; do
        # Random session length between 30 and 300 seconds
        session_length=$((RANDOM % 270 + 30))

        # Start a new session in the background
        simulate_session $session_length &

        # Random sleep between starting new sessions
        sleep $((RANDOM % 60 + 1))
    done
}

main