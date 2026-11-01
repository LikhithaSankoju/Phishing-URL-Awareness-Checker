# Test Results

Python version used: 3.14.3   |   Operating system: Windows 11   |   Date: 31 October 2026

| # | Input | Expected result | Actual result | Pass/Fail |
|---|-------|-----------------|---------------|-----------|
| 1 | https://www.example.com/login | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | http://192.0.2.10/account | IP address + HTTP | Uses an IP address instead of a familiar domain. Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | http://example.com@sample.invalid/login | @ symbol + HTTP | Contains an @ symbol; inspect carefully. Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | https://a.b.c.d.e.example.invalid/path | Many hostname segments | Contains many hostname segments/subdomains. | PASS |
| 5 | https://xn--example.invalid/ | Punycode-style hostname | Contains a punycode-style hostname. | PASS |

## Notes

I ran each workbook sample through `inspect_url()` and also through the interactive program. The six warning messages match the starter code in Section 06, so the extra features did not change the test wording.

What surprised me: typing `www.example.com` without `https://` is treated as HTTP, which is why the HTTP warning appears. Also, `https://secure-login.example.invalid` shows no listed signs even though the name looks like a login page. That made the "no signs does not mean safe" rule feel real.

Bonus checks: empty input returns `No URL entered.`; `http://[bad` used to crash with `ValueError`, and after Improvement C it returns `This text is not a valid URL format.`
