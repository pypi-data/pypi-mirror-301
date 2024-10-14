from collections.abc import Iterable, Mapping
from typing import Any, Optional

import xmltodict

from jinjanator_plugins import (
    Formats,
    plugin_formats_hook,
)


class XMLFormat:
    name = "xml"
    suffixes: Optional[Iterable[str]] = ".xml"
    option_names: Optional[Iterable[str]] = "process-namespaces"

    def __init__(self, options: Optional[Iterable[str]]) -> None:
        self.process_namespaces = False
        if options:
            for _option in options:
                self.process_namespaces = True

    def parse(
        self,
        data_string: str,
    ) -> Mapping[str, Any]:
        return xmltodict.parse(data_string, process_namespaces=self.process_namespaces)


@plugin_formats_hook
def plugin_formats() -> Formats:
    return {XMLFormat.name: XMLFormat}
