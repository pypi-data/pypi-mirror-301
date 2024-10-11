import os
import torch
import torch.nn as nn
import zipfile
import subprocess

from transformers import AutoTokenizer, AutoModel
import teradataml as tdml
from teradataml.context.context import _get_database_username, _get_current_databasename, _get_context_temp_databasename
import pandas as pd
import time

import tdstone2.tdstone
from tdstone2 import logger

import os
import sys
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch.nn as nn
import logging
import onnx
import onnxruntime as rt
from onnxruntime.tools.onnx_model_utils import make_dim_param_fixed
import pandas as pd
# Set up logging
logger = logging.getLogger(__name__)


def save_tokenizer_and_embeddings_model_onnx_old2(model_name: str, local_dir: str, device: str = "cpu"):
    """
    Downloads and saves the tokenizer and full transformer model of the specified SentenceTransformer.
    Exports and optimizes the full transformer model to an ONNX file using a tokenized dummy sentence.

    Args:
        model_name (str): The name of the pre-trained SentenceTransformer model to download.
        local_dir (str): The directory where the tokenizer and full transformer model will be saved.
        device (str): The device to move the model and inputs to ('cpu' or 'cuda').
    """
    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        logger.info(f"Created directory: {local_dir}")

    # Download and save the tokenizer locally
    logger.info(f"Downloading tokenizer for model: {model_name}")
    model = SentenceTransformer(model_name)
    tokenizer = model.tokenizer
    tokenizer.save_pretrained(local_dir)
    logger.info(f"Tokenizer saved in {local_dir}")

    # Extract the full transformer model (not just the embeddings layer)
    full_model = model._first_module().auto_model.to(device)  # Move model to the correct device
    logger.info(f"Extracted full transformer model from: {model_name}")

    # Tokenize a dummy sentence to use in ONNX export
    dummy_sentence = "This is a dummy sentence for testing."
    tokenized_output = tokenizer(dummy_sentence, return_tensors="pt", padding=True, truncation=True, max_length=256)

    # Move the tokenized input to the same device as the model
    for key in tokenized_output:
        tokenized_output[key] = tokenized_output[key].to(device).to(torch.int64)

    # Export the full transformer model to ONNX
    onnx_path = os.path.join(local_dir, "full_model.onnx")
    torch.onnx.export(
        full_model,  # The full transformer model to export
        tuple(tokenized_output.values()),  # Tokenized output as input
        onnx_path,  # Where to save the ONNX model
        input_names=list(tokenized_output.keys()),  # Use the actual keys from tokenized_output
        output_names=['last_hidden_state', 'pooler_output'],  # Output name in the graph (for token embeddings)
        dynamic_axes={key: {0: "batch_size", 1: "sequence_length"} for key in tokenized_output.keys()},  # Dynamic axes for all inputs
        opset_version=15,  # ONNX opset version
        do_constant_folding=True
    )

    logger.info(f"Full transformer model exported and saved in ONNX format at {onnx_path}")


def make_dim_param_fixed(graph, dim_name, fixed_value):
    """Utility function to fix dynamic dimension sizes."""
    for dim_param in graph.input:
        for dim in dim_param.type.tensor_type.shape.dim:
            if dim.dim_param == dim_name:
                dim.dim_value = fixed_value


def save_tokenizer_and_embeddings_model_onnx(model_name: str,  local_dir: str, model_task: None, device: str = "cpu",
                                             opset_version: int = 16):
    """
    Downloads and saves the tokenizer, exports the full transformer model using optimum-cli,
    and refines the exported ONNX model by fixing dynamic dimensions and removing unnecessary outputs.

    Args:
        model_name (str): The name of the pre-trained SentenceTransformer model to download.
        local_dir (str): The directory where the tokenizer and full transformer model will be saved.
        device (str): The device to move the model and inputs to ('cpu' or 'cuda').
        opset_version (int): The ONNX opset version to use for the export.
    """
    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        logger.info(f"Created directory: {local_dir}")

    # Step 1: Download and save the tokenizer locally
    logger.info(f"Downloading tokenizer for model: {model_name}")
    model = SentenceTransformer(model_name)
    tokenizer = model.tokenizer
    tokenizer.save_pretrained(local_dir)
    logger.info(f"Tokenizer saved in {local_dir}")

    # Step 2: Run the optimum-cli export command as a system command
    logger.info(f"Running optimum-cli export command for model: {model_name}")
    if model_task is None:
        command = f"optimum-cli export onnx --opset {opset_version} --trust-remote-code -m {model_name} {local_dir.replace('\\', '/')}"
    else:
        command = f"optimum-cli export onnx --task {model_task} --opset {opset_version} --trust-remote-code -m {model_name} {local_dir.replace('\\','/')}"
    logger.info(f"optimum-cli command: {command}")
    # Use os.system to execute the command
    exit_code = os.system(command)

    # Check if the system command was successful
    if exit_code != 0:
        print(f"Error: optimum-cli command failed with exit code {exit_code}")
        sys.exit(exit_code)

    logger.info(f"Model exported successfully to {local_dir}")

    # Step 3: Load the exported ONNX model
    onnx_model_path = os.path.join(local_dir, "model.onnx")
    model = onnx.load(onnx_model_path)

    # Step 4: Refine the ONNX model (fix dimensions, remove outputs)
    logger.info("Refining the ONNX model...")

    # Set the opset version for the refined model
    op = onnx.OperatorSetIdProto()
    op.version = opset_version
    refined_model = onnx.helper.make_model(model.graph, ir_version=8, opset_imports=[op])

    # Fix dynamic dimension sizes (batch_size, sequence_length)
    make_dim_param_fixed(refined_model.graph, "batch_size", 1)  # Fix batch size to 1
    make_dim_param_fixed(refined_model.graph, "sequence_length", 512)  # Fix sequence length to 512

    # Remove 'token_embeddings' output from the model graph
    for node in list(refined_model.graph.output):
        if node.name == "token_embeddings":
            refined_model.graph.output.remove(node)

    # Step 5: Save the refined ONNX model
    refined_onnx_model_path = os.path.join(local_dir, "full_model.onnx")
    onnx.save(refined_model, refined_onnx_model_path)

    logger.info(f"Refined ONNX model saved at {refined_onnx_model_path}")

    os.remove(os.path.join(local_dir, "model.onnx"))
    logger.info(f"Suboptimal ONNX model {onnx_model_path} removed")

    return

def save_tokenizer_and_embeddings_model_onnx_old(model_name: str, local_dir: str):
    """
    Downloads and saves the tokenizer and only the embeddings layer of the specified model.
    Exports and optimizes the embeddings model to an ONNX file.

    Args:
        model_name (str): The name of the pre-trained model to download.
        local_dir (str): The directory where the tokenizer and embeddings model will be saved.
    """
    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        logger.info(f"Created directory: {local_dir}")

    # Download and save the tokenizer locally
    logger.info(f"Downloading tokenizer for model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(local_dir)

    # Download the model locally
    logger.info(f"Downloading model: {model_name}")
    model = AutoModel.from_pretrained(model_name)

    # Extract only the embeddings layer
    embeddings_model = nn.Sequential(model.embeddings)
    logger.info(f"Extracted embeddings layer from model: {model_name}")

    # Ensure tensors are contiguous before saving
    for param in embeddings_model.parameters():
        if not param.is_contiguous():
            param.data = param.data.contiguous()

    # Create dummy input for export (batch size 1, sequence length 256 for example)
    dummy_input = torch.randint(0, tokenizer.vocab_size, (1, 256), dtype=torch.int32)

    # Export the embeddings model to ONNX
    onnx_path = os.path.join(local_dir, "embeddings_model.onnx")
    torch.onnx.export(
        embeddings_model,  # The model to export
        dummy_input,  # Dummy input tensor
        onnx_path,  # Where to save the ONNX model
        input_names=["input_ids"],  # Input name in the graph
        output_names=["embedding"],  # Output name in the graph
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "embedding": {0: "batch_size", 1: "sequence_length"}
        },  # Handle dynamic batch and sequence lengths
        opset_version=13,  # ONNX opset version
        do_constant_folding=True
    )

    logger.info(f"Embeddings model exported and saved in ONNX format at {onnx_path}")


def zip_saved_files(model_name: str, local_dir: str) -> str:
    """
    Zips the saved tokenizer and embeddings model using the specified model_name.
    The model_name will have '/' replaced with '_' to create a valid filename.
    The zip file will be placed in a dedicated 'models' folder to avoid issues with the source folder.

    Args:
        model_name (str): The name of the model whose files are being zipped.
        local_dir (str): The directory where the tokenizer and embeddings model files are located.

    Returns:
        str: The path to the created zip file in the 'models' directory.
    """
    # Replace '/' with '_' in the model name for valid file naming
    valid_model_name = model_name.replace("/", "_").replace(".", "_")

    # Create a dedicated models folder if it doesn't exist
    models_dir = os.path.join(".", "models")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        logger.info(f"Created models directory at {models_dir}")

    # Path for the zip file in the models folder
    zip_path = os.path.join(models_dir, f"tdstone2_emb_{valid_model_name}.zip")

    # Zip the contents of the local_dir and place the zip in the models folder
    logger.info(f"Zipping files in directory: {local_dir} to {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(local_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Add each file to the zip, maintaining the directory structure relative to local_dir
                zipf.write(file_path, os.path.relpath(file_path, local_dir))

    logger.info(f"Files have been zipped to {zip_path}")
    return zip_path


def get_tokenizer_and_embeddings_model_zip(model_name: str, local_dir: str, model_task: str = None) -> str:
    """
    Downloads the tokenizer and embeddings layer of the specified model, saves them locally,
    exports the embeddings layer to ONNX format, and zips the saved files into a single archive.

    Args:
        model_name (str): The name of the pre-trained model to download.
        local_dir (str): The directory where the tokenizer, embeddings model, and ONNX files will be saved.

    Returns:
        str: The path to the created zip file containing the tokenizer and ONNX model files.
    """
    # Save the tokenizer and embeddings model in ONNX format
    logger.info(f"Saving tokenizer and embeddings model for: {model_name}")
    save_tokenizer_and_embeddings_model_onnx(model_name,  local_dir, model_task)

    # Zip the saved files and return the zip file path
    zip_file_path = zip_saved_files(model_name, local_dir)

    return zip_file_path


def install_zip_in_vantage(zip_file_path: str, database: str, replace = False):
    """
    Installs the specified zip file into Teradata Vantage after setting the session parameters.

    Args:
        zip_file_path (str): The full path to the zip file, including the filename and .zip extension.
        database (str): The database where the file will be installed.

    Returns:
        None
    """
    # Extract the file name without the zip extension
    file_name = os.path.basename(zip_file_path).replace(".zip", "").replace('-', '_')

    # Set session parameters to point to the correct database
    logger.info(f"Setting session parameters for database: {database}")
    tdml.execute_sql(f"SET SESSION SEARCHUIFDBPATH = {database};")
    tdml.execute_sql(f'DATABASE "{database}";')

    # Install the zip file in Teradata Vantage
    logger.info(f"Installing zip file: {zip_file_path} in database: {database}")
    try:
        logger.info(f"Zip file {zip_file_path} installation to {database} database started ({file_name})")
        tdml.install_file(
            replace = replace,
            file_identifier=file_name,  # Filename without the zip extension
            file_path=zip_file_path,  # Full path to the zip file with .zip extension
            file_on_client=True,  # Indicates the file is located on the client machine
            is_binary=True  # Specifies that the file is binary
        )
        logger.info(f"Zip file {zip_file_path} has been installed in the {database} database.")

    except Exception as e:
        # Log error details and the file info
        logger.error(
            f"Failed to install the zip file: {zip_file_path} (file_name: {file_name}) in database: {database}. Error: {str(e)}")
    logger.info(f"Zip file {zip_file_path} has been installed in the {database} database.")


def install_model_in_vantage_from_name(
        model_name: str,
        local_dir: str = None,
        model_task: str = None,
        database: str = None,
        replace = False
):
    """
    Downloads the tokenizer and embeddings layer of the specified model, saves them as a zip file,
    and installs the zip file in Teradata Vantage. It ensures that the database context is restored
    to its original state after the installation.

    Args:
        model_name (str): The name of the pre-trained model to download.
        local_dir (str, optional): The directory where the tokenizer, embeddings model, and zip file will be saved. Defaults to './models/{model_name}'.
        database (str, optional): The database where the zip file will be installed in Teradata Vantage. Defaults to the current or temporary database in the context.

    Returns:
        None
    """

    # Set default local_dir if not provided, replacing '/' in model_name with '_'
    if local_dir is None:
        valid_model_name = model_name.replace("/", "_")
        local_dir = os.path.join(".", "models", valid_model_name)
        logger.info(f"Local directory for model files set to: {local_dir}")

    # Get the current database to reset later
    original_database = _get_current_databasename()

    # Set default database if not provided
    if database is None:
        database = original_database
        logger.info(f"Using default database: {database}")

    # Step 1: Get the zip file by saving the tokenizer and embeddings model to the local directory
    zip_file_path = get_tokenizer_and_embeddings_model_zip(model_name, local_dir, model_task)

    # Step 2: Install the zip file in Teradata Vantage
    try:
        install_zip_in_vantage(zip_file_path, database, replace = replace)
    finally:
        # Reset the database to the original one after installation
        if original_database:
            tdml.execute_sql(f'DATABASE "{original_database}";')
            logger.info(f"Database context has been reset to {original_database}.")
        else:
            logger.warning("No original database context was found to reset.")

    logger.info(f"Model {model_name} has been successfully installed in the {database} database.")


def list_installed_files(database: str = None, startswith: str = 'tdstone2_emb_', endswith: str = '.zip'):
    """
    Lists all installed files in the specified database that start with the specified prefix and end with the specified suffix.

    Args:
        database (str, optional): The database where the files are installed. If not provided, defaults to the current or temporary database.
        startswith (str, optional): The prefix for filtering filenames. Defaults to 'tdstone2_emb_'.
        endswith (str, optional): The suffix for filtering filenames. Defaults to '.zip'.

    Returns:
        DataFrame: A Teradata DataFrame containing the list of matching files in the specified database.
    """

    # Set default database if not provided
    if database is None:
        database = _get_current_databasename()
        logger.info(f"Using default database: {database}")
    else:
        logger.info(f"Using provided database: {database}")

    # Ensure that session search path is set to the correct database
    tdml.execute_sql(f"SET SESSION SEARCHUIFDBPATH = {database};")
    logger.info(f"Session search path set to database: {database}")

    # Prepare the query to list installed files
    query = f"""
    SELECT DISTINCT
      '{database}' as DATABASE_LOCATION,
      res as tdstone2_models
    FROM
        Script(
            SCRIPT_COMMAND(
                'ls {database.upper()}' 
            )
            RETURNS(
                'res varchar(1024)'
            )
        ) AS d
    WHERE lower(res) LIKE '{startswith.lower()}%{endswith.lower()}'
    """

    logger.info(
        f"Executing query to list installed files starting with '{startswith}' and ending with '{endswith}' in database {database}")

    # Execute the query and return the result as a DataFrame
    result = pd.read_sql(query, con=tdml.get_context())
    logger.info(f"Query executed successfully, returning result")

    return result


def setup_and_execute_script(model: str, dataset, text_column, hash_columns: list, accumulate_columns=[],
                             delimiter: str = '\t', database: str = None, data_hash_column: str = 'Problem_Type'):
    """
    Set up the Teradata session, unzip the model, and execute the script via tdml.
    If no database is provided, the default one will be used. After execution, the original default database is restored.

    Args:
        model (str): The model file to be unzipped and used.
        dataset: The dataset used in the tdml.Script.
        delimiter (str): The delimiter used in the script for data splitting (default is tab-delimited '\t').
        database (str, optional): The database to set the session for and work with (uses default if not provided).
        data_hash_column (str, optional): The column name for the data hash (default is 'Problem_Type').

    Returns:
        sto (tdml.Script): The tdml.Script object configured and executed.
    """

    text_column_position, hash_columns_positions, accumulate_positions = get_column_positions(dataset, text_column,
                                                                                              hash_columns,
                                                                                              accumulate_columns)

    sqlalchemy_types = dataset._td_column_names_and_sqlalchemy_types

    # Get the current database before changing the session
    previous_database = _get_current_databasename()

    # Set default database if not provided
    if database is None:
        database = _get_current_databasename()
        logger.info(f"Using default database: {database}")
    else:
        logger.info(f"Using provided database: {database}")

    try:
        # Set the Teradata session and database path
        tdml.execute_sql(f"SET SESSION SEARCHUIFDBPATH = {database};")
        tdml.execute_sql(f'DATABASE "{database}";')

        # Generate the unzip and execution command
        model_folder = model.split('.')[0]
        command = f"""unzip {database}/{model} -d $PWD/{model_folder}/ > /dev/null && tdpython3 ./{database}/tds_vector_embedding.py {model_folder} {text_column_position} {accumulate_positions} {delimiter}"""
        logger.info(f"bash command : {command}")
        # Create the tdml.Script object
        sto = tdml.Script(
            data=dataset,
            script_name='tds_vector_embedding.py',
            files_local_path='.',
            script_command=command,
            data_hash_column=hash_columns,  # Use provided data_hash_column or default 'Problem_Type'
            is_local_order=False,
            returns=tdml.OrderedDict(
                [(c, sqlalchemy_types[c.lower()]) for c in accumulate_columns] +
                [
                    ("jobid", tdml.VARCHAR(length=36, charset='latin')),
                    ("process_time", tdml.FLOAT()),
                    ("elapsed_time", tdml.FLOAT())
                ] +
                [
                    (text_column, sqlalchemy_types[text_column.lower()]),
                    ("Vector_Dimension", tdml.INTEGER()),
                    ("V", tdml.FLOAT()),
                    ("Model", tdml.VARCHAR(length=1024, charset='latin'))
                ]
            )
        )

        return sto

    finally:
        # Restore the previous database after execution
        tdml.execute_sql(f'DATABASE "{previous_database}";')
        logger.info(f"Restored previous database: {previous_database}")


def execute_and_create_pivot_view(sto, schema_name: str, table_name: str, hash_columns = None, if_exists='replace'):
    """
    Execute the given tdml.Script, save the results to a SQL table, and create a pivot view.

    Args:
        sto (tdml.Script): The tdml.Script object to execute.
        schema_name (str): The name of the schema where the table and view will be created.
        table_name (str): The name of the table to store the results.

    Returns:
        tdml.DataFrame: A DataFrame of the created pivot view.
    """

    from teradataml.context.context import _get_database_username

    logger.info("Starting script execution and SQL table creation.")

    # Measure the execution time
    tic = time.time()

    # Execute the script and store the result in a SQL table
    try:
        df_sto = sto.execute_script()
    except Exception as e:
        tac = time.time()
        logger.info(f"Script query construction. Construction time: {tac - tic:.2f} seconds")
        raise


    tac = time.time()
    logger.info(f"Script query construction. Construction time: {tac - tic:.2f} seconds")

    # Measure the execution time
    tic = time.time()
    # Execute the script and store the result in a SQL table
    try:
        df_sto.to_sql(
            schema_name=schema_name,
            table_name='TV_' + table_name,
            if_exists=if_exists,
            temporary=True
        )
        df_sto = tdml.DataFrame(tdml.in_schema(_get_database_username(), 'TV_' + table_name))
    except Exception as e:
        tac = time.time()
        logger.info(f"Script execution and storage in volatile table. Computation time: {tac - tic:.2f} seconds")
        raise

    tac = time.time()
    logger.info(f"Script execution and storage in volatile table. Computation time: {tac - tic:.2f} seconds")

    # Measure the storage time
    tic = time.time()
    try:
        if hash_columns is None:
            df_sto.to_sql(
                schema_name   = schema_name,
                table_name    = 'T_' + table_name,
                if_exists     = if_exists,
                temporary     = True
            )
        else:
            df_sto.to_sql(
                schema_name   = schema_name,
                table_name    = 'T_' + table_name,
                if_exists     = if_exists,
                primary_index = hash_columns
            )
    except Exception as e:
        tac = time.time()
        logger.info(f"Data stored in T_{table_name}. Storage time: {tac - tic:.2f} seconds")
        raise

    tac = time.time()
    logger.info(f"Data stored in T_{table_name}. Storage time: {tac - tic:.2f} seconds")

    # Compute vector_dimension from the stored table
    vector_dimension_query = f"SEL max(Vector_Dimension) + 1 FROM {schema_name}.T_{table_name}"
    vector_dimension = tdml.execute_sql(vector_dimension_query).fetchall()[0][0]
    logger.info(f"Computed vector dimension: {vector_dimension}")

    # Generate the pivot columns for the view using the computed vector_dimension
    columns = '\n,'.join([f"'{i}' AS V_{i}" for i in range(vector_dimension)])

    # Create a PIVOT view
    query = f"""
    REPLACE VIEW {schema_name}.{table_name} AS
    LOCK ROW FOR ACCESS
    SELECT * 
    FROM {schema_name}.T_{table_name}
    PIVOT (sum("V") FOR (Vector_Dimension) IN (
    {columns}
    )) Tmp
    """

    # Execute the SQL query to create the pivot view
    logger.info(f"Creating pivot view {table_name}.")
    tdml.execute_sql(query)

    logger.info(f"Pivot view {table_name} created successfully.")

    # Return the DataFrame of the created view
    return tdml.DataFrame(tdml.in_schema(schema_name, table_name))


def get_column_positions(dataset, text_column: str, hash_columns: list, accumulate: list):
    """
    Get the positions of the text_column, hash_columns, and accumulate columns in the dataset.
    Ensure that there is no overlap between the sets of indices.

    Args:
        dataset: A Teradata DataFrame.
        text_column (str): The name of the text column.
        hash_columns (list): A list of column names to hash.
        accumulate (list): A list of column names to accumulate.

    Returns:
        tuple: The position of text_column, list of positions of hash_columns, and list of positions of accumulate columns.

    Raises:
        ValueError: If there is an overlap in the column indices between the three sets.
    """
    # Get the list of columns from the dataset
    dataset_columns = list(dataset.columns)

    # Get the position of text_column
    try:
        text_column_position = dataset_columns.index(text_column)
    except ValueError:
        raise ValueError(f"'{text_column}' not found in the dataset columns.")

    # Get the positions of hash_columns
    try:
        hash_columns_positions = [dataset_columns.index(col) for col in hash_columns]
    except ValueError as e:
        raise ValueError(f"One or more hash_columns not found in the dataset: {e}")

    # Get the positions of accumulate columns
    try:
        accumulate_positions = [dataset_columns.index(col) for col in accumulate]
    except ValueError as e:
        raise ValueError(f"One or more accumulate columns not found in the dataset: {e}")

    # Ensure no overlap between the three sets of column indices
    all_positions = set([text_column_position]) | set(accumulate_positions)
    if len(all_positions) != 1 + len(accumulate_positions):
        raise ValueError("There is an overlap in the column indices between text_column, hash_columns, and accumulate.")

    # Return the positions
    return text_column_position, hash_columns_positions, accumulate_positions


def compute_vector_embedding(model, dataset, schema_name, table_name, text_column, hash_columns, accumulate_columns=[]):
    """
    Set up and execute a script for the given model and dataset, ensuring that the text column is VARCHAR
    and the model exists. Finally, create a pivot view of the results.

    Args:
        model (str): The name of the model file.
        dataset: A Teradata DataFrame.
        schema_name (str): The schema name where the table and view will be created.
        table_name (str): The name of the table to store the results.
        text_column (str): The name of the text column.
        hash_columns (list): A list of columns to hash.
        accumulate_columns (list): A list of columns to accumulate.

    Returns:
        tdml.DataFrame: A DataFrame of the created pivot view.

    Raises:
        ValueError: If the text_column is not of type VARCHAR or the model is not found.
    """
    from sqlalchemy.sql.sqltypes import VARCHAR
    # Initial logger message explaining the function's purpose
    logger.info(f"Starting computation of vector embedding for the text in '{text_column}' using model '{model}'. "
                f"The computation will be distributed across the hash columns {hash_columns}, "
                f"and the results will be stored in the '{schema_name}' schema. "
                f"Results will be saved in the table 'T_{table_name}' and accessible through the pivoted view '{table_name}'."
                )
    if len(accumulate_columns)>0:
        logger.info(f"{accumulate_columns} will be included in the result set.")
    logger.info("Starting the process of script execution and view creation.")

    # Check if the text_column is a VARCHAR in the dataset
    column_types = dataset._td_column_names_and_sqlalchemy_types
    logger.info(f"Checking if the column '{text_column}' is of type VARCHAR.")

    if text_column.lower() not in column_types or not isinstance(column_types[text_column.lower()], VARCHAR):
        logger.error(f"The column '{text_column}' is not of type VARCHAR.")
        raise ValueError(f"The column '{text_column}' must be of type VARCHAR.")
    else:
        logger.info(f"Column '{text_column}' is valid and of type VARCHAR.")

    # Check if the model exists in the installed models
    logger.info(f"Checking if the model '{model}' exists in the installed models.")
    installed_models_df = list_installed_files()

    if not any(installed_models_df['tdstone2_models'].str.contains(model)):
        logger.error(f"Model '{model}' not found in the installed models.")
        raise ValueError(f"Model '{model}' not found in the installed models.")
    else:
        logger.info(f"Model '{model}' found in the installed models.")

    # If the checks pass, set up and execute the script
    logger.info("Setting up and executing the script.")
    sto = setup_and_execute_script(
        model=model,
        dataset=dataset,
        text_column=text_column,
        hash_columns=hash_columns,
        accumulate_columns=accumulate_columns
    )
    logger.info("Script setup and execution completed.")

    # Execute and create the pivot view
    logger.info(f"Creating pivot view for schema '{schema_name}' and table '{table_name}'.")
    res = execute_and_create_pivot_view(sto, schema_name, table_name, hash_columns = hash_columns)
    logger.info(f"Pivot view created successfully for table '{table_name}' in schema '{schema_name}'.")

    return res


def get_tdstone2_data_script_path():
    """
    Dynamically find the path of the 'tds_vector_embedding.py' script in the tdstone2 package.
    This works for editable mode installations (pip install -e).
    """
    return os.path.join(tdstone2.tdstone.this_dir, "data", "tds_vector_embedding.py")


def run_tds_vector_embedding_script_locally(df, zip_file_path, text_column, accumulate_columns):
    """
    Runs the 'tds_vector_embedding.py' script in the data module of the 'tdstone2' package
    by passing a dataframe via stdin and the required arguments.

    Args:
        df (pd.DataFrame): The dataframe to process.
        zip_file_path (str): The path to the zip file.
        text_column (int): The index of the text column in the dataframe.
        accumulate_columns (list): The list of column indexes to accumulate and print.

    Returns:
        pd.DataFrame: The resulting output from stdout as a pandas DataFrame.
    """
    logger.info("Starting the vector embedding script.")

    # Convert the dataframe to the expected input format (tab-delimited)
    input_data = df.apply(lambda row: '\t'.join(map(str, row.values)), axis=1).str.cat(sep='\n')
    logger.info("Dataframe converted to tab-delimited format.")

    # Get column positions
    text_column_, _, accumulate_columns_ = get_column_positions(df, accumulate=accumulate_columns, hash_columns='',
                                                                text_column=text_column)
    logger.info(f"Text column: {text_column_}, Accumulate columns: {accumulate_columns_}")

    # Prepare the arguments to pass to the script
    script_path = get_tdstone2_data_script_path()  # Replace this with how you get the path in your environment

    # Check if the script path exists
    if not os.path.exists(script_path):
        logger.error(f"Script file not found: {script_path}")
        return None

    # Prepare the command-line arguments
    args = [sys.executable, script_path, zip_file_path, str(text_column_), str(accumulate_columns_)]
    logger.info(f"Running script with arguments: {args}")

    # Run the script with the dataframe input piped to stdin
    try:
        result = subprocess.run(
            args,
            input=input_data,  # Pass the dataframe as stdin input
            text=True,  # Treat input and output as text (string)
            capture_output=True,  # Capture the stdout and stderr
            check=True  # Raise an error if the subprocess fails
        )
        logger.info("Script executed successfully.")

        # Parse the stdout into a pandas DataFrame
        output = result.stdout.strip()  # Remove any extra whitespace around the output
        if output:  # Ensure there is output to process
            logger.info("Processing script output into DataFrame.")
            rows = [line.split('\t') for line in output.split('\n')]  # Split rows and columns based on tab delimiter
            logger.info(rows[0])
            df_output = pd.DataFrame(rows,
                                     columns=accumulate_columns + ['jobid','process_time','elapsed_time'] + [text_column] + ['Vector_Dimension', 'V', 'model'])

            # Pivot the DataFrame to get the embeddings in a proper structure
            df_output = df_output.pivot(columns='Vector_Dimension', values='V',
                                        index=accumulate_columns + ['jobid','process_time','elapsed_time'] + [text_column] + ['model'])[
                [str(i) for i in range(df_output['Vector_Dimension'].astype(int).max())]]
        else:
            logger.warning("No output from the script. Returning an empty DataFrame.")
            df_output = pd.DataFrame()  # Return an empty DataFrame if no output

        return df_output

    except subprocess.CalledProcessError as e:
        logger.error(f"Error while running the script: {e.stderr}")
        return None