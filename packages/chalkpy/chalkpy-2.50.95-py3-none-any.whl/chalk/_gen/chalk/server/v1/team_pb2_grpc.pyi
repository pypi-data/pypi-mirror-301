"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from abc import (
    ABCMeta,
    abstractmethod,
)
from chalk._gen.chalk.server.v1.team_pb2 import (
    CreateEnvironmentRequest,
    CreateEnvironmentResponse,
    CreateProjectRequest,
    CreateProjectResponse,
    CreateServiceTokenRequest,
    CreateServiceTokenResponse,
    CreateTeamRequest,
    CreateTeamResponse,
    DeleteServiceTokenRequest,
    DeleteServiceTokenResponse,
    ExpireTeamInviteRequest,
    ExpireTeamInviteResponse,
    GetAgentRequest,
    GetAgentResponse,
    GetAvailablePermissionsRequest,
    GetAvailablePermissionsResponse,
    GetDisplayAgentRequest,
    GetDisplayAgentResponse,
    GetEnvRequest,
    GetEnvResponse,
    GetEnvironmentsRequest,
    GetEnvironmentsResponse,
    GetTeamRequest,
    GetTeamResponse,
    InviteTeamMemberRequest,
    InviteTeamMemberResponse,
    ListServiceTokensRequest,
    ListServiceTokensResponse,
    ListTeamInvitesRequest,
    ListTeamInvitesResponse,
    UpdateScimGroupSettingsRequest,
    UpdateScimGroupSettingsResponse,
    UpdateServiceTokenRequest,
    UpdateServiceTokenResponse,
    UpsertFeaturePermissionsRequest,
    UpsertFeaturePermissionsResponse,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    UnaryUnaryMultiCallable,
)

class TeamServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    GetEnv: UnaryUnaryMultiCallable[
        GetEnvRequest,
        GetEnvResponse,
    ]
    GetEnvironments: UnaryUnaryMultiCallable[
        GetEnvironmentsRequest,
        GetEnvironmentsResponse,
    ]
    GetAgent: UnaryUnaryMultiCallable[
        GetAgentRequest,
        GetAgentResponse,
    ]
    GetDisplayAgent: UnaryUnaryMultiCallable[
        GetDisplayAgentRequest,
        GetDisplayAgentResponse,
    ]
    GetTeam: UnaryUnaryMultiCallable[
        GetTeamRequest,
        GetTeamResponse,
    ]
    CreateTeam: UnaryUnaryMultiCallable[
        CreateTeamRequest,
        CreateTeamResponse,
    ]
    CreateProject: UnaryUnaryMultiCallable[
        CreateProjectRequest,
        CreateProjectResponse,
    ]
    CreateEnvironment: UnaryUnaryMultiCallable[
        CreateEnvironmentRequest,
        CreateEnvironmentResponse,
    ]
    GetAvailablePermissions: UnaryUnaryMultiCallable[
        GetAvailablePermissionsRequest,
        GetAvailablePermissionsResponse,
    ]
    CreateServiceToken: UnaryUnaryMultiCallable[
        CreateServiceTokenRequest,
        CreateServiceTokenResponse,
    ]
    DeleteServiceToken: UnaryUnaryMultiCallable[
        DeleteServiceTokenRequest,
        DeleteServiceTokenResponse,
    ]
    ListServiceTokens: UnaryUnaryMultiCallable[
        ListServiceTokensRequest,
        ListServiceTokensResponse,
    ]
    UpdateServiceToken: UnaryUnaryMultiCallable[
        UpdateServiceTokenRequest,
        UpdateServiceTokenResponse,
    ]
    InviteTeamMember: UnaryUnaryMultiCallable[
        InviteTeamMemberRequest,
        InviteTeamMemberResponse,
    ]
    ExpireTeamInvite: UnaryUnaryMultiCallable[
        ExpireTeamInviteRequest,
        ExpireTeamInviteResponse,
    ]
    ListTeamInvites: UnaryUnaryMultiCallable[
        ListTeamInvitesRequest,
        ListTeamInvitesResponse,
    ]
    UpsertFeaturePermissions: UnaryUnaryMultiCallable[
        UpsertFeaturePermissionsRequest,
        UpsertFeaturePermissionsResponse,
    ]
    UpdateScimGroupSettings: UnaryUnaryMultiCallable[
        UpdateScimGroupSettingsRequest,
        UpdateScimGroupSettingsResponse,
    ]

class TeamServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def GetEnv(
        self,
        request: GetEnvRequest,
        context: ServicerContext,
    ) -> GetEnvResponse: ...
    @abstractmethod
    def GetEnvironments(
        self,
        request: GetEnvironmentsRequest,
        context: ServicerContext,
    ) -> GetEnvironmentsResponse: ...
    @abstractmethod
    def GetAgent(
        self,
        request: GetAgentRequest,
        context: ServicerContext,
    ) -> GetAgentResponse: ...
    @abstractmethod
    def GetDisplayAgent(
        self,
        request: GetDisplayAgentRequest,
        context: ServicerContext,
    ) -> GetDisplayAgentResponse: ...
    @abstractmethod
    def GetTeam(
        self,
        request: GetTeamRequest,
        context: ServicerContext,
    ) -> GetTeamResponse: ...
    @abstractmethod
    def CreateTeam(
        self,
        request: CreateTeamRequest,
        context: ServicerContext,
    ) -> CreateTeamResponse: ...
    @abstractmethod
    def CreateProject(
        self,
        request: CreateProjectRequest,
        context: ServicerContext,
    ) -> CreateProjectResponse: ...
    @abstractmethod
    def CreateEnvironment(
        self,
        request: CreateEnvironmentRequest,
        context: ServicerContext,
    ) -> CreateEnvironmentResponse: ...
    @abstractmethod
    def GetAvailablePermissions(
        self,
        request: GetAvailablePermissionsRequest,
        context: ServicerContext,
    ) -> GetAvailablePermissionsResponse: ...
    @abstractmethod
    def CreateServiceToken(
        self,
        request: CreateServiceTokenRequest,
        context: ServicerContext,
    ) -> CreateServiceTokenResponse: ...
    @abstractmethod
    def DeleteServiceToken(
        self,
        request: DeleteServiceTokenRequest,
        context: ServicerContext,
    ) -> DeleteServiceTokenResponse: ...
    @abstractmethod
    def ListServiceTokens(
        self,
        request: ListServiceTokensRequest,
        context: ServicerContext,
    ) -> ListServiceTokensResponse: ...
    @abstractmethod
    def UpdateServiceToken(
        self,
        request: UpdateServiceTokenRequest,
        context: ServicerContext,
    ) -> UpdateServiceTokenResponse: ...
    @abstractmethod
    def InviteTeamMember(
        self,
        request: InviteTeamMemberRequest,
        context: ServicerContext,
    ) -> InviteTeamMemberResponse: ...
    @abstractmethod
    def ExpireTeamInvite(
        self,
        request: ExpireTeamInviteRequest,
        context: ServicerContext,
    ) -> ExpireTeamInviteResponse: ...
    @abstractmethod
    def ListTeamInvites(
        self,
        request: ListTeamInvitesRequest,
        context: ServicerContext,
    ) -> ListTeamInvitesResponse: ...
    @abstractmethod
    def UpsertFeaturePermissions(
        self,
        request: UpsertFeaturePermissionsRequest,
        context: ServicerContext,
    ) -> UpsertFeaturePermissionsResponse: ...
    @abstractmethod
    def UpdateScimGroupSettings(
        self,
        request: UpdateScimGroupSettingsRequest,
        context: ServicerContext,
    ) -> UpdateScimGroupSettingsResponse: ...

def add_TeamServiceServicer_to_server(servicer: TeamServiceServicer, server: Server) -> None: ...
