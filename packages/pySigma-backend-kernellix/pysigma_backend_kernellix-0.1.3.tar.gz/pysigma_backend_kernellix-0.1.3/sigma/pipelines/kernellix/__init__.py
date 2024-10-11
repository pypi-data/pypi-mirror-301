from .kernellix import ecs_linux,ecs_cloudtrail,ecs_windows,ecs_web_access,ecs_azure_activity,ecs_azure_signinlogs,ecs_microsoft_o365
# TODO: add all pipelines that should be exposed to the user of your backend in the import statement above.

pipelines = {
    "kernellix_linux": ecs_linux,
    "kernellix_cloudtrail": ecs_cloudtrail,
    "kernellix_windows": ecs_windows,
    "kernellix_web_access": ecs_web_access,
    "kernellix_azure_activity": ecs_azure_activity,
    "kernellix_azure_signinlogs": ecs_azure_signinlogs,
    "kernellix_microsoft_signinlogs": ecs_microsoft_o365
}