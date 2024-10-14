import csv
import re
from datetime import datetime, timedelta
from typing import List

from pydantic import Field

from plurally.json_utils import replace_refs
from plurally.models.misc import Table
from plurally.models.node import Node
from plurally.models.source.schedule import ScheduleUnit
from plurally.models.utils import create_dynamic_model


class FormatText(Node):
    ICON = "format"

    class InitSchema(Node.InitSchema):
        """Format text using a template."""

        template: str = Field(
            pattern=r"\{([^{}]+)\}",
            description="Template to format the input text, example: Hello, {name}! I like {food}. Each named variable inside curly braces will be replaced by the corresponding connected value.",
            examples=["Hello, {name}, I like {food}."],
            json_schema_extra={
                "uiSchema": {
                    "errorMessages": {
                        "pattern": "You must provide at least one named variable inside curly braces, for example: Hi my name is {name}."
                    },
                    "ui:widget": "textarea",
                    "ui:placeholder": "Write template here, for example: Hello, my name is {name}.",
                },
            },
        )

    class InputSchema(Node.InputSchema):
        text: str = Field(
            description="Text to format.",
            examples=["Hello, world!"],
            format="textarea",
        )

    class OutputSchema(Node.OutputSchema):
        formatted_text: str = Field(
            description="The text formatted using the template.",
        )

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: InitSchema):
        self._template = init_inputs.template
        super().__init__(init_inputs)

    def _set_schemas(self) -> None:
        # create pydantic model from output_fields
        vars = re.findall(r"{(.*?)}", self.template)
        self.InputSchema = create_dynamic_model(
            "InputSchema", vars, base=Node.InputSchema
        )

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
        self._set_schemas()
        self.tgt_handles = self._get_handles(self.InputSchema, None)

    def forward(self, node_input):
        formatted_text = self.template.format(**node_input.model_dump())
        self.outputs["formatted_text"] = formatted_text

    def serialize(self):
        return {
            "template": self.template,
            "input_schema": replace_refs(self.InputSchema.model_json_schema()),
            **super().serialize(),
        }


class FormatTable(Node):
    ICON = "format"

    class InitSchema(Node.InitSchema):
        """Format a table to text using a template."""

        template: str = Field(
            pattern=r"\{([^{}]+)\}",
            description="Template to format each row, example, every variable should be a table column.",
            examples=["Hello, {name}, I like {food}."],
            json_schema_extra={
                "uiSchema": {
                    "errorMessages": {
                        "pattern": "You must provide at least one named variable inside curly braces, for example: Hi my name is {name}."
                    },
                    "ui:widget": "textarea",
                    "ui:placeholder": "Write template here, for example: Hello, my name is {name}.",
                },
            },
        )
        separator: str = Field(
            "\n",
            description="Separator to use between rows. If unsure, use a new line (default).",
            examples=[", "],
            json_schema_extra={
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": "Write separator here, for example: for example a comma or a new line.",
                },
            },
        )

        prefix: str = Field(
            "",
            description="Prefix to add to the formatted text.",
            examples=["#### This is before the text ####."],
            json_schema_extra={
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": "Write prefix here, for example: #### This is before the text ####.",
                },
            },
        )
        suffix: str = Field(
            "",
            description="Suffix to add to the formatted text.",
            examples=["#### This is after the text ####"],
            json_schema_extra={
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": "Write suffix here, for example: #### This is after the text ####.",
                },
            },
        )

    class InputSchema(Node.InputSchema):
        table: Table = Field(
            description="Table to format.",
        )

    class OutputSchema(Node.OutputSchema):
        formatted_text: str = Field(
            description="The table's content formatted to text.",
        )

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: InitSchema):
        self.template = init_inputs.template.strip()
        self.prefix = init_inputs.prefix
        self.suffix = init_inputs.suffix
        self.separator = init_inputs.separator

        super().__init__(init_inputs)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
        self._set_schemas()
        self.src_handles = self._get_handles(self.OutputSchema, None)

    def forward(self, node_input: InputSchema):
        row_str = []
        for row in node_input.table.data:
            formatted_text = self.template.format(**row)
            row_str.append(formatted_text)
        formatted_text = (
            self.prefix
            + self.separator
            + self.separator.join(row_str)
            + self.separator
            + self.suffix
        )
        self.outputs["formatted_text"] = formatted_text

    def get_necessary_columns(self):
        return re.findall(r"{(.*?)}", self.template)

    def serialize(self):
        return super().serialize() | {
            "template": self.template,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "separator": self.separator,
        }


class CsvToTable(Node):
    ICON = "format"

    class InitSchema(Node.InitSchema):
        """Convert CSV text to a table."""

        delimiter: str = Field(
            ",",
            description="Delimiter to use between columns.",
            examples=[","],
            min_length=1,
        )

    class InputSchema(Node.InputSchema):
        csv: str = Field(
            description="CSV string to convert to a table.",
            examples=["name,age\nAlice,25\nBob,30"],
            format="textarea",
        )

    class OutputSchema(Node.OutputSchema):
        data: Table = Field(
            description="The table converted from the CSV string.",
        )

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: InitSchema):
        self.delimiter = init_inputs.delimiter
        super().__init__(init_inputs)

    def forward(self, node_input: InputSchema):
        data = csv.DictReader(
            node_input.csv.splitlines(),
            delimiter=self.delimiter,
        )
        table = Table(data=data)
        self.outputs["data"] = table

    def serialize(self):
        return super().serialize() | {
            "delimiter": self.delimiter,
        }


class ToTable(Node):
    ICON = "format"

    class InitSchema(Node.InitSchema):
        """Convert inputs to table. For instance, if you have 2 inputs age and name, you can convert them to a table with columns age and name."""

        columns: List[str] = Field(
            title="Columns",
            description="The columns of the table.",
            examples=[["name", "age"]],
        )

    class OutputSchema(Node.OutputSchema):
        data: Table = Field(
            description="The table converted from the inputs.",
        )

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: Node.InitSchema):
        self.columns = init_inputs.columns
        super().__init__(init_inputs)

    def _set_schemas(self) -> None:
        self.InputSchema = create_dynamic_model(
            "InputSchema", self.columns, base=Node.InputSchema
        )

    def forward(self, node_input):
        table = Table(data=[node_input.model_dump(include=self.columns)])
        self.outputs["data"] = table

    def serialize(self):
        return super().serialize() | {
            "columns": self.columns,
            "input_schema": replace_refs(self.InputSchema.model_json_schema()),
        }


class DateTimeManipulate(Node):
    ICON = "format"

    class InitSchema(Node.InitSchema):
        """Manipulate a datetime."""

        to_add_or_subtract: int = Field(
            title="To Add or Subtract",
            description="The number of units to add or subtract (if negative) to the date.",
            examples=[1, -3],
        )
        unit: ScheduleUnit = Field(
            description="The unit of the value to add or subtract to the date.",
            title="Unit",
        )

    class InputSchema(Node.InputSchema):
        date: datetime = Field(
            description="The date to manipulate.",
            format="date-time",
        )

    class OutputSchema(Node.OutputSchema):
        value: datetime = Field(
            description="The date manipulated.",
            format="date-time",
        )

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: Node.InitSchema):
        self.to_add_or_subtract = init_inputs.to_add_or_subtract
        self.unit = init_inputs.unit
        super().__init__(init_inputs)

    def forward(self, node_input: InputSchema):
        self.outputs["value"] = node_input.date + timedelta(
            **{self.unit: self.to_add_or_subtract}
        )

    def serialize(self):
        return super().serialize() | {
            "to_add_or_subtract": self.to_add_or_subtract,
            "unit": self.unit,
        }


class TableToTextSimple(Node):
    ICON = "format"

    class InitSchema(Node.InitSchema):
        """Convert a table to a text simply."""

    class InputSchema(Node.InputSchema):
        table: Table = Field(
            description="Table to convert to text.",
        )

    class OutputSchema(Node.OutputSchema):
        text: str = Field(
            description="The table converted to text.",
        )

    DESC = InitSchema.__doc__

    def forward(self, node_input: InputSchema):
        # we do not know here if the user properly formatted the table and put headers
        # we assume that if there is more than one column, there is a header
        text = ""
        if not node_input.table.is_empty():
            first_row = node_input.table.data[0]
            if len(first_row) == 1:
                text += f"{list(first_row.keys())[0]}\n"
                for row in node_input.table.data:
                    text += f"{list(row.values())[0]}\n"
            else:
                for row in node_input.table.data:
                    for key, value in row.items():
                        text += f"{key}: {value}\n"
                    text += "\n"
        self.outputs["text"] = text


__all__ = [
    "FormatText",
    "FormatTable",
    "TableToTextSimple",
    "CsvToTable",
    "ToTable",
    "DateTimeManipulate",
]
