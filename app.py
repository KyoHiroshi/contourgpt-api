from flask import Flask, request, jsonify
from contourgpt_v2 import enforce_json_structure
import oracledb, json, sys

app = Flask(__name__)

@app.route('/generateSegment', methods=['GET'])
def generateSegment():
    res = enforce_json_structure(system_prompt = '''You are to extract the segment information from the user's query and complete the segment information based on the format''',
                    user_prompt = '''I want a oneoff segment named oldPeople which contains people over the age of fifty.''',
                    # user_prompt = '''I want a recurring segment named 3kids which contains people who have 3 kids.''',
                    # user_prompt = '''I want a oneoff segment named lowerClass which contains people who have an income of less than fifty thousand.''',

                    # output_format = {
                    #     "segmentName": "<segment name>",
                    #     "segCalc": "<oneoff or recurring>",
                    #     "ruleParam": "Specified rule parameter, type: str['Age', 'Income', 'Kids']",
                    #     "ruleOperator": "Symbol for operator, type: str['=', '>=', '<=']",
                    #     "operatorText": "Operator description, str['is equal to', 'greater than or equal to', 'less than or equal to']",
                    #     "sentenceText": "Include People with an <ruleParam> value which  <operatorText>  <value>",
                    #     "value": "Value supplied by user, type: int"
                    #     }

                    output_format = {
                        "segmentID": "null",
                        "segmentName": "<segment name>",
                        "calculateWhen": "1",
                        "segCalc": "<oneoff or recurring>",
                        "segDaysToCalc": "null",
                        "segStructure": "(S1=M)",
                        "segCalcType": "<oneoff or recurring>",
                        "rules": [
                          {
                              "include": "true",
                              "ruleID": "1",
                              "ruleOperator": "[=>, =, <=]",
                              "ruleParam": "<Rule Parameter, type: str['Age', 'Income', 'Kids']>",
                              "ruleGroupRecord": {
                                  "text": "Person Attributes",
                                  "value": "1"
                              },
                              "ruleParamRecord": {
                                  "text": "<Rule Parameter>",
                                  "value": "<Rule Parameter>"
                              },
                              "ruleValue": "<ruleValue, type: int>",
                              "sentenceText": "Include People with an <Rule Parameter> which  is greater than or equal to  <value>",
                              "ruleOperatorRecord": {
                                  "text": "is greater than or equal to",
                                  "value": "greater_than_or_equal",
                                  "operatorAny": "false",
                                  "operatorSymbol": ">="
                              },
                              "ruleValueRecord": {
                                  "value": "<ruleValue>",
                                  "text": "<ruleValue>"
                              },
                              "ruleType": "type:1",
                              "ruleTypeRecord": {
                                  "text": "<Rule Parameter>",
                                  "value": "type:1"
                              }
                            }
                          ]
                        }
                    )
    return jsonify(res)
    print(res)

def execute(sql, mode, **kwargs):
    try:
        # Establish a connection to the database
        connection = oracledb.connect(user="RAMBO", password="biggun", dsn="STALLONE:1521/STALLONE")

        # Create a cursor object
        cursor = connection.cursor()

        if mode == 'P':  # Execute a procedure
            procedure_name = sql
            parameters = kwargs.get('parameters', [])
            cursor.callproc(procedure_name, parameters)
            connection.commit()

        elif mode == 'Q':  # Execute a query
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows

    except Exception as e:
        print("An error occurred:", e)
        return None

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@app.route('/getOracleData', methods=['GET'])
def getSegmentRules():
    sql = "SELECT ruleid, field, field_name, operator, operator_name FROM segment_rules WHERE ruleid IN (1, 8, 9)"
    rows = execute(sql, 'Q')

    # Convert data into list of dictionaries
    data = []
    for row in rows:
        data.append({
            "ruleid": row[0],
            "field": row[1],
            "field_name": row[2],
            "operator": row[3],
            "operator_name": row[4]
        })

    return jsonify(data)
    # return jsonify({"response": rows})

@app.route('/createSegment', methods=['POST'])
def createSegment():
    # print('This works')
    # sys.exit()
    try:
        # Extract data from the request
        # formData = request.json  # Assuming JSON data is sent in the request body

        formData = {
            "segmentID": None,
            "segmentName": "MHT_segTest13",
            "calculateWhen": "1",
            "segCalc": "oneoff",
            "segDaysToCalc": None,
            "segStructure": "(S1=M)",
            "segCalcType": "oneoff",
            "rules": [
                {
                    "include": True,
                    "ruleID": "9",
                    "ruleOperator": "=",
                    "ruleParam": "KIDS",
                    "ruleGroupRecord": {
                        "text": "Person Attributes",
                        "value": "1"
                    },
                    "ruleParamRecord": {
                        "text": "Kids",
                        "value": "KIDS"
                    },
                    "ruleValue": "3",
                    "sentenceText": "Include People with a number of Kids which is equal to 3",
                    "ruleOperatorRecord": {
                        "text": "is equal to",
                        "value": "exact_match",
                        "operatorAny": False,
                        "operatorSymbol": "="
                    },
                    "ruleValueRecord": {
                        "value": "3",
                        "text": "3"
                    },
                    "ruleType": "type:9",
                    "ruleTypeRecord": {
                        "text": "Kids",
                        "value": "type:9"
                    }
                }
            ]
        }

        # formData2 = {"segmentID":None,"segmentName":"MHT_segTest8","calculateWhen":"1","segCalc":"oneoff","segDaysToCalc":None,"segStructure":"(S1=M)","segCalcType":"oneoff","rules":[{"include":True,"ruleID":"9","ruleOperator":"=","ruleParam":"KIDS","ruleGroupRecord":{"text":"Person Attributes","value":"1"},"ruleParamRecord":{"text":"Kids","value":"KIDS"},"ruleValue":"3","sentenceText":"Include People with a number of Kids which  is equal to  3","ruleOperatorRecord":{"text":"is equal to","value":"exact_match","operatorAny":False,"operatorSymbol":"="},"ruleValueRecord":{"value":"3","text":"3"},"ruleType":"type:9","ruleTypeRecord":{"text":"Kids","value":"type:9"}}]}

        # Establish a connection to the database
        connection = oracledb.connect(user="RAMBO", password="biggun", dsn="STALLONE:1521/STALLONE")

        # Create a cursor object
        cursor = connection.cursor()

        # Define the variable to hold the OUT parameter
        segment_id_var = cursor.var(int)

        # Convert formData to JSON string
        segrulejson = json.dumps(formData, separators=(',', ':'))

        # print(segrulejson)

        # Call the procedure
        cursor.callproc('SegInterface.save_segment', [
            segment_id_var,  # io_segmentid
            formData.get('segmentName', ''), # in_segmentname
            '7107', # in_userid
            '-299', # in_applicationid
            segrulejson, # in_segrulejson
            1, # in_calculate
            1, # / use inday data? 1 or 0
            'AI Generated Segment 6', # in_descriptionbyuser
            1 # Debug flag
        ])

        # # Retrieve the value of the OUT parameter
        segment_id = segment_id_var.getvalue()
        print("Segment ID:", segment_id)

        # out_matches = cursor.var(int)
        # out_last_calc_date = cursor.var(str)
        # cursor.callproc('SegInterface.get_seg_calc_and_date', [
        #     11893,
        #     out_matches,
        #     out_last_calc_date,
        #     1
        # ])

        # print("Segment ID:", 11893)
        # print("out_matches:", out_matches.getvalue())
        # print("out_last_calc_date:", out_last_calc_date.getvalue())




        # Return a success response
        # return jsonify({"message": "Segment created successfully.", "out_matches": out_matches.getvalue(), "out_last_calc_date": out_last_calc_date.getvalue()}), 200
        return jsonify({"message": "Segment created successfully.", "segmentID": segment_id}), 200

    except Exception as e:
        # Return an error response if an exception occurs
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8050, host="0.0.0.0", debug=True)