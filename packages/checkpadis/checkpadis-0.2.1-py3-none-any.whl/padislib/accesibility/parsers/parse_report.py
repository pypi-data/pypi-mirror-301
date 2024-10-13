from padislib.accessibility.enums.reports_keys import ReportKeys
from padislib.accessibility.parsers.translation import Translation


def translate_text(text):
    return Translation.get_translation(text)


def translate_summary(summary):
    for translation in Translation:
        summary = summary.replace(
            translation.value, Translation.get_translation(translation.value)
        )
    return summary


def parse_violation(violation):
    entries = []
    description = translate_text(violation.get("description"))
    impact = violation.get("impact", ReportKeys.DEFAULT_IMPACT.value)
    help_url = violation.get("helpUrl", ReportKeys.DEFAULT_HELP_URL.value)

    for node in violation.get("nodes", []):
        failure_summary = translate_summary(
            node.get(
                "failureSummary", ReportKeys.DEFAULT_FAILURE_SUMMARY.value
            )
        )
        entry = {
            ReportKeys.IMPACT.value: impact,
            ReportKeys.DESCRIPTION.value: description,
            ReportKeys.TARGET_ELEMENTS.value: ", ".join(
                node.get("target", [])
            ),
            ReportKeys.FAILURE_SUMMARY.value: failure_summary,
            ReportKeys.HTML_SNIPPET.value: node.get(
                "html", ReportKeys.DEFAULT_HTML_SNIPPET.value
            ),
            ReportKeys.HELP_URL.value: help_url,
        }
        entries.append(entry)
    return entries


def generate_clean_report(results):
    parsed_report = []
    for _, result in results:
        for violation in result.get("violations", []):
            parsed_report.extend(parse_violation(violation))
    return parsed_report
