from sigma.pipelines.common import generate_windows_logsource_items
from sigma.processing.transformations import (
    FieldMappingTransformation,
    AddConditionTransformation,
    DropDetectionItemTransformation,
    AddFieldnamePrefixTransformation,
)
from sigma.processing.conditions import (
    LogsourceCondition,
    IncludeFieldCondition,
    FieldNameProcessingItemAppliedCondition,
)
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline

def ecs_cloudtrail() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) aws cloudtrail log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "aws.cloudtrail"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="aws", service="cloudtrail"),
                ],
            ),
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "apiVersion": "aws.cloudtrail.api_version",
                        "awsRegion": "cloud.region",
                        "errorCode": "aws.cloudtrail.error_code",
                        "errorMessage": "aws.cloudtrail.error_message",
                        "eventID": "event.id",
                        "eventName": "event.action",
                        "eventSource": "event.provider",
                        "eventTime": "ts",
                        "eventType": "aws.cloudtrail.event_type",
                        "eventVersion": "aws.cloudtrail.event_version",
                        "managementEvent": "aws.cloudtrail.management_event",
                        "readOnly": "aws.cloudtrail.read_only",
                        "requestID": "aws.cloudtrail.request_id",
                        "resources.accountId": "aws.cloudtrail.resources.account_id",
                        "resources.ARN": "aws.cloudtrail.resources.arn",
                        "resources.type": "aws.cloudtrail.resources.type",
                        "sharedEventId": "aws.cloudtrail.shared_event_id",
                        "sourceIPAddress": "source.address",
                        "userAgent": "user_agent",
                        "userIdentity.accessKeyId": "aws.cloudtrail.user_identity.access_key_id",
                        "userIdentity.accountId": "cloud.account.id",
                        "userIdentity.arn": "aws.cloudtrail.user_identity.arn",
                        "userIdentity.invokedBy": "aws.cloudtrail.user_identity.invoked_by",
                        "userIdentity.principalId": "user.id",
                        "userIdentity.sessionContext.attributes.creationDate": "aws.cloudtrail.user_identity.session_context.creation_date",
                        "userIdentity.sessionContext.attributes.mfaAuthenticated": "aws.cloudtrail.user_identity.session_context.mfa_authenticated",
                        "userIdentity.sessionContext.sessionIssuer.userName": "role.name",
                        "userIdentity.type": "aws.cloudtrail.user_identity.type",
                        "userIdentity.userName": "user.name",
                        "vpcEndpointId": "aws.cloudtrail.vpc_endpoint_id",
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="aws", service="cloudtrail"),
                ],
            )
        ],
    )

def ecs_web_access() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) Web Access log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "webaccess"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="webaccess"),
                ],
            ), 
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "cs-username": "user.name",
                        "c-ip": "source.ip",
                        "c-port": "source.port",
                        "s-ip": "destination.ip",
                        "s-port": "destination.port",
                        "cs-method": "http.request.method",
                        "cs-uri-stem": "url.path",
                        "cs-uri-query": "url.original",
                        "sc-status": "http.respond.code",
                        "sc-bytes": "http.response.body.bytes",
                        "cs-host": "url.domain",
                        "cs-user-agent": "user_agent.original",
                        "cs-referer": "http.referer"
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="webaccess"),
                ],
            )
        ],
    )

def ecs_linux() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) linux log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "linux"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="linux"),
                ],
            ),
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "a0": "process.args",
                        "a1": "process.args",
                        "a2": "process.args",
                        "a3": "process.args",
                        "CommandLine": "process.command_line",
                        "CommandLine": "process.command_line",
                        "event.action": "event.action",
                        "event.category":"event.category",
                        "event.type":"event.type",
                        "exe":"process.executable",
                        "file.Ext.original.extension":"file.Ext.original.extension",
                        "file.extension":"file.extension",
                        "file.path":"file.path",
                        "Image": "process.executable",
                        "Initiated" : "initiated",
                        "ParentCommandLine": "process.parent.command_line",
                        "ParentCommandLine": "process.parent.command_line",
                        "ParentImage": "process.parent.executable",
                        "ParentImage": "process.parent.executable",
                        "process.args":"process.args",
                        "process.executable":"process.executable",
                        "process.name":"process.name",
                        "QueryName": "dns.question.name",
                        "QueryResults": "dns.answers",
                        "user.name":"user.name",
                        "User": "user.name",
                        "TargetFilename":"targetfilename",
                        "DestinationIp":"destination.ip",
                        "DestinationPort":"destinationp.ort",
                        "SourceIp":"source.ip",
                        "SourcePort":"source.port",
                        "DestinationHostname": "destination.host.name"
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="linux"),
                ],
            )
        ],
    )

def ecs_windows() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) windows log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "windows"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="windows"),
                ],
            ),
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "Accesses": "winlog.event_data.Accesses",
                        "AccessList": "winlog.event_data.AccessList",
                        "AccessMask": "winlog.event_data.AccessMask",
                        "AccountName": "winlog.event_data.AccountName",
                        "AllowedToDelegateTo": "winlog.event_data.AllowedToDelegateTo",
                        "AttributeLDAPDisplayName": "winlog.event_data.AttributeLDAPDisplayName",
                        "AttributeValue": "winlog.event_data.AttributeValue",
                        "AuditPolicyChanges": "winlog.event_data.AuditPolicyChanges",
                        "AuditSourceName": "winlog.event_data.AuditSourceName",
                        "AuthenticationAlgorithm": "winlog.event_data.AuthenticationAlgorithm",
                        "AuthenticationPackageName": "winlog.event_data.AuthenticationPackageName",
                        "BSSID": "winlog.event_data.BSSID",
                        "BSSType": "winlog.event_data.BSSType",
                        "CallerProcessName": "winlog.event_data.CallerProcessName",
                        "CallingProcessName": "winlog.event_data.CallingProcessName",
                        "CallTrace": "winlog.event_data.CallTrace",
                        "CertIssuerName": "winlog.event_data.CertIssuerName",
                        "CertSerialNumber": "winlog.event_data.CertSerialNumber",
                        "CertThumbprint": "winlog.event_data.CertThumbprint",
                        "ChangeType": "winlog.event_data.ChangeType",
                        "Channel": "winlog.channel",
                        "CipherAlgorithm": "winlog.event_data.CipherAlgorithm",
                        "ClassName": "winlog.event_data.ClassName",
                        "ClientProcessId": "winlog.event_data.ClientProcessId",
                        "CommandLine": "process.command_line",
                        "Company": "winlog.event_data.Company",
                        "ComputerName": "winlog.ComputerName",
                        "ConnectionId": "winlog.event_data.ConnectionId",
                        "ConnectionMode": "winlog.event_data.ConnectionMode",
                        "ContextInfo": "winlog.event_data.ContextInfo",
                        "CurrentDirectory": "CurrentDirectory",
                        "CurrentDirectory": "process.working_directory",
                        "Description": "winlog.event_data.Description",
                        "DestAddress": "winlog.event_data.DestAddress",
                        "Destination": "Destination",
                        "DestinationHostname": "destination.domain",
                        "DestinationIp": "destination.ip",
                        "DestinationIsIpv6": "winlog.event_data.DestinationIsIpv6",
                        "DestinationPort": "destination.port",
                        "DestinationPortName": "network.protocol",
                        "DestPort": "winlog.event_data.DestPort",
                        "Details": "winlog.event_data.Details",
                        "Device": "Device",
                        "DeviceDescription": "winlog.event_data.DeviceDescription",
                        "DisableIntegrityChecks": "winlog.event_data.DisableIntegrityChecks",
                        "DisplayName": "winlog.event_data.DisplayName",
                        "DnsHostName": "winlog.event_data.DnsHostName",
                        "Domain": "winlog.event_data.Domain",
                        "EnabledPrivilegeList": "winlog.event_data.EnabledPrivilegeList",
                        "EngineVersion":"powershell.engine.version",
                        "EventID":"event.code",
                        "EventType": "winlog.event_data.EventType",
                        "FailureReason": "winlog.event_data.FailureCode",
                        "FileName": "file.path",
                        "FileVersion": "FileVersion",
                        "FilterName": "winlog.event_data.FilterName",
                        "GrantedAccess": "winlog.event_data.GrantedAccess",
                        "GroupMembership": "winlog.event_data.GroupMembership",
                        "Hashes": "Hashes",
                        "Hashes": "winlog.event_data.Hashes",
                        "HiveName": "winlog.event_data.HiveName",
                        "HostApplication": "process.command_line",
                        "HostName": "process.title",
                        "Image": "process.executable",
                        "ImageLoaded": "file.path",
                        "ImagePath": "file.path",
                        "ImagePath": "winlog.event_data.ImagePath",
                        "Imphash": "winlog.event_data.Imphash",
                        "Initiated": "winlog.event_data.Initiated",
                        "IntegrityLevel": "IntegrityLevel",
                        "IntegrityLevel": "winlog.event_data.IntegrityLevel",
                        "InterfaceDescription": "winlog.event_data.InterfaceDescription",
                        "InterfaceGuid": "winlog.event_data.InterfaceGuid",
                        "IpAddress": "source.ip",
                        "IpPort": "source.port",
                        "IsExecutable": "winlog.event_data.IsExecutable",
                        "KernelDebug": "winlog.event_data.KernelDebug",
                        "KeyLength": "winlog.event_data.KeyLength",
                        "LayerName": "winlog.event_data.LayerName",
                        "LayerRTID": "LayerRTID",
                        "LinkName": "LinkName",
                        "LocalName": "winlog.event_data.LocalName",
                        "LogonId" : "winlog.logon.id",
                        "LogonProcessName": "winlog.event_data.LogonProcessName",
                        "LogonType": "winlog.event_data.LogonType",
                        "MemberName": "winlog.event_data.MemberName",
                        "MemberSid": "winlog.event_data.MemberSid",
                        "NewProcessName": "winlog.event_data.NewProcessName",
                        "NewSd": "winlog.event_data.NewSd",
                        "NewTargetUserName": "winlog.event_data.NewTargetUserName",
                        "NewTemplateContent": "winlog.event_data.NewTemplateContent",
                        "NewUacValue": "winlog.event_data.NewUacValue",
                        "NewValue": "winlog.event_data.NewValue",
                        "NotificationPackageName": "winlog.event_data.NotificationPackageName",
                        "ObjectClass": "winlog.event_data.ObjectClass",
                        "ObjectDN": "winlog.event_data.ObjectDN",
                        "ObjectName": "winlog.event_data.ObjectName",
                        "ObjectType": "winlog.event_data.ObjectType",
                        "ObjectValueName": "winlog.event_data.ObjectValueName",
                        "OldTargetUserName": "winlog.event_data.OldTargetUserName",
                        "OldUacValue": "winlog.event_data.OldUacValue",
                        "OnexEnabled": "winlog.event_data.OnexEnabled",
                        "OperationType": "winlog.event_data.OperationType",
                        "OriginalFileName": "OriginalFileName",
                        "OriginalFileName": "winlog.event_data.OriginalFileName",
                        "param1" : "winlog.even_data.param1",
                        "param2" : "winlog.even_data.param2",
                        "param3" : "winlog.even_data.param3",
                        "param4" : "winlog.even_data.param4",
                        "param5" : "winlog.even_data.param5",
                        "param6" : "winlog.even_data.param6",
                        "param7" : "winlog.even_data.param7",
                        "param8" : "winlog.even_data.param8",
                        "param9" : "winlog.even_data.param9",
                        "param10" : "winlog.even_data.param10",
                        "param11" : "winlog.even_data.param11",
                        "param12" : "winlog.even_data.param12",
                        "param13" : "winlog.even_data.param13",
                        "param14" : "winlog.even_data.param14",
                        "param15" : "winlog.even_data.param15",
                        "param16" : "winlog.even_data.param16",
                        "param17" : "winlog.even_data.param17",
                        "param18" : "winlog.even_data.param18",
                        "param19" : "winlog.even_data.param19",
                        "param20" : "winlog.even_data.param20",
                        "param21" : "winlog.even_data.param21",
                        "param22" : "winlog.even_data.param22",
                        "param23" : "winlog.even_data.param23",
                        "param24" : "winlog.even_data.param24",
                        "param25" : "winlog.even_data.param25",
                        "param26" : "winlog.even_data.param26",
                        "param27" : "winlog.even_data.param27",
                        "param28" : "winlog.even_data.param28",
                        "param29" : "winlog.even_data.param29",
                        "param30" : "winlog.even_data.param30",
                        "ParentCommandLine": "process.parent.command_line",
                        "ParentImage": "process.parent.executable",
                        "ParentProcessId": "winlog.event_data.ParentProcessId",
                        "ParentProcessName": "process.parent.name",
                        "ParentUser": "ParentUser",
                        "PasswordLastSet": "winlog.event_data.PasswordLastSet",
                        "Path": "winlog.event_data.Path",
                        "Payload":"powershell.command.invocation_details",
                        "PHYType": "winlog.event_data.PHYType",
                        "PipeName": "file.name",
                        "PreAuthType": "winlog.event_data.PreAuthType",
                        "PrivilegeList": "winlog.event_data.PrivilegeList",
                        "ProcessID": "ProcessID",
                        "ProcessName": "process.executable",
                        "processPath": "winlog.event_data.processPath",
                        "Product": "Product",
                        "Product": "winlog.event_data.Product",
                        "ProfileName": "winlog.event_data.ProfileName",
                        "Properties": "winlog.event_data.Properties",
                        "Provider_Name" : "winlog.provider_name",
                        "Protocol": "winlog.event_data.Protocol",
                        "QueryName": "dns.question.name",
                        "QueryResults": "dns.answers",
                        "QueryStatus": "winlog.event_data.QueryStatus",
                        "RegistryValue": "winlog.event_data.RegistryValue",
                        "RelativeTargetName": "winlog.event_data.RelativeTargetName",
                        "RemoteName": "winlog.event_data.RemoteName",
                        "RuleName": "winlog.event_data.RuleName",
                        "ScriptBlockText": "powershell.file.script_block_text",
                        "SearchFilter": "winlog.event_data.SearchFilter",
                        "SecurityDescriptor":"winlog.event_data.SecurityDescriptor",
                        "SecurityID": "winlog.event_data.SecurityID",
                        "SecurityPackageName": "winlog.event_data.SecurityPackageName",
                        "Service": "Service",
                        "ServiceAccount": "winlog.event_data.ServiceAccount",
                        "ServiceFileName": "winlog.event_data.ServiceFileName",
                        "ServiceName": "winlog.event_data.ServiceName",
                        "ServicePrincipalNames": "winlog.event_data.ServicePrincipalNames",
                        "ServiceSid": "winlog.event_data.ServiceSid",
                        "ServiceStartType": "winlog.event_data.ServiceStartType",
                        "ServiceType": "winlog.event_data.ServiceType",
                        "SessionName": "winlog.event_data.SessionName",
                        "ShareName": "winlog.event_data.ShareName",
                        "SidHistory": "winlog.event_data.SidHistory",
                        "Signature": "winlog.event_data.Signature",
                        "SignatureStatus": "SignatureStatus",
                        "SignatureStatus": "winlog.event_data.SignatureStatus",
                        "Signed": "Signed",
                        "Signed": "winlog.event_data.Signed",
                        "Source": "winlog.event_data.Source",
                        "SourceAddr": "SourceAddr",
                        "SourceAddress": "SourceAddress",
                        "SourceHostname": "source.domain",
                        "SourceImage": "process.executable",
                        "SourceIp": "source.ip",
                        "SourceIsIpv6": "winlog.event_data.SourceIsIpv6",
                        "SourceName": "winlog.event_data.SourceName",
                        "SourcePort": "source.port",
                        "SourcePort": "winlog.event_data.SourcePort",
                        "SourcePortName": "winlog.event_data.SourcePortName",
                        "SSID": "winlog.event_data.SSID",
                        "StartAddress": "StartAddress",
                        "StartFunction": "StartFunction",
                        "StartModule": "winlog.event_data.StartModule",
                        "StartType": "winlog.event_data.StartType",
                        "Status": "winlog.event_data.Status",
                        "SubjectDomainName": "winlog.event_data.SubjectDomainName",
                        "SubjectLogonId": "winlog.event_data.SubjectLogonId",
                        "SubjectUserName": "winlog.event_data.SubjectUserName",
                        "SubjectUserSid": "winlog.event_data.SubjectUserSid",
                        "SubStatus": "winlog.event_data.SubStatus",
                        "TargetDomainName": "winlog.event_data.TargetDomainName",
                        "TargetFilename": "file.path",
                        "TargetImage": "winlog.event_data.TargetImage",
                        "TargetInfo": "winlog.event_data.TargetInfo",
                        "TargetLogonId": "winlog.event_data.TargetLogonId",
                        "TargetName": "TargetName",
                        "TargetName": "winlog.event_data.TargetName",
                        "TargetObject": "winlog.event_data.TargetObject",
                        "TargetServerName": "winlog.event_data.TargetServerName",
                        "TargetSid": "winlog.event_data.TargetSid",
                        "TargetUserName": "winlog.event_data.TargetUserName",
                        "TargetUserSid": "winlog.event_data.TargetUserSid",
                        "TaskContent": "winlog.event_data.TaskContent",
                        "TaskName": "winlog.event_data.TaskName",
                        "TemplateContent": "winlog.event_data.TemplateContent",
                        "TestSigning": "winlog.event_data.TestSigning",
                        "TicketEncryptionType": "winlog.event_data.TicketEncryptionType",
                        "TicketOptions": "winlog.event_data.TicketOptions",
                        "TransmittedServices": "winlog.event_data.TransmittedServices",
                        "User": "user.name",
                        "UserAccountControl": "winlog.event_data.UserAccountControl",
                        "UserDomain":"winlog.user.domain",
                        "UserID": "winlog.event_data.UserID",
                        "UserName":"user.name",
                        "UserPrincipalName": "winlog.event_data.UserPrincipalName",
                        "Workstation": "winlog.event_data.Workstation",
                        "WorkstationName": "source.domain",
                        "WorkstationName": "winlog.event_data.WorkstationName"
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="windows"),
                ],
            )
        ],
    )

def ecs_azure_activity() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) Azure Activity log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "azure.activitylogs"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="azure", service="activitylogs"),
                ],
            ), 
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "action": "azure.activitylogs.identity.authorization.action",
                        "CategoryValue": "azure.activitylogs.category",
                        "eventName": "azure.activitylogs.EventName",
                        "eventSource": "azure.activitylogs.eventSource",
                        "Operation": "azure.activitylogs.OperationName",
                        "operationName": "azure.activitylogs.operation_name",
                        "OperationNameValue": "azure.activitylogs.operation_name",
                        "PrincipalId": "azure.activitylogs.identity.authorization.evidance.principal_id",
                        "PrincipalType": "azure.activitylogs.identity.authorization.evidance.principal_type",
                        "ResourceId": "azure.resource.id",
                        "ResourceName": "azure.resource.name",
                        "ResourceProviderValue": "azure.activitylogs.resourceProvider",
                        "role": "azure.activitylogs.identity.authorization.evidence.role",
                        "roleAssignmentId": "azure.activitylogs.identity.authorization.evidence.role_assignment_id",
                        "roleAssignmentScope": "azure.activitylogs.identity.authorization.evidence.role_assignment_scope",
                        "roleDefinationId": "azure.activitylogs.identity.authorization.evidence.role_defination_id",
                        "scope": "azure.activitylogs.identity.authorization.scope",
                        "Status": "azure.activitylogs.status",
                        "status": "azure.activitylogs.status"
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="azure", service="activitylogs"),
                ],
            )
        ],
    )

def ecs_azure_signinlogs() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) Azure Signin log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "azure.signinlogs"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="azure", service="signinlogs"),
                ],
            ), 
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "AuthenticationRequirement": "azure.signinlogs.properties.authentication_requirement",
                        "CategoryValue": "azure.signinlogs.category",
                        "ClientApp": "azure.signinlogs.properties.client_app_used",
                        "ConditionalAccessStatus": "azure.signinlogs.properties.conditional_access_status",
                        "conditionalAccessStatus": "azure.signinlogs.properties.conditional_access_status",
                        "DeviceDetail.deviceId": "azure.signinlogs.properties.device_detail.device_id",
                        "DeviceDetail.isCompliant": "azure.signinlogs.properties.device_detail.is_compliant",
                        "DeviceDetail.trusttype": "azure.signinlogs.properties.device_detail.trusttype",
                        "HomeTenantId": "azure.siginlogs.properties.home_tenant_id",
                        "Location": "geo.country_iso_code",
                        "NetworkLocationDetails": "azure.signinlogs.properties.network_location_details",
                        "ResourceDisplayName": "azure.signinlogs.properties.resource_display_name",
                        "ResourceTenantId": "azure.siginlogs.properties.resource_tenant_id",
                        "ResultDescription": "azure.siginlogs.result_description",
                        "resultDescription": "azure.signinlogs.result_description",
                        "Resultdescription": "azure.signinlogs.result_description",
                        "ResultType": "azure.signinlogs.result_type",
                        "RiskState": "azure.signinlogs.properties.risk_state",
                        "Status": "azure.siginlogs.properties.status.status_code",
                        "status": "azure.signinlogs.properties.status.status_code",
                        "UserAgent": "azure.signinlogs.properties.user_agent",
                        "userAgent": "azure.siginlogs.properties.user_agent",
                        "Username": "azure.siginlogs.properties.user_principal_name"
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="azure", service="signinlogs"),
                ],
            )
        ],
    )

def ecs_microsoft_o365() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) Microsoft Office365 log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={"event.dataset": "o365.audit"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="m365"),
                ],
            ), 
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "EventName": "rule.name",
                        "eventName": "rule.name",
                        "EventSource": "event.provider",
                        "eventSource": "event.provider",
                        "ItemType": "o365.audit.ItemType",
                        "itemType": "o365.audit.ItemType",
                        "ObjectId": "o365.audit.ObjectId",
                        "objectId": "o365.audit.ObjectId",
                        "Operation": "o365.audit.Operation",
                        "operation": "o365.audit.Operation",
                        "Status": "o365.audit.Status",
                        "status": "o365.audit.Status",
                        "UserAgent": "o365.audit.UserAgent",
                        "userAgent": "o365.audit.UserAgent",
                        "UserId": "o365.audit.UserId",
                        "userId": "o365.audit.UserId"
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="m365"),
                ],
            )
        ],
    )