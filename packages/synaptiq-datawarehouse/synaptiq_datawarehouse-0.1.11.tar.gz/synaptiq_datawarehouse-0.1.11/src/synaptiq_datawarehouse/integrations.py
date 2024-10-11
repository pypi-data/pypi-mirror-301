import json

import dateutil.parser
import requests
from databricks.sdk.runtime import *
from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build
from xero_python.accounting import AccountingApi



# COMMAND ----------


def query_freshteams(query, freshteams_api_key):
    # Freshteams connection params
    base_url = "https://synaptiq.freshteam.com/api"
    header = {
        "accept": "application/json",
        "Authorization": "Bearer " + freshteams_api_key,
    }
    url = base_url + query

    result = requests.get(url, headers=header).text
    return result


# COMMAND ----------


# retrieve the token from the tmp file store in order to handle 60 day expiration and refresh
def read_xero_token():
    return dbutils.fs.head("/tmp/xero")


def write_xero_token(token):
    dbutils.fs.put("/tmp/xero", token, True)


def refresh_xero_access_token(xero_client_id, xero_client_secret):
    url = "https://identity.xero.com/connect/token"

    # boot strap with this then load from temp file
    # TODO: write back to secret or at least fall back to secret on failure/missing
    # refresh_token = dbutils.secrets.get(scope='synaptiq_dw', key='xero_refresh_token')
    refresh_token = read_xero_token()
    response = requests.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "client_id": xero_client_id,
            "client_secret": xero_client_secret,
            "refresh_token": refresh_token,
        },
    )
    json_response = response.json()
    write_xero_token(json_response["refresh_token"])
    return json_response


def accounting_get_invoices(
    xero_tenant_id, api_client, modified_since="2020-01-01T00:00:00.000Z"
):
    api_instance = AccountingApi(api_client)

    # Set parameters for invoice query
    if_modified_since = dateutil.parser.parse(modified_since)
    where = 'Type=="ACCREC"'
    order = "Date ASC"
    include_archived = False
    summary_only = False
    page = 1  # Page number for pagination
    page_size = 1000

    try:
        api_response = api_instance.get_invoices(
            xero_tenant_id=xero_tenant_id,
            if_modified_since=if_modified_since,
            where=where,
            order=order,
            page=page,
            page_size=page_size,
            include_archived=include_archived,
            summary_only=summary_only,
        )
        return api_response
    except Exception as e:
        print(f"Exception when calling AccountingApi->get_invoices: {e}")
        return None


def process_invoices(invoices_dict):
    for i, invoice in enumerate(invoices_dict["invoices"]):
        invoices_dict["invoices"][i]["line_amount_types"] = invoice[
            "line_amount_types"
        ].value
        invoices_dict["invoices"][i]["currency_code"] = invoice["currency_code"].value
    return invoices_dict


def list_gsuite_users(credentials_json, subject=None):
    credentials_dict = json.loads(credentials_json)
    creds = service_account.Credentials.from_service_account_info(
        credentials_dict,
        scopes=["https://www.googleapis.com/auth/admin.directory.user.readonly"],
        subject=subject,
    )

    # Build the API service
    service = build("admin", "directory_v1", credentials=creds)

    # Call the API to list all users
    users = service.users().list(customer="C01gp0xmn").execute()
    return json.dumps(users.get("users", []))


# COMMAND ----------


def write_data_to_delta(spark, data, table_name, database_name):
    destination = database_name + "." + table_name
    # escape out any key names with disallowed characters
    cleaned_data = escape_keys(json.loads(data))
    # find the python incantation to delete or merge the table first
    spark.read.json(sc.parallelize([json.dumps(cleaned_data)])).write.mode(
        "overwrite"
    ).option("overwriteSchema", "true").format("delta").saveAsTable(destination)


def write_df_to_delta(
    spark, data_frame, table_name, write_to_bigquery, database_name, bq_client
):
    spark_df = spark.createDataFrame(data_frame)
    spark_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(
        database_name + "." + table_name
    )
    if write_to_bigquery:
        write_df_to_bigquery(data_frame, table_name, bq_client)


def write_df_to_bigquery(df, table_name, bq_client):
    file_path = "/tmp/" + table_name + ".csv"
    df.to_csv(file_path, index=False)
    table_id = "synaptiq_data_warehouse." + table_name
    print("about to create table: " + table_id + " in BigQuery")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    with open(file_path, "rb") as source_file:
        job = bq_client.load_table_from_file(
            source_file, table_id, job_config=job_config
        )

    job.result()  # Waits for the job to complete.

    table = bq_client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )


def save_output(data, table_name):
    dbutils.fs.put("/FileStore/" + table_name + ".json", data, True)


# find and replace all key names with a new key name
def escape_keys(data, characters=[" ", ",", ";", "{", "}", "(", ")", "\n", "\t", "="]):
    if isinstance(data, list):
        for item in data:
            escape_keys(item, characters)
    elif isinstance(data, dict):
        for key, value in list(data.items()):
            new_key = key
            for char in characters:
                if new_key.find(char) != -1:
                    new_key = new_key.replace(char, "_")
            data[new_key] = data.pop(key)
            escape_keys(value, characters)
    return data

def load_data_from_everhour(everhour_client, query, pagination=True, verbose=False):
  i = 0
  cleaned_data = []
  # Loop over everhour API pagination
  while True:
      i += 1
      if pagination:
        data = everhour_client.query_everhour(query + f"&page={i}")
      else:
        data = everhour_client.query_everhour(query)
        cleaned_data.extend(escape_keys(json.loads(data)))
        break
      n_page = escape_keys(json.loads(data))
      cleaned_data.extend(n_page)

      # exit the loop if no more data to be processed
      if len(n_page) == 0:
          break
      if verbose:
        print(f"Everhour historical data page {i} processed")
  return cleaned_data