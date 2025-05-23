keys = {
    # AWS Credentials
    "AWS Access Key": r"AKIA[0-9A-Z]{12,20}",
    "AWS Secret Key": r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+]{25,50}['\"]",

    # Google Cloud
    "Google API Key": r"AIza[0-9A-Za-z-_]{25,40}",
    "Google OAuth Access Token": r"ya29\.[0-9A-Za-z\-_]+",

    # Microsoft Azure
    # "Azure Storage Account Key": r"[0-9a-zA-Z+\/]{88}",
    "Azure Client Secret": r"(?i)azure(.{0,20})?['\"][0-9a-zA-Z/+]{25,50}['\"]",

    # GitHub
    "GitHub Personal Access Token": r"ghp_[0-9a-zA-Z]{36}",
    "GitHub OAuth Token": r"gho_[0-9a-zA-Z]{36}",
    "GitHub Refresh Token": r"ghr_[0-9a-zA-Z]{36}",

    # Slack
    "Slack Token": r"xox[baprs]-([0-9a-zA-Z]{10,48})?",

    # JSON Web Tokens (JWT)
    "JWT Token": r"eyJ[a-zA-Z0-9]{20,}\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",

    # Basic & Bearer Auth
    # "Basic Auth": r"Basic [a-zA-Z0-9=:_\+/-]{5,100}",
    "Bearer Token": r"Bearer [a-zA-Z0-9-._~+/]{20,}",

    # Cryptographic Hashes
    # These provide a LOT of results
    # "MD5 Hash": r"\b[a-fA-F0-9]{32}\b",
    # "SHA-1 Hash": r"\b[a-fA-F0-9]{40}\b",
    # "SHA-256 Hash": r"\b[a-fA-F0-9]{64}\b",
    # "SHA-512 Hash": r"\b[a-fA-F0-9]{128}\b",

    # PayPal/Braintree
    "PayPal Braintree Access Token": r"access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}",

    # Stripe API Keys
    "Stripe Secret Key": r"sk_live_[0-9a-zA-Z]{24}",
    "Stripe Publishable Key": r"pk_live_[0-9a-zA-Z]{24}",

    # Square API
    "Square Access Token": r"sandbox-sq0atb-[0-9A-Za-z\-_]{22}",
    "Square OAuth Secret": r"sandbox-sq0csp-[0-9A-Za-z\-_]{43}",

    # Twilio API
    "Twilio Account SID": r"AC[a-f0-9]{32}",
    # "Twilio Auth Token": r"[0-9a-f]{32}",

    # Facebook
    "Facebook Access Token": r"EAACEdEose0cBA[0-9A-Za-z]+",
    # "Facebook App Secret": r"[0-9a-f]{32}",

    # Twitter
    "Twitter API Key": r"(?i)twitter(.{0,20})?['\"][0-9a-zA-Z/+]{25,50}['\"]",
    "Twitter API Secret": r"(?i)twitter(.{0,20})?['\"][0-9a-zA-Z/+]{25,50}['\"]",
    "Twitter Bearer Token": r"AAAAAAAAAAAAAAAAAAAAA[0-9A-Za-z%]{32,60}",

    # LinkedIn
    "LinkedIn Client ID": r"(?i)linkedin(.{0,20})?['\"][0-9a-zA-Z]{14,20}['\"]",
    "LinkedIn Client Secret": r"(?i)linkedin(.{0,20})?['\"][0-9a-zA-Z/+]{25,50}['\"]",

    # Dropbox
    "Dropbox API Key": r"sl\.[A-Za-z0-9_-]{20,100}",

    # Discord
    "Discord Token": r"mfa\.[a-zA-Z0-9_-]{84}",

    # Mailgun
    "Mailgun API Key": r"key-[0-9a-zA-Z]{32}",

    # Heroku API Key
    "Heroku API Key": r"(?i)heroku(.{0,20})?['\"][0-9a-fA-F]{32}['\"]",

    # Shopify
    "Shopify API Key": r"shpca_[0-9a-fA-F]{32}",
    "Shopify Admin Access Token": r"shpat_[0-9a-fA-F]{32}",
    "Shopify Shared Secret": r"shpss_[0-9a-fA-F]{32}",

    # Coinbase
    "Coinbase API Key": r"(?i)coinbase(.{0,20})?['\"][0-9a-zA-Z]{25,50}['\"]",

    # OpenAI API Key
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{32,48}",

    # Custom Tokens
    # "Generic Secret Key": r"(?i)(secret|password|token|key|private|auth|api)[\s:=]{0,5}['\"][0-9a-zA-Z/+]{25,50}['\"]"
}
