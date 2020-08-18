# CSP Observer Data Repository
This repository contains a collection of identified CSP report causes in a standardized format.

The data is used by [django-csp-observer](https://github.com/flxn/django-csp-observer) to provider user feedback about potentially malicious browser behavior.

## Rule Format

### Required Information

The required fields are:

| Field | Description | Required? |
| ----- | ----------- | --------- |
| `cause` | The origin that caused the CSP violation. Must be one of the following: `extension` (for browser extensions), `browser` (for violations directly caused by the web browser), `malware` (if the violation can be directly attributed to malware), `other` (for all other/unknown sources) | `yes` |
| `title` | The title of the Rule that will be shown to the user. E.g. the name of the corresponding browser extension that causes the violation. | `yes` |
| `description` | A more detailed description of the rule that will be shown to the user. | `yes` |
| `url` | The url that caused the violation (blocked-uri). Must be a simple string or a valid Python RegEx expression string (for wildcard URLs) | `yes` |
| `directive` | Can be used to apply the rule only for specific violated CSP directives. Multiple directives can be separated by commas. If the field is omitted the rule will apply to all violations that match the specified url. | `no` |

You can specify additional urls/directives by adding additional url/directive parameters with a number appendix (`url_n`/`directive_n`). If you have 3 different urls you would add the following fields:
`url`, `directive`, `url_2`, `directive_2`, `url_3`, `directive_3`. The `directive` field is still optional but it has to match the numbering of the corresponding url.

### Markdown Template

Below is the example markdown format of the rule file. All rules **must** follow this template so that they can be automatically parsed.
You can view an example rule in ``rules/demo_test.md``.

```
# $TITLE

| Field       | Value |
| ----------- | ----- |
| cause       | $CAUSE |
| title       | $TITLE |
| description | $LONG_DESCRIPTION |
| url         | $URL |
| directive   | $DIRECTIVE |
| url_2       | $URL_2 |
| directive_2 | $DIRECTIVE_2 |

/* You can remove the url_2/directive_2 parameters if you do not need them or add more if you need them (following the url_n/directive_n scheme) */

## Comments

/* You can include any custom content here. E.g. to explain how you found the violation and why you think the rule should be included. */
```

Replace `$CAUSE`, `$TITLE`, etc. with the appropriate values as described under *Required Information*.

Place the file in the `rules` directory and give it a **lowercase**, **camel case** filename following the format `$CAUSE_$TITLE.md`