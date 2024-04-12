from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from contourgpt_v2 import enforce_json_structure
import oracledb, json, sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/generateSegment', methods=['POST'])
def generateSegment():

    user_prompt = request.json.get('user_prompt')
    print(user_prompt)

    res = enforce_json_structure(system_prompt = '''You are to extract the segment information from the user's query and complete the segment information based on the format''',
                    user_prompt = user_prompt,
                    # user_prompt = '''I want a oneoff segment named oldPeople which contains people over the age of fifty.''',
                    # user_prompt = '''I want a recurring segment named 3kids which contains people who have 3 kids.''',
                    # user_prompt = '''I want a oneoff segment named lowerClass which contains people who have an income of less than fifty thousand.''',
                    # user_prompt = '''I want a oneoff segment named upperClass which contains people who have an income of more than 100,000.''',

                    output_format = {
                        "segmentName": "<segment name>",
                        "segCalc": "<oneoff or recurring>",
                        "segCalcType": "<oneoff or recurring>",
                        "ruleParam": "Specified rule parameter, type: str['Age', 'Income', 'Kids']",
                        "ruleOperator": "Symbol for operator, type: str['=', '>=', '<=']",
                        "operatorText": "Operator description, str['is equal to', 'greater than or equal to', 'less than or equal to']",
                        "sentenceText": "Include People with an <ruleParam> value which  <operatorText>  <value>",
                        "ruleValue": "Value supplied by user, type: int"
                        }
                    )
    # print(res)

    data = getSegmentRules(res['ruleParam'])
    ruleid = data.get('ruleid')
    print('Rule_ID: ' + str(ruleid))
    # return str(ruleid)

    match res['ruleOperator']:
        case "=":
            ruleOperatorRecord = {
                "ruleOperatorRecord": {
                    "text": "is equal to",
                    "value": "exact_match",
                    "operatorAny": False,
                    "operatorSymbol": "="
                }
            }
            res.update(ruleOperatorRecord)
        case ">":
            res['ruleOperator'] = ">="
            ruleOperatorRecord = {
                "ruleOperatorRecord": {
                    "text": "is greater than or equal to",
                    "value": "greater_than_or_equal_to",
                    "operatorAny": False,
                    "operatorSymbol": ">="
                }
            }
            res.update(ruleOperatorRecord)
        case "<":
            res['ruleOperator'] = "<="
            ruleOperatorRecord = {
                "ruleOperatorRecord": {
                    "text": "is less than or equal to",
                    "value": "less_than_or_equal_to",
                    "operatorAny": False,
                    "operatorSymbol": "<="
                }
            }
            res.update(ruleOperatorRecord)
        case _:
            print("Fix this later")

    segStruc = {
                    "segmentID": None,
                    "segmentName": res['segmentName'],
                    "calculateWhen": "1",
                    "segCalc": res['segCalc'],
                    "segDaysToCalc": None,
                    "segStructure": "(S1=M)",
                    "segCalcType": res['segCalcType'],
                    "rules": [
                        {
                            "include": True,
                            "ruleID": str(ruleid),
                            "ruleOperator": res['ruleOperator'],
                            "ruleParam": res['ruleParam'].upper(),
                            "ruleGroupRecord": {
                                "text": "Person Attributes",
                                "value": "1"
                            },
                            "ruleParamRecord": {
                                "text": res['ruleParam'],
                                "value": res['ruleParam'].upper()
                            },
                            "ruleValue": str(res['ruleValue']),
                            "sentenceText": f"Include People with an {res['ruleParam']} value which  {res['ruleOperatorRecord']['text']}  {res['ruleValue']}",
                            "ruleOperatorRecord": res['ruleOperatorRecord'],
                            "ruleValueRecord": {
                                "value": str(res['ruleValue']),
                                "text": str(res['ruleValue'])
                            },
                            "ruleType": f"type:{str(ruleid)}",
                            "ruleTypeRecord": {
                                "text": res['ruleParam'],
                                "value": f"type:{str(ruleid)}"
                            }
                        }
                    ]
                }



    segment_id = createSegment(segStruc)
    print("generateSegment Response: ")
    print(segment_id)
    print(segStruc)


    if segment_id:
        return jsonify({"message": "Segment created successfully.", "segmentID": segment_id}), 200
    else:
        return jsonify({"error": "Unable to retrieve segment ID."}), 500

    # return segStruc

def execute(sql, mode, **kwargs):
    try:
        connection = oracledb.connect(user="RAMBO", password="biggun", dsn="STALLONE:1521/STALLONE")
        cursor = connection.cursor()
        parameters = kwargs.get('parameters', [])

        if mode == 'P':  # Procedure
            # parameters = kwargs.get('parameters', [])
            out_param = None
            if kwargs.get('has_out_param', False):
                out_param = cursor.var(int)  # Assuming OUT param is needed
                parameters.insert(0, out_param)  # If OUT param should be first
            cursor.callproc(sql, parameters)
            connection.commit()

            if out_param is not None:
                print("execute Response: ")
                print(out_param.getvalue())
                return out_param.getvalue()  # Return just the OUT param value

        elif mode == 'Q':  # Execute a query with parameters
            # parameters = kwargs.get('parameters', [])
            print(parameters)
            cursor.execute(sql, parameters)  # Execute with parameters
            rows = cursor.fetchall()
            return rows  # Return fetched rows for queries

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

@app.route('/getOracleData', methods=['GET'])
def getSegmentRules(field):
    # sql = "SELECT ruleid, field, field_name, operator, operator_name FROM segment_rules WHERE ruleid IN (1, 8, 9)"

    # Retrieve 'Field' parameter from the URL query string and convert it to uppercase
    # field_param = request.args.get('field', '').upper()
    field_param = field.upper()

    # Construct a parameterized SQL query
    sql = "SELECT ruleid, field, field_name, operator, operator_name FROM segment_rules WHERE field = :field_param"
    # sql = "SELECT ruleid, field, field_name, operator, operator_name FROM segment_rules WHERE field = 'INCOME'"

    # Execute the SQL query with parameter
    rows = execute(sql, 'Q', parameters={"field_param": field_param})
    # rows = execute(sql, 'Q')

    # Convert data into list of dictionaries
    # data = []
    # for row in rows:
    #     data.append({
    #         "ruleid": row[0],
    #         "field": row[1],
    #         "field_name": row[2],
    #         "operator": row[3],
    #         "operator_name": row[4]
    #     })

    # return jsonify(data)
    # return jsonify({"response": rows})

    data = [{"ruleid": row[0], "field": row[1], "field_name": row[2], "operator": row[3], "operator_name": row[4]} for row in rows]
    return data[0]

@app.route('/createSegment', methods=['POST'])
def createSegment(segStruc):
    try:
        # Extract data from the request

        # Convert formData to JSON string
        segrulejson = json.dumps(segStruc, separators=(',', ':'))

        # Define the parameters for the procedure call
        parameters = [
            segStruc.get('segmentName', ''),  # in_segmentname
            '7107',                           # in_userid
            '-299',                           # in_applicationid
            segrulejson,                      # in_segrulejson
            1,                                # in_calculate
            1,                                # use inday data? 1 or 0
            '',                               # in_descriptionbyuser
            1                                 # Debug flag
        ]

        # Call the execute function to run the procedure
        segment_id = execute('SegInterface.save_segment', 'P', parameters=parameters, has_out_param=True)

        print("createSegment Response: ")
        print(segment_id)

        return segment_id
        # return segrulejson

        # if segment_id:
        #     return jsonify({"message": "Segment created successfully.", "segmentID": segment_id}), 200
        # else:
        #     return jsonify({"error": "Unable to retrieve segment ID."}), 500

        # Retrieve the value of the OUT parameter
        # segment_id = segment_id_var.getvalue()
        # print("Segment ID:", segment_id)

        # Return a success response
        # return jsonify({"message": "Segment created successfully.", "out_matches": out_matches.getvalue(), "out_last_calc_date": out_last_calc_date.getvalue()}), 200
        # return jsonify({"message": "Segment created successfully.", "segmentID": segment_id}), 200
        # return jsonify({"message": "Segment Structure.", "Segment": segrulejson}), 200
        # return jsonify({"message": "Segment Structure.", "Segment": segStruc}), 200

    except Exception as e:
        # Return an error response if an exception occurs
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8050, host="0.0.0.0", debug=True)