import logging

import pandas as pd
from django.db import IntegrityError
from django.utils.text import slugify
from services.models import (
    Division,
    FunderPolicy,
    ResearchLifecyclePhase,
    ResearchLifecyclePhaseAddition,
    ServiceCategory,
    ServiceCategoryAddition,
    ServicePage,
    ServicePageDivisionAddition,
    ServicesListingPage,
)


def get_values_from_columns(path, sheet_name, *columns, dropna=True):
    """Extracts values from specified columns for each row in a specified sheet of an Excel file.

    This function reads an Excel file specified by the given path,
    accesses the specified sheet, and retrieves the values from the
    specified columns for each row. If any column does not exist
    or if the file cannot be found, appropriate error messages are printed.

    Args:
        path (str): The file path to the Excel file.
        sheet_name (str): The name of the sheet to read from.
        *columns (str): The names of the columns to extract.

    Returns:
        list: A list of tuples, where each tuple contains the values
              from the specified columns for each row.

    Raises:
        ValueError: If any specified column does not exist in the specified sheet.
        FileNotFoundError: If the specified file does not exist.
        Exception: For any other errors that may occur during file reading.
    """
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)

        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(
                f"The following columns do not exist in the '{sheet_name}' sheet: {', '.join(missing_columns)}"
            )

        # Use sets to remove duplicates
        if dropna is False:
            return list(set(tuple(row) for row in df[list(columns)].values))
        return list(set(tuple(row) for row in df[list(columns)].dropna().values))

    except FileNotFoundError:
        print(f"The file at {path} was not found.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")


def populate_research_lifecycle_phases_from_xlsx(spreadsheet):
    """
    Populate the ResearchLifecyclePhase model with data from an Excel spreadsheet.

    This function retrieves values from the specified column ('Phase')
    in the 'UTILS' sheet of the provided Excel spreadsheet. For each value
    retrieved, it creates a new instance of the ResearchLifecyclePhase model
    and saves it to the database.

    Args:
        spreadsheet (str): The path to the Excel spreadsheet.

    Returns:
        int: The number of ResearchLifecyclePhase instances created.

    Raises:
        ValueError: If the spreadsheet is not formatted correctly or if
        there are issues during the save process.
    """
    try:
        values = get_values_from_columns(spreadsheet, 'UTILS', 'Phase')
        phases = []

        for val in values:
            if val:
                name = val[0]
                slug = slugify(name)
                phases.append(ResearchLifecyclePhase(name=name, slug=slug))

        if phases:
            ResearchLifecyclePhase.objects.bulk_create(phases)
            logging.info(
                f"Successfully created {len(phases)} ResearchLifecyclePhase instances."
            )
        else:
            logging.warning("No valid 'Phase' values found in the spreadsheet.")

        return len(phases)

    except IntegrityError as e:
        logging.error(f"Database error occurred: {e}")
        raise ValueError("An error occurred while saving to the database.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise ValueError(
            "An unexpected error occurred while processing the spreadsheet."
        )


def populate_categories_from_xlsx(spreadsheet):
    """
    Populate the ServiceCategory model with data from an Excel spreadsheet.

    This function retrieves values from the specified column ('Sub-Phase')
    in the 'UTILS' sheet of the provided Excel spreadsheet. For each value
    retrieved, it creates a new instance of the ServiceCategory model
    and saves it to the database.

    Args:
        spreadsheet (str): The path to the Excel spreadsheet.

    Returns:
        int: The number of ServiceCategory instances created.

    Raises:
        ValueError: If the spreadsheet is not formatted correctly or if
        there are issues during the save process.
    """
    try:
        values = get_values_from_columns(spreadsheet, 'UTILS', 'Sub-Phase')
        phases = []

        for val in values:
            if val:
                name = val[0]
                slug = slugify(name)
                phases.append(ServiceCategory(name=name, slug=slug))

        if phases:
            ServiceCategory.objects.bulk_create(phases)
            logging.info(
                f"Successfully created {len(phases)} ServiceCategory instances."
            )
        else:
            logging.warning("No valid 'Sub-Phase' values found in the spreadsheet.")

        return len(phases)

    except IntegrityError as e:
        logging.error(f"Database error occurred: {e}")
        raise ValueError("An error occurred while saving to the database.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise ValueError(
            "An unexpected error occurred while processing the spreadsheet."
        )


def populate_funder_policies_from_xlsx(spreadsheet):
    """
    Populate the FunderPolicy model with data from an Excel spreadsheet.

    This function retrieves values from the specified columns
    ('Research Data Funder Policies' and 'URL') in the 'Funder Policies'
    sheet of the provided Excel spreadsheet. For each value retrieved,
    it creates a new instance of the FunderPolicy model and saves it to
    the database.

    Args:
        spreadsheet (str): The path to the Excel spreadsheet.

    Returns:
        int: The number of ServiceCategory instances created.

    Raises:
        ValueError: If the spreadsheet is not formatted correctly or if
        there are issues during the save process.
    """
    try:
        values = get_values_from_columns(
            spreadsheet, 'Funder Policies', 'Research Data Funder Policies', 'URL'
        )
        policies = []

        for val in values:
            if val:
                name = val[0]
                url = val[1]
                slug = slugify(name)
                policies.append(FunderPolicy(name=name, url=url, slug=slug))

        if policies:
            FunderPolicy.objects.bulk_create(policies)
            logging.info(
                f"Successfully created {len(policies)} FunderPolicy instances."
            )
        else:
            logging.warning("No valid values found in the spreadsheet.")

        return len(policies)

    except IntegrityError as e:
        logging.error(f"Database error occurred: {e}")
        raise ValueError("An error occurred while saving to the database.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise ValueError(
            "An unexpected error occurred while processing the spreadsheet."
        )


def populate_divisions_from_xlsx(spreadsheet):
    """
    Populate the Division model with data from an Excel spreadsheet.

    This function retrieves values from the specified columns
    ('Division' and 'URL') in the 'Divisions' sheet of the provided
    Excel spreadsheet. For each value retrieved, it creates a new
    instance of the Division model and saves it to the database.

    Args:
        spreadsheet (str): The path to the Excel spreadsheet.

    Returns:
        int: The number of ServiceCategory instances created.

    Raises:
        ValueError: If the spreadsheet is not formatted correctly or if
        there are issues during the save process.
    """
    try:
        values = get_values_from_columns(spreadsheet, 'Divisions', 'Division', 'URL')
        divisions = []

        for val in values:
            if val:
                name = val[0]
                url = val[1]
                slug = slugify(name)
                divisions.append(Division(name=name, url=url, slug=slug))

        if divisions:
            Division.objects.bulk_create(divisions)
            logging.info(f"Successfully created {len(divisions)} Division instances.")
        else:
            logging.warning("No valid values found in the spreadsheet.")

        return len(divisions)

    except IntegrityError as e:
        logging.error(f"Database error occurred: {e}")
        raise ValueError("An error occurred while saving to the database.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise ValueError(
            "An unexpected error occurred while processing the spreadsheet."
        )


def add_snippet(text, snippet_model, snippet_through_table, attribute, child):
    """
    Adds snippets to a ServicePage object from a comma-separated string of snippet
    names.

    Args:
        text (str): Comma-separated snippet names.
        snippet_model (Model): Model class to retrieve snippet objects.
        snippet_through_table (Model): Model class for the through table.
        attribute (str): Attribute in the through table to set to the snippet.
        child (ServicePage instance): Child object to associate snippets with.

    Returns:
        None: Modifies the database by saving new associations.
    """
    if not pd.isna(text):
        data_list = text.split(',')
        for data in data_list:
            snippet = snippet_model.objects.get(name=data.strip())
            snippet_addition = snippet_through_table(page=child)
            snippet_addition.__setattr__(attribute, snippet)
            snippet_addition.save()


def populate_service_pages_from_xlsx(spreadsheet):
    """
    Populates service pages from an Excel spreadsheet.

    Args:
        spreadsheet (str): Path to the Excel spreadsheet.

    Returns:
        int: The number of service pages created.
    """
    values = get_values_from_columns(
        spreadsheet,
        'data_services',
        'Name (text)',
        'URL (URL)',
        'Description (paragraph)',
        'Research Lifecycle Phase (text)',
        'Category/Sub-Phase (text) R (tags)',
        'Division (text) R',
        dropna=False,
    )
    parent = ServicesListingPage.objects.first()
    count = 0
    for row in values:
        title = row[0]
        slug = slugify(row[0])
        url = row[1]
        body_txt = row[2]
        lifecycle_phase_txt = row[3]
        categories_txt = row[4]
        divisions_txt = row[5]

        if not pd.isna(title) and not pd.isna(body_txt):
            child = ServicePage(
                title=title,
                slug=slug,
                body=[('paragraph', body_txt)],
            )
            if not pd.isna(url):
                child.service_url = url
            parent.add_child(instance=child)
            child.save()
            count += 1

            add_snippet(
                lifecycle_phase_txt,
                ResearchLifecyclePhase,
                ResearchLifecyclePhaseAddition,
                'phase',
                child,
            )
            add_snippet(
                categories_txt,
                ServiceCategory,
                ServiceCategoryAddition,
                'category',
                child,
            )
            add_snippet(
                divisions_txt, Division, ServicePageDivisionAddition, 'division', child
            )

    return count
