from abc import ABC, abstractmethod

from uncountable.types import queued_job_t


class Datastore(ABC):
    @abstractmethod
    def add_job_to_queue(
        self, job_payload: queued_job_t.QueuedJobPayload, job_ref_name: str
    ) -> queued_job_t.QueuedJob: ...

    @abstractmethod
    def remove_job_from_queue(self, queued_job_uuid: str) -> None: ...

    @abstractmethod
    def increment_num_attempts(self, queued_job_uuid: str) -> int: ...

    @abstractmethod
    def load_job_queue(self) -> list[queued_job_t.QueuedJob]: ...
