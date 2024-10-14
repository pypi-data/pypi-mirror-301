"""
This module provides a service for interacting with Jenkins jobs.
"""

import json
import urllib
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Union


class CyclicDependencyError(Exception):
    """
    Exception raised when a cyclic dependency is detected in the schema.
    """

    pass


class JsonTransformer:
    """
    Transforms and serializes validated data into a structured format suitable for POST requests.
    """

    def __init__(self, transformations: Optional[Dict[str, Any]] = None):
        """
        Initializes the JsonTransformer with optional field-specific transformations.

        Parameters
        ----------
        transformations : Dict[str, Any], optional
            A dictionary mapping field paths to transformation functions, by default None.
        """
        self.transformations: Dict[str, Any] = transformations or {}

    def transform(self, data: Dict[str, Any]) -> str:
        """
        Transforms the input data into a flattened and URL-encoded JSON string.

        Parameters
        ----------
        data : Dict[str, Any]
            The validated and processed data to transform.

        Returns
        -------
        str
            The URL-encoded JSON string ready for a POST request.
        """
        flattened_data = self._flatten_json(data, "root")
        self._apply_transformations(flattened_data)
        self._replace_spaces(flattened_data)
        parameter = self._construct_parameter(flattened_data, data)
        final_json = self._assemble_final_json(parameter)
        return self._url_encode(final_json)

    def _flatten_json(
        self,
        current: Union[Dict, List],
        path: str,
        flattened: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Recursively flattens a nested JSON structure.

        Parameters
        ----------
        current : Union[Dict, List]
            The current level of JSON to flatten.
        path : str
            The current path for the keys.
        flattened : Dict[str, Any], optional
            The dictionary to store flattened key-value pairs, by default None.

        Returns
        -------
        Dict[str, Any]
            The flattened JSON structure.
        """
        if flattened is None:
            flattened = {}

        if isinstance(current, dict):
            for key, value in current.items():
                new_path = f"{path}[{key}]"
                self._flatten_json(value, new_path, flattened)
        elif isinstance(current, list):
            if not current:
                # Empty list, keep as is
                flattened[path] = []
            elif all(isinstance(item, dict) for item in current):
                # List of dictionaries, flatten with indices
                for index, item in enumerate(current):
                    new_path = f"{path}[{index}]"
                    self._flatten_json(item, new_path, flattened)
            else:
                # List of simple types, keep the list
                flattened[path] = [
                    (
                        item.replace(" ", "+")
                        if isinstance(item, str) and " " in item
                        else item
                    )
                    for item in current
                ]
        else:
            # Scalar value
            if isinstance(current, str) and " " in current:
                flattened[path] = current.replace(" ", "+")
            else:
                flattened[path] = current

        return flattened

    def _apply_transformations(self, flattened: Dict[str, Any]):
        """
        Applies field-specific transformations to the flattened data.

        Parameters
        ----------
        flattened : Dict[str, Any]
            The flattened JSON data.
        """
        for key, transform in self.transformations.items():
            if key in flattened:
                flattened[key] = transform(flattened[key])

    def _replace_spaces(self, flattened: Dict[str, Any]):
        """
        Replaces spaces with '+' in all remaining string values within the flattened data.

        Parameters
        ----------
        flattened : Dict[str, Any]
            The flattened JSON data.
        """
        for key, value in flattened.items():
            if isinstance(value, str) and " " in value:
                flattened[key] = value.replace(" ", "+")
            elif isinstance(value, list):
                flattened[key] = [
                    (
                        item.replace(" ", "+")
                        if isinstance(item, str) and " " in item
                        else item
                    )
                    for item in value
                ]

    def _construct_parameter(
        self, flattened: Dict[str, Any], original_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Constructs the 'parameter' dictionary required for the POST request.

        Parameters
        ----------
        flattened : Dict[str, Any]
            The flattened and transformed data.
        original_data : Dict[str, Any]
            The original validated data.

        Returns
        -------
        Dict[str, Any]
            The 'parameter' dictionary with placeholders and data.
        """
        parameter: Dict[str, Any] = {
            "name": "_",
            "": [""] * 45,  # Adjust the number of empty strings as needed
        }

        for key, value in flattened.items():
            parameter[key] = value

        # Add the original JSON as a JSON string under 'value'
        parameter["value"] = json.dumps(original_data)

        return parameter

    def _assemble_final_json(self, parameter: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assembles the final JSON structure required for the POST request.

        Parameters
        ----------
        parameter : Dict[str, Any]
            The 'parameter' dictionary containing the transformed data.

        Returns
        -------
        Dict[str, Any]
            The complete JSON structure for the POST request.
        """
        return {
            "parameter": parameter,
            "redirectTo": ".",
            "": "",
        }

    def _url_encode(self, final_json: Dict[str, Any]) -> str:
        """
        URL-encodes the final JSON structure.

        Parameters
        ----------
        final_json : Dict[str, Any]
            The complete JSON structure for the POST request.

        Returns
        -------
        str
            The URL-encoded JSON string.
        """
        return "json=" + urllib.parse.quote(json.dumps(final_json))


@dataclass
class DependencyGraphBuilder:
    """
    Builds a dependency graph from a JSON schema based on 'watch' properties.

    Attributes
    ----------
    schema : Dict[str, Any]
        The JSON schema from which to build the dependency graph.
    graph : Dict[str, Set[str]]
        The resulting dependency graph.
    """

    schema: Dict[str, Any]
    graph: Dict[str, Set[str]] = field(
        init=False, default_factory=lambda: defaultdict(set)
    )

    def __post_init__(self):
        """
        Constructs the dependency graph upon initialization.
        """
        self._traverse_schema(self.schema.get("properties", {}), "", self.graph)

    def _traverse_schema(
        self, schema: Dict[str, Any], prefix: str, graph: Dict[str, Set[str]]
    ):
        """
        Recursively traverses the schema to populate the dependency graph.

        Parameters
        ----------
        schema : Dict[str, Any]
            The current level of the schema being traversed.
        prefix : str
            The hierarchical prefix representing the current path in the schema.
        graph : Dict[str, Set[str]]
            The dependency graph being populated.
        """
        for key, value in schema.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if "properties" in value:
                self._traverse_schema(value["properties"], full_key, graph)
            if "watch" in value:
                for watched_key in value["watch"].values():
                    graph[watched_key].add(full_key)

    def get_dependency_graph(self) -> Dict[str, Set[str]]:
        """
        Retrieves the constructed dependency graph.

        Returns
        -------
        Dict[str, Set[str]]
            The dependency graph where each key maps to a set of dependent keys.
        """
        return self.graph


@dataclass
class JsonSchemaProcessor:
    """
    Validates and processes input data against a provided JSON schema.

    Attributes
    ----------
    schema : Dict[str, Any]
        The JSON schema used for validation.
    dependency_graph : Dict[str, Set[str]]
        A graph representing dependencies between fields based on 'watch' properties.
    processing_order : List[str]
        The order in which fields should be processed based on dependencies.
    """

    schema: Dict[str, Any]
    dependency_graph: Dict[str, Set[str]] = field(init=False)
    processing_order: List[str] = field(init=False)

    def __post_init__(self):
        """
        Initializes the dependency graph and processing order after dataclass initialization.
        """
        graph_builder = DependencyGraphBuilder(self.schema)
        self.dependency_graph = graph_builder.get_dependency_graph()
        self.processing_order = self._topological_sort()

    def _topological_sort(self) -> List[str]:
        """
        Performs a topological sort on the dependency graph to determine processing order.

        Returns
        -------
        List[str]
            A list of keys sorted based on dependencies.

        Raises
        ------
        CyclicDependencyError
            If a cyclic dependency is detected in the schema.
        """
        visited = set()
        stack = []
        temp_marks = set()

        def dfs(node: str):
            if node in temp_marks:
                raise CyclicDependencyError(
                    f"Cyclic dependency detected at node: {node}"
                )
            if node not in visited:
                temp_marks.add(node)
                for neighbor in self.dependency_graph.get(node, []):
                    dfs(neighbor)
                temp_marks.remove(node)
                visited.add(node)
                stack.append(node)

        for node in self.dependency_graph:
            if node not in visited:
                dfs(node)

        return list(reversed(stack))

    def validate_and_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and processes the input data against the schema.

        Parameters
        ----------
        data : Dict[str, Any]
            The input data to validate and process.

        Returns
        -------
        Dict[str, Any]
            The validated and processed data.

        Raises
        ------
        ValueError
            If the input data does not conform to the schema.
        """
        result: Dict[str, Any] = {}

        for key in self.processing_order:
            self._process_field(key, data, result)

        # Process any remaining fields not covered by dependencies
        self._process_remaining_fields(self.schema.get("properties", {}), data, result)

        return result

    def _process_field(self, key: str, data: Dict[str, Any], result: Dict[str, Any]):
        """
        Processes an individual field, handling templates and validations.

        Parameters
        ----------
        key : str
            The hierarchical key of the field to process.
        data : Dict[str, Any]
            The input data containing the field values.
        result : Dict[str, Any]
            The dictionary where processed fields are stored.
        """
        parts = key.split(".")
        schema_part = self.schema.get("properties", {})
        data_part = data
        result_part = result

        for part in parts[:-1]:
            schema_part = schema_part.get(part, {}).get("properties", {})
            data_part = data_part.get(part, {})
            if part not in result_part:
                result_part[part] = {}
            result_part = result_part[part]

        field_schema = schema_part.get(parts[-1], {})
        field_data = data_part.get(parts[-1])

        if "template" in field_schema:
            result_part[parts[-1]] = self._process_template(field_schema, result)
        elif field_data is not None:
            result_part[parts[-1]] = self._validate_field(field_schema, field_data)
        else:
            result_part[parts[-1]] = self._get_default_value(field_schema)

    def _process_remaining_fields(
        self, schema: Dict[str, Any], data: Dict[str, Any], result: Dict[str, Any]
    ):
        """
        Recursively processes any remaining fields in the schema that haven't been processed.

        Parameters
        ----------
        schema : Dict[str, Any]
            The current level of the schema.
        data : Dict[str, Any]
            The input data corresponding to the current schema level.
        result : Dict[str, Any]
            The dictionary where processed fields are stored.
        """
        for key, value in schema.items():
            if "properties" in value:
                if key not in result:
                    result[key] = {}
                self._process_remaining_fields(
                    value["properties"], data.get(key, {}), result[key]
                )
            elif key not in result:
                if key in data:
                    result[key] = self._validate_field(value, data[key])
                else:
                    result[key] = self._get_default_value(value)

    def _get_default_value(self, field_schema: Dict[str, Any]) -> Any:
        """
        Retrieves the default value for a field based on its schema.

        Parameters
        ----------
        field_schema : Dict[str, Any]
            The schema definition for the field.

        Returns
        -------
        Any
            The default value for the field.
        """
        if "default" in field_schema:
            return field_schema["default"]
        elif "enum" in field_schema:
            return field_schema["enum"][0]  # Use the first enum value as default

        field_type = field_schema.get("type")
        if field_type == "boolean":
            return False
        elif field_type == "integer":
            return 0
        elif field_type == "number":
            return 0.0
        elif field_type == "array":
            return []
        elif field_type == "string":
            return ""
        else:
            return None

    def _validate_field(self, field_schema: Dict[str, Any], value: Any) -> Any:
        """
        Validates and casts a field value based on its schema.

        Parameters
        ----------
        field_schema : Dict[str, Any]
            The schema definition for the field.
        value : Any
            The value to validate and cast.

        Returns
        -------
        Any
            The validated and casted value.

        Raises
        ------
        ValueError
            If the value does not conform to the field's type or enum.
        """
        field_type = field_schema.get("type", "string")

        if value is None:
            return self._get_default_value(field_schema)

        if field_type == "string":
            value = str(value)
            if "enum" in field_schema and value not in field_schema["enum"]:
                raise ValueError(
                    f"Invalid value '{value}' for field with enum {field_schema['enum']}"
                )
            return value
        elif field_type == "integer":
            try:
                return int(value)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid integer value: {value}")
        elif field_type == "number":
            try:
                return float(value)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid number value: {value}")
        elif field_type == "boolean":
            return bool(value)
        elif field_type == "array":
            return self._validate_array(field_schema, value)
        else:
            return value

    def _validate_array(
        self, field_schema: Dict[str, Any], value: List[Any]
    ) -> List[Any]:
        """
        Validates an array-type field.

        Parameters
        ----------
        field_schema : Dict[str, Any]
            The schema definition for the array field.
        value : List[Any]
            The list to validate.

        Returns
        -------
        List[Any]
            The validated list.

        Raises
        ------
        ValueError
            If the input is not a list or if any item fails validation.
        """
        if not isinstance(value, list):
            raise ValueError(f"Expected list, got {type(value)}")

        item_schema = field_schema.get("items", {})
        return [self._validate_field(item_schema, item) for item in value]

    def _process_template(
        self, field_schema: Dict[str, Any], data: Dict[str, Any]
    ) -> str:
        """
        Processes a template string by replacing placeholders with actual data.

        Parameters
        ----------
        field_schema : Dict[str, Any]
            The schema definition containing the template and watch properties.
        data : Dict[str, Any]
            The processed data to use for template replacement.

        Returns
        -------
        str
            The processed template string.
        """
        template_str = field_schema["template"]
        watch = field_schema.get("watch", {})

        for key, path in watch.items():
            placeholder = f"{{{{{key}}}}}"
            replacement = self._resolve_path(path, data)
            if replacement is None:
                replacement = ""
            template_str = template_str.replace(placeholder, str(replacement))

        return template_str

    def _resolve_path(self, path: str, data: Any) -> Any:
        """
        Resolves a dot-separated path in the data dictionary.

        Parameters
        ----------
        path : str
            The dot-separated path string.
        data : Dict[str, Any]
            The data dictionary to traverse.

        Returns
        -------
        Any
            The value found at the specified path, or an empty string if not found.
        """
        parts = path.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return ""
        return current if current is not None else ""
