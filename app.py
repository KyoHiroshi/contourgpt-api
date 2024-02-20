from flask import Flask, request, jsonify
from contourgpt_v2 import enforce_json_structure
import cx_Oracle

app = Flask(__name__)

@app.route('/generateSegment', methods=['GET'])
def test():
    res = enforce_json_structure(system_prompt = '''You are to extract the segment information from the user's query and complete the segment information based on the format''',
                    user_prompt = '''I want a oneoff segment named oldPeople which contains people over the age of 50.''',
                    # output_format = {"segmentName": "<segment name>", "segCalc": "Is it oneoff or recurring", "ruleOperator": "Is it =, >= or <=", "value": "<value>"}
                    output_format = {
                        "segmentID": "null",
                        "segmentName": "<segment name>",
                        "calculateWhen": "1",
                        "segCalc": "<Is it oneoff or recurring>",
                        "segDaysToCalc": "null",
                        "segStructure": "(S1=M)",
                        "segCalcType": "<Is it oneoff or recurring>",
                        "rules": [
                          {
                              "include": "true",
                              "ruleID": "1",
                              "ruleOperator": "{Is it =, >= or <=}",
                              "ruleParam": "<Rule Parameter>",
                              "ruleGroupRecord": {
                                  "text": "Person Attributes",
                                  "value": "1"
                              },
                              "ruleParamRecord": {
                                  "text": "<Rule Parameter>",
                                  "value": "<Rule Parameter>"
                              },
                              "ruleValue": "<value>",
                              "sentenceText": "Include People with an <Rule Parameter> which  is equal to  <value>",
                              "ruleOperatorRecord": {
                                  "text": "is equal to",
                                  "value": "exact_match",
                                  "operatorAny": "false",
                                  "operatorSymbol": "="
                              },
                              "ruleValueRecord": {
                                  "value": "<value>",
                                  "text": "<value>"
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
    return jsonify({"response": res})
    print(res)

if __name__ == '__main__':
    app.run(port=8050, host="0.0.0.0", debug=True)