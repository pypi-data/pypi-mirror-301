from dataclasses import dataclass, asdict, field
from cooptools.config import JsonConfigHandler
from typing import List, Iterable, Dict
import datetime
from cooptools.typevalidation import datestamp_tryParse
import json
import uuid
import cooptools.date_utils as du
from cooptools.coopEnum import CoopEnum
from cooptools.protocols import UniqueIdentifier

UNDEFINED ='UNDEFINED'

class TaskLinkType(CoopEnum):
    PREDECESSOR = 'predecessor'
    PARENT = 'parent'

@dataclass(frozen=True, slots=True)
class TaskLink:
    task_link_type: TaskLinkType
    linked_task_id: str

@dataclass(frozen=True, slots=True)
class BaseTaskMeta:
    id: UniqueIdentifier = field(default=UNDEFINED)
    task_group_id: UniqueIdentifier = field(default=UNDEFINED)
    task_type: str = field(default=UNDEFINED)
    creating_user_id: UniqueIdentifier = field(default=UNDEFINED)
    required_agent_id: UniqueIdentifier=None
    task_links: Iterable[TaskLink] = None
    created_date: datetime.datetime = field(default_factory=du.now)
    due_date: datetime.datetime = None
    expiration_date: datetime.datetime = None
    priority: int = 999

    def __post_init__(self):
        object.__setattr__(self, f'{self.due_date=}'.split('=')[0].replace('self.', ''), datestamp_tryParse(self.due_date))
        object.__setattr__(self, f'{self.created_date=}'.split('=')[0].replace('self.', ''), datestamp_tryParse(self.created_date))
        object.__setattr__(self, f'{self.expiration_date=}'.split('=')[0].replace('self.', ''), datestamp_tryParse(self.expiration_date))
        if type(self.priority) == str:
            object.__setattr__(self, f'{self.priority=}'.split('=')[0].replace('self.', ''), int(self.priority))

    def toJson(self):
        return json.dumps(asdict(self), default=str, indent=4)


@dataclass(frozen=True, slots=True)
class MissionTaskMeta:
    base_meta: BaseTaskMeta
    task_names: Iterable[str]

    def __post_init__(self):
        if type(self.base_meta) == dict:
            object.__setattr__(self, f'{self.base_meta=}'.replace('self.', '').split('=')[0], BaseTaskMeta(**self.base_meta))


if __name__ == '__main__':
    from pprint import pprint

    def test_base_args():
        base = BaseTaskMeta(
            id='test',
            task_group_id='tg1',
            task_type="user type",
        )

        pprint(base)

    test_base_args()