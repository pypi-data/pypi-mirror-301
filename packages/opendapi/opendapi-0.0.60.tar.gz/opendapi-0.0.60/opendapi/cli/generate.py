"""Entrypoint for the OpenDAPI CLI `opendapi generate` command."""

# pylint: disable=duplicate-code

import click

from opendapi.cli.common import (
    Schemas,
    get_opendapi_config_from_root,
    pretty_print_errors,
    print_cli_output,
)
from opendapi.cli.options import (
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
    dev_options,
    minimal_schema_options,
)
from opendapi.logging import LogDistKey, Timer
from opendapi.validators.base import MultiValidationError
from opendapi.validators.categories import CategoriesValidator
from opendapi.validators.dapi import DAPI_INTEGRATIONS_VALIDATORS
from opendapi.validators.datastores import DatastoresValidator
from opendapi.validators.subjects import SubjectsValidator
from opendapi.validators.teams import TeamsValidator


@click.command()
@minimal_schema_options
@dev_options
def cli(**kwargs):
    """
    Generate DAPI files for integrations specified in the OpenDAPI configuration file.

    For certain integrations such as DBT and PynamoDB, this command will also run
    additional commands in the respective integration directories to generate DAPI files.
    """
    print_cli_output(
        "Generating DAPI files for your integrations per `opendapi.config.yaml` configuration",
        color="green",
    )
    opendapi_config = get_opendapi_config_from_root(
        local_spec_path=kwargs.get("local_spec_path"), validate_config=True
    )

    minimal_schemas = Schemas(
        teams=TEAMS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        datastores=DATASTORES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        purposes=PURPOSES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        dapi=DAPI_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        subjects=SUBJECTS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        categories=CATEGORIES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
    )

    validators = [
        TeamsValidator,
        DatastoresValidator,
        CategoriesValidator,
        SubjectsValidator,
    ]

    print_cli_output(
        "Identifying your integrations...",
        color="yellow",
    )
    for intg, validator in DAPI_INTEGRATIONS_VALIDATORS.items():
        if opendapi_config.has_integration(intg):
            if validator:
                validators.append(validator)
            print_cli_output(f"  Found {intg}...", color="green")

    print_cli_output(
        "Generating DAPI files for your integrations...",
        color="yellow",
    )
    errors = []
    metrics_tags = {"org_name": opendapi_config.org_name_snakecase}
    with Timer(dist_key=LogDistKey.CLI_GENERATE, tags=metrics_tags):
        for validator in validators:
            inst_validator = validator(
                root_dir=opendapi_config.root_dir,
                enforce_existence=True,
                should_autoupdate=True,
                schema_to_prune_base_template_for_autoupdate=minimal_schemas.minimal_schema_for(
                    validator
                ),
            )

            try:
                inst_validator.run()
            except MultiValidationError as exc:
                errors.append(exc)

    if errors:
        pretty_print_errors(errors)
        # fails with exit code 1 - meaning it blocks merging - but as a ClickException
        # it does not go to sentry, which is appropriate, as this is not an error condition
        raise click.ClickException("Encountered one or more validation errors")

    print_cli_output(
        "Successfully generated DAPI files for your integrations",
        color="green",
    )
