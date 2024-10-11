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

def ecs_linux() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="Elastic Common Schema (ECS) linux log mappings",
        priority=30,
        items=[
            ProcessingItem(
                identifier="index_condition",
                transformation=AddConditionTransformation(
                    conditions={".event.dataset": "linux"}, template=False
                ),
                rule_conditions=[
                    LogsourceCondition(product="linux"),
                ],
            ),
            ProcessingItem(
                identifier="field_mapping",
                transformation=FieldMappingTransformation(
                    mapping={
                        "CommandLine": "process.command_line",
                        "Image": "process.executable",
                        "ParentCommandLine": "process.parent.command_line",
                        "ParentImage": "process.parent.executable",
                    }
                ),
                rule_conditions=[
                    LogsourceCondition(product="linux"),
                ],
            )
        ],
    )