import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import json

app = func.FunctionApp()

@app.function_name(name="cases")
@app.route(route="cases", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
@app.generic_input_binding(arg_name="cases", type="sql",
                        CommandType="Text",
                        ConnectionStringSetting="SqlConnectionString",
                        data_type=DataType.STRING)
def get_cases(req: func.HttpRequest, cases: func.SqlRowList) -> func.HttpResponse:
    with open('dart_query.sql', 'r') as dart_query:
        dart_sql = dart_query.read()
        cases.set('CommandText', dart_sql)
        rows = list(map(lambda r: json.loads(r.to_json()), cases))
        return func.HttpResponse(
            json.dumps(rows),
            status_code=200,
            mimetype="application/json"
    )

@app.function_name(name="getCase")
@app.route(route="case/{AppealRefNumber}", methods=["get"], auth_level=func.AuthLevel.FUNCTION)
@app.generic_input_binding(arg_name="case", type="sql",
                        CommandText="SELECT * FROM [odw_harmonised_db].[dbo].[casework_case_info_dim] WHERE [AppealRefNumber] = @appealRefNumber",
                        CommandType="Text",
                        Parameters="@AppealRefNumber={AppealRefNumber}",
                        ConnectionStringSetting="SqlConnectionString",
                        data_type=DataType.STRING)
def get_case(req: func.HttpRequest, case: func.SqlRowList) -> func.HttpResponse:
    rows = list(map(lambda r: json.loads(r.to_json()), case))
    return func.HttpResponse(
        json.dumps(rows),
        status_code=200,
        mimetype="application/json"
    )
