from flask import Flask, request, jsonify
from contourgpt_v2 import enforce_json_structure
import oracledb

app = Flask(__name__)

@app.route('/generateSegment', methods=['GET'])
def test():
    # Testing Rule Parameter: Age
    # res = enforce_json_structure(system_prompt = '''You are to extract the segment information from the user's query and complete the segment information based on the format''',
    #                 user_prompt = '''I want a oneoff segment named oldPeople which contains people over the age of 50.''',
    #                 # output_format = {"segmentName": "<segment name>", "segCalc": "Is it oneoff or recurring", "ruleOperator": "Is it =, >= or <=", "value": "<value>"}
    #                 output_format = {
    #                     "segmentID": "null",
    #                     "segmentName": "<segment name>",
    #                     "calculateWhen": "1",
    #                     "segCalc": "<Is it oneoff or recurring>",
    #                     "segDaysToCalc": "null",
    #                     "segStructure": "(S1=M)",
    #                     "segCalcType": "<Is it oneoff or recurring>",
    #                     "rules": [
    #                       {
    #                           "include": "true",
    #                           "ruleID": "1",
    #                           "ruleOperator": "{Is it =, >= or <=}",
    #                           "ruleParam": "<Rule Parameter>",
    #                           "ruleGroupRecord": {
    #                               "text": "Person Attributes",
    #                               "value": "1"
    #                           },
    #                           "ruleParamRecord": {
    #                               "text": "<Rule Parameter>",
    #                               "value": "<Rule Parameter>"
    #                           },
    #                           "ruleValue": "<value>",
    #                           "sentenceText": "Include People with an <Rule Parameter> which  is equal to  <value>",
    #                           "ruleOperatorRecord": {
    #                               "text": "is equal to",
    #                               "value": "exact_match",
    #                               "operatorAny": "false",
    #                               "operatorSymbol": "="
    #                           },
    #                           "ruleValueRecord": {
    #                               "value": "<value>",
    #                               "text": "<value>"
    #                           },
    #                           "ruleType": "type:1",
    #                           "ruleTypeRecord": {
    #                               "text": "<Rule Parameter>",
    #                               "value": "type:1"
    #                           }
    #                         }
    #                       ]
    #                     }
    #               )
    # return jsonify({"response": res})
    # print(res)

    # Testing Rule Parameter: Income
    # res = enforce_json_structure(system_prompt = '''You are to extract the segment information from the user's query and complete the segment information based on the format''',
    #                 user_prompt = '''I want a recurring segment named income2000 which contains people who have a minimum income of 2000.''',
    #                 # output_format = {"segmentName": "<segment name>", "segCalc": "Is it oneoff or recurring", "ruleOperator": "Is it =, >= or <=", "value": "<value>"}
    #                 output_format = {
    #                     "segmentID": "0",
    #                     "segmentName": "<segment name>",
    #                     "calculateWhen": "1",
    #                     "segCalc": "<Is it oneoff or recurring>",
    #                     "segDaysToCalc": "null",
    #                     "segStructure": "(S1=M)",
    #                     "segCalcType": "<Is it oneoff or recurring>",
    #                     "rules": [
    #                       {
    #                           "include": "true",
    #                           "ruleID": "8",
    #                           "ruleOperator": "{Is it =, >= or <=}",
    #                           "ruleParam": "<Rule Parameter>",
    #                           "ruleGroupRecord": {
    #                               "text": "Person Attributes",
    #                               "value": "1"
    #                           },
    #                           "ruleParamRecord": {
    #                               "text": "<Rule Parameter>",
    #                               "value": "<Rule Parameter>"
    #                           },
    #                           "ruleValue": "<value>",
    #                           "sentenceText": "Include People with an <Rule Parameter> value which  {is equal to/greater than or equal to}  <value>",
    #                           "ruleOperatorRecord": {
    #                               "text": "is equal to",
    #                               "value": "exact_match",
    #                               "operatorAny": "false",
    #                               "operatorSymbol": "{Is it =, >= or <=}"
    #                           },
    #                           "ruleValueRecord": {
    #                               "value": "<value>",
    #                               "text": "<value>"
    #                           },
    #                           "ruleType": "type:8",
    #                           "ruleTypeRecord": {
    #                               "text": "<Rule Parameter>",
    #                               "value": "type:1"
    #                           }
    #                         }
    #                       ]
    #                     }
    #               )
    # return jsonify({"response": res})
    # print(res)

    # Testing Rule Parameter: Kids
    res = enforce_json_structure(system_prompt = '''You are to extract the segment information from the user's query and complete the segment information based on the format''',
                    user_prompt = '''I want a oneoff segment named 3kids which contains people who have a 3 kids.''',
                    output_format = {
                        "segmentName": "<segment name>",
                        "segCalc": "{oneoff/recurring}",
                        "ruleParam": "{Age/Income/Kids}",
                        "ruleOperator": "{=/>=/<=}",
                        "operatorText": "{is equal to/greater than or equal to/less than or equal to}",
                        "value": "<value>"
                        }
    )
                #     output_format = {
                #         "segmentID": "0",
                #         "segmentName": "<segment name>",
                #         "calculateWhen": "1",
                #         "segCalc": "<Is it oneoff or recurring>",
                #         "segDaysToCalc": "null",
                #         "segStructure": "(S1=M)",
                #         "segCalcType": "{oneoff/recurring}",
                #         "rules": [
                #           {
                #               "include": "true",
                #               "ruleID": "3",
                #               "ruleOperator": "{Is it =, >= or <=}",
                #               "ruleParam": "<Rule Parameter>",
                #               "ruleGroupRecord": {
                #                   "text": "Person Attributes",
                #                   "value": "1"
                #               },
                #               "ruleParamRecord": {
                #                   "text": "<Rule Parameter>",
                #                   "value": "<Rule Parameter>"
                #               },
                #               "ruleValue": "<value>",
                #               "sentenceText": "Include People with an <Rule Parameter> value which  {is equal to/greater than or equal to}  <value>",
                #               "ruleOperatorRecord": {
                #                   "text": "is equal to",
                #                   "value": "exact_match",
                #                   "operatorAny": "false",
                #                   "operatorSymbol": "{Is it =, >= or <=}"
                #               },
                #               "ruleValueRecord": {
                #                   "value": "<value>",
                #                   "text": "<value>"
                #               },
                #               "ruleType": "type:3",
                #               "ruleTypeRecord": {
                #                   "text": "<Rule Parameter>",
                #                   "value": "type:1"
                #               }
                #             }
                #           ]
                #         }
                #   )
    return jsonify({"response": res})
    print(res)

@app.route('/getOracleData', methods=['GET'])
def testOracle():
    # Establish a connection to the database
    connection = oracledb.connect("username", "password", "hostname:port/service_name")

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a query
    cursor.execute("SELECT * FROM segment_rules WHERE FIELD IN ('AGE', 'INCOME', 'KIDS');")

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the results
    # for row in rows:
    #     print(row)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return jsonify({"response": rows})


if __name__ == '__main__':
    app.run(port=8050, host="0.0.0.0", debug=True)