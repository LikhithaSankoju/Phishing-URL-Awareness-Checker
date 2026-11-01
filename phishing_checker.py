import re
from urllib.parse import urlparse


# Messages that are information, not warning signs.
INFO_PREFIXES = (
    "No URL entered",
    "Could not identify",
    "No listed warning",
    "This text is not a valid URL format",
)

# Short reasons printed under each warning (Improvement D).
REASONS = {
    "Contains an @ symbol; inspect carefully.": (
        "A browser can ignore the text before @, so the link may go somewhere else."
    ),
    "Unusually long URL (over 100 characters).": (
        "A very long link can hide the real destination far to the right."
    ),
    "Uses an IP address instead of a familiar domain.": (
        "Everyday sites usually use a name, not a number address."
    ),
    "Contains many hostname segments/subdomains.": (
        "Stacking many name parts can make a link look more official than it is."
    ),
    "Contains a punycode-style hostname.": (
        "xn-- can hide look-alike letters that mimic a familiar name."
    ),
    "Uses HTTP. HTTPS alone does not prove trust.": (
        "HTTP is not encrypted, so data can be seen on the way."
    ),
}


def inspect_url(raw_url):
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url

    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ["This text is not a valid URL format."]

    host = (parsed.hostname or "").lower()
    if not host:
        return ["Could not identify a hostname."]

    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def has_warnings(findings):
    """True when the first message is a real warning, not an info line."""
    if not findings:
        return False
    return not findings[0].startswith(INFO_PREFIXES)


def print_findings(findings):
    print("\nResult:")
    for item in findings:
        print("- " + item)
        reason = REASONS.get(item)
        if reason:
            print("    Why: " + reason)

    if has_warnings(findings):
        print("\nREVIEW CAREFULLY: " + str(len(findings)) + " warning sign(s) found.")
    print("Never enter passwords from unexpected links.")


def main():
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")
    print("Type q and press Enter to quit.")

    while True:
        try:
            raw_url = input("\nEnter a sample URL to inspect: ")
        except EOFError:
            print("\nGoodbye! Stay alert online.")
            break

        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        print_findings(inspect_url(raw_url))


if __name__ == "__main__":
    main()
