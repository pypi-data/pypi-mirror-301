from typing import Any, List, Optional

from botocore.session import Session

class ServiceDocumenter:
    def __init__(self, service_name: str, session: Session, root_docs_path: str) -> None: ...
    def document_service(self) -> bytes: ...
    def title(self, section: Any) -> None: ...
    def table_of_contents(self, section: Any) -> None: ...
    def client_api(self, section: Any) -> None: ...
    def client_exceptions(self, section: Any) -> None: ...
    def paginator_api(self, section: Any) -> None: ...
    def waiter_api(self, section: Any) -> None: ...
    def get_examples(self, service_name: str, api_version: Optional[str] = ...) -> List[str]: ...
    def client_context_params(self, section: Any) -> None: ...
