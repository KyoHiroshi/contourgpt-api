import ast
import json
import os
import re

import openai
from openai import OpenAI

# API Keys
os.environ["OPENAI_API_KEY"] = ["INSERT API KEY HERE"]
openai.api_key = os.environ["OPENAI_API_KEY"]


def enforce_json_structure(
    system_prompt,
    user_prompt,
    output_format,
    delimiter="###",
    model="gpt-3.5-turbo",
    temperature=0,
    num_tries=3,
    verbose=False,
    literal_eval=True,
    openai_json_mode=False,
    **kwargs,
):

    client = OpenAI()

    # If OpenAI JSON mode is selected, then just let OpenAI do the processing
    if openai_json_mode:
        # if model fails, default to gpt-3.5-turbo-1106
        try:
            assert model in ["gpt-4-1106-preview", "gpt-3.5-turbo-1106"]
        except Exception as e:
            model = "gpt-3.5-turbo-1106"

        response = client.chat.completions.create(
            temperature=temperature,
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": str(system_prompt)
                    + "\nOutput in the following json format: "
                    + str(output_format),
                },
                {"role": "user", "content": str(user_prompt)},
            ],
            **kwargs,
        )
        res = response.choices[0].message.content
        try:
            loaded_json = json.loads(res)
        except Exception as e:
            loaded_json = {}
        return loaded_json

    # Otherwise, implement JSON parsing using Strict JSON
    else:
        # start off with no error message
        error_msg = ""

        for i in range(num_tries):

            # make the output format keys with a unique identifier
            new_output_format = {}
            for key in output_format.keys():
                new_output_format[f"{delimiter}{key}{delimiter}"] = output_format[key]
            output_format_prompt = f"""\nYou are to output the following in json format: {new_output_format}
    You must use "{delimiter}{{key}}{delimiter}" to enclose each {{key}} and change values based on context"""

            # Use OpenAI to get a response
            client = OpenAI()
            response = client.chat.completions.create(
                temperature=temperature,
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": str(system_prompt)
                        + output_format_prompt
                        + error_msg,
                    },
                    {"role": "user", "content": str(user_prompt)},
                ],
                **kwargs,
            )

            res = response.choices[0].message.content

            if verbose:
                print(
                    "System prompt:", system_prompt + output_format_prompt + error_msg
                )
                print("\nUser prompt:", str(user_prompt))
                print("\nGPT response:", res)

            # try-catch block to ensure output format is adhered to
            try:
                # check key appears for each element in the output
                for key in new_output_format.keys():
                    # if output field missing, raise an error
                    if key not in res:
                        raise Exception(f"{key} not in json output")

                # if all is good, we then extract out the fields
                # Use regular expressions to extract keys and values
                pattern = rf",*\s*['|\"]{delimiter}([^#]*){delimiter}['|\"]: "

                matches = re.split(pattern, res[1:-1])

                # remove null matches
                my_matches = [match for match in matches if match != ""]

                # remove the ' from the value matches
                curated_matches = [
                    match[1:-1] if match[0] in "'\"" else match for match in my_matches
                ]

                # create a dictionary
                end_dict = {}
                for i in range(0, len(curated_matches), 2):
                    end_dict[curated_matches[i]] = curated_matches[i + 1]

                # try to do some parsing via literal_eval
                if literal_eval:
                    res = end_dict
                    for key in end_dict.keys():
                        try:
                            end_dict[key] = ast.literal_eval(end_dict[key])
                        except Exception as e:
                            # if there is an error in literal processing, do nothing as it is not of the form of a literal
                            continue

                return end_dict

            except Exception as e:
                error_msg = f'\n\nResult: {res}\n\nError message: {str(e)}\nYou must use "{delimiter}{{key}}{delimiter}" to enclose the each {{key}}.'
                print("An exception occurred:", str(e))
                print("Current invalid json format:", res)

        return {}


class strict_function:
    def __init__(
        self,
        fn_description="Output a reminder to define this function in a happy way",
        output_format={"output": "sentence"},
        examples=None,
        input_type=None,
        output_type=None,
        **kwargs,
    ):

        # Compulsary variables
        self.fn_description = fn_description
        self.output_format = output_format

        # Optional variables
        self.input_type = input_type
        self.output_type = output_type
        self.examples = examples
        self.kwargs = kwargs

        if self.examples is not None:
            self.fn_description += "\nExamples:\n" + str(examples)

    def __call__(self, *args, **kwargs):
        """Describes the function, and inputs the relevant parameters as either unnamed variables (args) or named variables (kwargs)
        If there is any variable that needs to be strictly converted to a datatype, put mapping function in input_type or output_type

        Inputs:
        - *args: Tuple. Unnamed input variables of the function. Will be processed to var1, var2 and so on based on order in the tuple
        - **kwargs: Dict. Named input variables of the function

        Output:
        - res: Dict. JSON containing the output variables"""

        # Do the merging of args and kwargs
        for num, arg in enumerate(args):
            kwargs["var" + str(num + 1)] = arg

        # Do the input type converstion (optional)
        if self.input_type is not None:
            for key in kwargs:
                if key in self.input_type:
                    try:
                        kwargs[key] = self.input_type[key](kwargs[key])
                    except Exception as e:
                        continue

        # do the function.
        res = enforce_json_structure(
            system_prompt=self.fn_description,
            user_prompt=kwargs,
            output_format=self.output_format,
            **self.kwargs,
        )

        # Do the output type conversion (optional)
        if self.output_type is not None:
            for key in res:
                if key in self.output_type:
                    try:
                        res[key] = self.output_type[key](res[key])
                    except Exception as e:
                        continue

        return res
