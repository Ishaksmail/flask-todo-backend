ERROR_MESSAGES = {
    "USER_ID_REQUIRED": "User ID is required.",
    "USER_NOT_FOUND": "User not found.",
    "USERNAME_ALREADY_EXISTS": "Username is already taken.",
    "EMAIL_ALREADY_EXISTS": "Email address is already registered.",
    "INVALID_CREDENTIALS": "Invalid login credentials.",
    "PASSWORD_TOO_SHORT": "Password must be at least 6 characters long.",
    "PASSWORD_REQUIRED": "Password is required.",
    "USERNAME_REQUIRED": "Username is required.",
    "EMAIL_NOT_FOUND": "Email not found.",
    "EMAIL_REQUIRED": "Email address is required.",
    "EMAIL_NOT_VERIFIED": "No verified email associated with this account.",
    "NO_ACTIVE_PRIMARY_EMAIL": "No active primary email found for this account.",
    "PRIMARY_EMAIL_REQUIRED": "Exactly one primary email is required.",
    "PASSWORD_RESET_LINK_SENT": "Password reset link has been sent to your email.",
    
    # ✅ Password hashing service
    "INVALID_PASSWORD_LENGTH": "Password must be at least 8 characters long.",
    "INVALID_PASSWORD_INPUTS": "Valid password and hashed password are required.",
    "PASSWORD_VERIFICATION_FAILED": "Password verification failed.",

    # ✅ Register user use case
    "ALL_FIELDS_REQUIRED": "All fields (username, email, password) are required.",

    # ✅ Reset password use case
    "MISSING_RESET_TOKEN": "Password reset token is required.",
    "INVALID_NEW_PASSWORD": "New password must be at least 8 characters long.",
    "INVALID_OR_EXPIRED_TOKEN": "Invalid or expired password reset token.",
    "INVALID_TOKEN_TYPE": "Invalid token type.",
    "TOKEN_NOT_FOUND": "Password reset token not found.",
    "TOKEN_ALREADY_USED": "Password reset token has already been used.",
    "TOKEN_CONFIRMATION_FAILED": "Failed to confirm password reset token.",

    # ✅ Reset username use case
    "MISSING_CURRENT_USERNAME": "Current username is required.",
    "INVALID_NEW_USERNAME": "New username is invalid or already taken.",
    "USERNAME_UPDATE_FAILED": "Failed to update username.",

    # ✅ Mail service
    "EMAIL_SEND_FAILED": "Failed to send email.",

    # ✅ Token service
    "TOKEN_INVALID_OR_EXPIRED": "Token is invalid or has expired.",
    "TOKEN_GENERATION_FAILED": "Failed to generate token.",
    "TOKEN_MATCH_FAILED": "Failed to match token hash.",

    # ✅ Verified email use case
    "MISSING_VERIFICATION_TOKEN": "Verification token is required.",
    "MISSING_TOKEN_DATA": "Token data is missing or invalid.",
    "VERIFICATION_TOKEN_NOT_FOUND": "No verification token found for this email.",
    "TOKEN_MISMATCH": "Verification token does not match the stored record.",
    "EMAIL_VERIFIED_SUCCESS": "Email has been successfully verified.",
    
    # ✅ Group
    "MISSING_FIELDS": "Required fields are missing.",
    "GROUP_NOT_FOUND": "Group not found.",
    
    # ✅ Task
    "TASK_NOT_FOUND": "Task not found.",
}
