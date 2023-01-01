on run {targetGirlPhone, targetMessage}
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetGirl to buddy targetGirlPhone of targetService
        send targetMessage to targetGirl
    end tell
end run
