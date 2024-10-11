<h1 align="center">
  DCS SDK v0.3.1
</h1>

> SDK for DataChecks


## Installation

> Python version `>=3.10,<3.12`

```bash

$ pip install dcs-sdk[all-dbs]

```

## Supported Databases

> Availability Status

| Database   | Code Name    | Supported |
| ---------- | ------------ | --------- |
| PostgreSQL | `postgres`   | ✅         |
| Snowflake  | `snowflake`  | ✅         |
| Trino      | `trino`      | ✅         |
| Databricks | `databricks` | ✅         |
| Oracle     | `oracle`     | ✅         |
| MSSQL      | `mssql`      | ✅         |
| File       | `file`       | ✅         |



## Available Commands



|    Option     | Short Option | Required |     Default     |                    Description                     |                                             Example                                              |
| :-----------: | :----------: | :------: | :-------------: | :------------------------------------------------: | :----------------------------------------------------------------------------------------------: |
| --config-path |      -C      | **Yes**  |      None       |    Specify the file path for the configuration     |                    dcs_sdk run --config-path config.yaml --compare comp_name                     |
|   --compare   |              | **Yes**  |      None       | Run only specific comparison using comparison name |                    dcs_sdk run --config-path config.yaml --compare comp_name                     |
|  --save-json  |      -j      |    No    |      False      |           Save the data into a JSON file           |              dcs_sdk run --config-path config.yaml --compare comp_name --save-json               |
|  --json-path  |     -jp      |    No    | dcs_report.json |        Specify the file path for JSON file         |   dcs_sdk run --config-path config.yaml --compare comp_name --save-json --json-path ouput.json   |
|    --stats    |              |    No    |      False      |            Print stats about data diff             |                dcs_sdk run --config-path config.yaml --compare comp_name --stats                 |
|     --url     |              |    No    |      None       |         Specify url to send data to server         |    dcs_sdk run --config-path config.yaml --compare comp_name --url=https://comapre/send/data     |
| --html-report |              |    No    |      False      |                 Save table as HTML                 |             dcs_sdk run --config-path config.yaml --compare comp_name --html-report              |
| --report-path |              |    No    | dcs_report.html |       Specify the file path for HTML report        | dcs_sdk run --config-path config.yaml --compare comp_name --html-report --report-path table.html |



### Example Command [CLI]

```sh
$ dcs_sdk --version

$ dcs_sdk --help

$ dcs_sdk run -C example.yaml --compare comparison_one --stats -j -jp output.json --html-report --report-path result.html --url=https://comapre/send/data
```

<details>
<summary><h2>Example Configuration</h2></summary>

```yml
data_sources:
  - name: iris_snowflake
    type: snowflake
    id: f533c099-196f-48da-b231-1d4c380f84bf
    workspace: default
    connection:
      account: bp54281.central-india.azure
      username: !ENV ${SNOWFLAKE_USER}
      password: !ENV ${SNOWFLAKE_PASS}
      database: TEST_DCS
      schema: PUBLIC
      warehouse: compute_wh
      role: accountadmin

  - name: pgsql_azure
    type: postgres
    id: 4679b79a-7174-48fd-9c71-81cf806ef617
    workspace: default
    connection:
      host: !ENV ${POSTGRES_HOST_ONE}
      port: !ENV ${POSTGRES_PORT_ONE}
      username: !ENV ${POSTGRES_USER_ONE}
      password: !ENV ${POSTGRES_PASSWORD_ONE}
      database: !ENV ${POSTGRES_DB_ONE}

  - name: trino_test
    type: trino
    id: 9d86df86-6802-4551-a1ce-b98cdf3ec15f
    workspace: default
    connection:
      host: localhost
      port: 8080
      username: admin
      catalog: tpch
      schema: sf100

  - name: file_source_raw
    id: b5a76a0a-1b8f-4222-a31d-a31740f23168
    workspace: default
    type: file
    file_path: "nk.kyc_data/RAW_EMPLOYEE.csv"

  - name: file_source_tl
    id: 52c1f3c7-fd1e-4f3c-aed3-b01d8e1cfa4d
    workspace: default
    type: file
    file_path: "nk.kyc_data/TL_EMPLOYEE.csv"

  - name: databricks_test
    type: databricks
    id: 6f1fd8d6-5a59-4ba5-be37-aec044b000e7
    workspace: default
    connection:
      host: !ENV ${DATABRICKS_HOST}
      port: !ENV ${DATABRICKS_PORT}
      catalog: hive_metastore
      schema: default
      access_token: !ENV ${DATABRICKS_ACCESS_TOKEN}
      http_path: !ENV ${DATABRICKS_HTTP_PATH}

comparisons:
  # DB TO DB (SNOWFLAKE)
  comparison_one:
    source:
      data_source: iris_snowflake
      table: RAW_EMPLOYEE

    target:
      data_source: iris_snowflake
      table: TL_EMPLOYEE
    key_columns:
      - CUSTID
    columns:
      - FIRSTNAME
      - LASTNAME
      - DESIGNATION
      - SALARY

  # DB TO DB (Postgres Azure)
  comparison_two:
    source:
      data_source: pgsql_azure
      table: actor
    target:
      data_source: pgsql_azure
      table: actor2
    key_columns:
      - actor_id
    columns:
      - first_name
      - last_name
      - last_update
    columns_mappings:
      - source_column: actor_id
        target_column: actor_id1
      - source_column: first_name
        target_column: first_name1
      - source_column: last_name
        target_column: last_name1
      - source_column: last_update
        target_column: last_update1

  # FILE TO FILE
  comparison_three:
    source:
      data_source: file_source_raw
      table: RAW_EMPLOYEE

    target:
      data_source: file_source_tl
      table: TL_EMPLOYEE
    key_columns:
      - custid
    columns:
      - FIRSTNAME
      - lastname
      - designation
      - salary
    columns_mappings:
      - source_column: FIRSTNAME
        target_column: firstname

  # DB TO DB (Trino)
  comparison_trino:
    source:
      data_source: trino_test
      table: nation
    target:
      data_source: trino_test
      table: region
    key_columns:
      - regionkey
    columns:
      - name

  # DB TO DB (Databricks)
  comparison_databricks:
    source:
      data_source: databricks_test
      table: RAW_EMPLOYEE

    target:
      data_source: databricks_test
      table: TL_EMPLOYEE
    key_columns:
      - custid
    columns:
      - FIRSTNAME
      - lastname
      - designation
      - salary
    columns_mappings:
      - source_column: FIRSTNAME
        target_column: firstname
```
</details>