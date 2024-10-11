from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pararamio.client import Pararamio
from pararamio.exceptions import PararamioRequestException
from pararamio.user import User
from pararamio.group import Group
from pararamio.utils import get_formatted_attr_or_load, parse_iso_datetime


if TYPE_CHECKING:
    from datetime import datetime
    from pararamio._types import FormatterT
__all__ = (
    'TeamMember',
    'Team',
    'TeamMemberStatus',
)

ATTR_FORMATTERS: 'FormatterT' = {
    'time_edited': parse_iso_datetime,
    'time_created': parse_iso_datetime,
}
MEMBER_ATTR_FORMATTERS: 'FormatterT' = {
    **ATTR_FORMATTERS,
    'last_activity': parse_iso_datetime,
}
STATUS_ATTR_FORMATTERS: 'FormatterT' = {
    'time_created': parse_iso_datetime,
}


class TeamMemberStatus:
    __slots__ = (
        'client',
        '_data',
    )
    client: 'Pararamio'
    _data: Dict[str, Any]
    id: int
    user_id: int
    setter_id: int
    org_id: int
    time_created: 'datetime'
    status: str

    def __init__(self, client: 'Pararamio', id: int, **kwargs):
        self.client = client
        self._data = {**kwargs, 'id': int(id)}

    def __getattr__(self, key: str) -> Any:
        return get_formatted_attr_or_load(self, key, STATUS_ATTR_FORMATTERS)


class TeamMember:
    __slots__ = ('client', '_data')
    _data: Dict[str, Any]
    chats: List[int]
    email: str
    groups: List[int]
    id: int
    org_id: int
    inviter_id: Optional[int]
    is_admin: bool
    is_member: bool
    last_activity: 'datetime'
    phonenumber: str
    state: str
    time_created: 'datetime'
    time_updated: 'datetime'
    two_step_enabled: bool

    def __init__(self, client: 'Pararamio', id: int, org_id: int, **kwargs):
        self.client = client
        self._data = {**kwargs, 'id': int(id), 'org_id': int(org_id)}

    def __getattr__(self, key: str) -> Any:
        return get_formatted_attr_or_load(self, key, MEMBER_ATTR_FORMATTERS)

    def __str__(self):
        return self._data.get('email', self._data['id'])

    def __eq__(self, other):
        if not isinstance(other, (TeamMember, User)):
            return hash(other) == hash(self)
        return self.id == other.id

    @property
    def user(self) -> User:
        return User(client=self.client, id=self.id)

    def get_last_status(self) -> Optional['TeamMemberStatus']:
        url = f'/core/org/status?user_ids={self.id}'
        res = self.client.api_get(url).get('data', [])
        if not res:
            return None
        return TeamMemberStatus(self.client, **res[0])

    def add_status(self, status: str) -> bool:
        url = '/core/org/status'
        data = {
            'org_id': self.org_id,
            'status': status,
            'user_id': self.id,
        }
        res = self.client.api_post(url, data=data)
        return bool(res) and res.get('result') == 'OK'


class Team:
    __slots__ = (
        '_data',
        'client',
        '_load_on_key_error',
    )
    _data: Dict[str, Any]
    client: 'Pararamio'
    admins: List[int]
    default_thread_id: int
    description: Optional[str]
    email_domain: Optional[str]
    groups: List[int]
    guest_thread_id: Optional[int]
    guests: List[int]
    id: int
    inviter_id: Optional[int]
    is_active: bool
    slug: str
    state: str
    time_created: str
    time_updated: str
    title: str
    two_step_required: bool
    users: List[int]
    _load_on_key_error: bool

    def __init__(self, client: 'Pararamio', id: int, load_on_key_error: bool = True, **kwargs):
        self.client = client
        self._load_on_key_error = load_on_key_error
        self._data = {**kwargs, 'id': int(id)}

    def __getattr__(self, key: str) -> Any:
        return get_formatted_attr_or_load(
            self,
            key,
            ATTR_FORMATTERS,
        )

    def __str__(self):
        text = self._data.get('text', None)
        if text is None:
            self.load()
            text = self._data['text']
        return text

    def __eq__(self, other):
        if not isinstance(other, Team):
            return hash(other) == hash(self)
        return self.id == other.id

    def __contains__(self, item):
        if not isinstance(item, (TeamMember, User)):
            return False
        return item.id in self.users

    def create_role(self, name: str, description: Optional[str] = None) -> 'Group':
        return Group.create(
            self.client, organization_id=self.id, name=name, description=description
        )

    def load(self):
        """
        Fetches data from the API for the current organization's ID and updates the object's data.

        Requests data from the organization's endpoint using the object's ID,
        then updates the object's data with the response.

        Returns:
            self: The current object instance with updated data.
        """
        url = f'/core/org?ids={self.id}'
        res = self.client.api_get(url)
        self._data.update(res)
        return self

    def member_info(self, user_id: int) -> 'TeamMember':
        url = f'/core/org/{self.id}/member_info/{user_id}'
        res = self.client.api_get(url)
        if not res:
            raise PararamioRequestException(f'empty response for user {user_id}')
        return TeamMember(self.client, org_id=self.id, **res)

    def members_info(self) -> List['TeamMember']:
        url = f'/core/org/{self.id}/member_info'
        res = self.client.api_get(url)
        if res:
            return [TeamMember(self.client, org_id=self.id, **m) for m in res.get('data', [])]
        return []

    @classmethod
    def my_team_ids(cls, client: 'Pararamio') -> List[int]:
        url = '/core/org/sync'
        res = client.api_get(url) or {}
        return res.pop('ids', [])

    @classmethod
    def load_teams(cls, client: 'Pararamio') -> List['Team']:
        """

        Loads teams from the Pararamio client.

        @param client: An instance of the Pararamio client.
        @return: A list of Team objects.
        """
        ids = cls.my_team_ids(client)

        if ids:
            url = '/core/org?ids=' + ','.join(map(str, ids))
            res = client.api_get(url)

            if res:
                return [cls(client, **r) for r in res['orgs']]

        return []
