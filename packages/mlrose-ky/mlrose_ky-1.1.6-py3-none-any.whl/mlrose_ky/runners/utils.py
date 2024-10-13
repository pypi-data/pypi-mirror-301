"""Utility function to build file paths for experiment data, ensuring directories are created if needed."""

import os


def build_data_filename(
    output_directory: str, runner_name: str, experiment_name: str, df_name: str, x_param: str = "", y_param: str = "", ext: str = ""
) -> str:
    """
    Build and return a data file path, ensuring the directory exists.

    Parameters
    ----------
    output_directory : str
        The root directory where the file will be saved.
    runner_name : str
        The name of the runner.
    experiment_name : str
        The name of the experiment.
    df_name : str
        The name of the data frame or file being saved.
    x_param : str, optional
        An optional parameter to include in the filename, typically representing an X-axis value (default is "").
    y_param : str, optional
        An optional parameter to include in the filename, typically representing a Y-axis value (default is "").
    ext : str, optional
        The file extension to use (e.g., ".csv"). If not provided, the default is an empty string.

    Returns
    -------
    str
        The full file path including the directory, filename, and extension.
    """
    # Ensure the directory exists
    try:
        os.makedirs(os.path.join(output_directory, experiment_name), exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create directory '{os.path.join(output_directory, experiment_name)}': {e}")

    # Sanitize extension and parameters
    if ext and not ext.startswith("."):
        ext = f".{ext}"
    if x_param and not x_param.startswith("_") and not x_param.endswith("_"):
        x_param = f"_{x_param}_"
    if y_param and not y_param.startswith("_") and not y_param.endswith("_"):
        y_param = f"_{y_param}"

    # Build and return the full filename
    filename = f"{runner_name.lower()}__{experiment_name}__{df_name}{x_param}{y_param}{ext}"

    return os.path.join(output_directory, experiment_name, filename)
