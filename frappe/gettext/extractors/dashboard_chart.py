import json
from collections.abc import Iterator
from typing import IO, Any

from .utils import get_line_number

ExtractedMessage = tuple[int | None, str, str, list[str]]


def extract(fileobj: IO[bytes], *args: Any, **kwargs: Any) -> Iterator[ExtractedMessage]:
	"""
	Extract messages from Dashboard Chart JSON files. To be used as a babel extractor.

	Extracts:
	- `chart_name`: the chart's title, used when a Workspace Chart has no label
	- `report_name`: the source report, shown in the chart's "{0} Report" action
	- `empty_state_message`: the text shown when the chart has no data

	:param fileobj: the file-like object the messages should be extracted from
	:rtype: `iterator`
	"""
	text = fileobj.read().decode()
	data = json.loads(text)

	if isinstance(data, list):
		return

	if data.get("doctype") != "Dashboard Chart":
		return

	chart_name = data.get("chart_name")

	if chart_name:
		yield get_line_number(text, "chart_name", chart_name), "_", chart_name, ["Name of a Dashboard Chart"]

	report_name = data.get("report_name")

	if report_name:
		yield (
			get_line_number(text, "report_name", report_name),
			"_",
			report_name,
			[f"Name of the report used by the {chart_name} Dashboard Chart"],
		)

	empty_state_message = data.get("empty_state_message")

	if empty_state_message:
		yield (
			get_line_number(text, "empty_state_message", empty_state_message),
			"_",
			empty_state_message,
			[f"Empty state message of the {chart_name} Dashboard Chart"],
		)
