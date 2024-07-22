from drf_spectacular.generators import EndpointEnumerator, SchemaGenerator
from drf_spectacular.openapi import AutoSchema


def custom_preprocessing_hook(endpoints):
    filtered = []
    for path, path_regex, method, callback in endpoints:
        # Remove all but DRF API endpoints
        if path.lstrip("/").startswith("api") and "schema" not in path:
            filtered.append((path, path_regex, method, callback))
    return filtered


def route_path_version(path: str) -> str:
    return path.strip("/").split("/")[1]


def custom_postprocessing_hook(result, generator, request, public):
    requested_swagger_version = route_path_version(request.path)

    filtered_result = {
        key: value
        for (key, value) in result["paths"].items()
        if route_path_version(key) == requested_swagger_version
    }
    result["paths"] = filtered_result

    return result


class CustomEndpointEnumerator(EndpointEnumerator):
    def get_allowed_methods(self, callback) -> list:
        if hasattr(callback, "actions"):
            actions = set(callback.actions)
            http_method_names = set(callback.cls.http_method_names)
            methods = [method.upper() for method in actions & http_method_names]
        else:
            methods = callback.cls().allowed_methods

        return [
            method for method in methods if method not in ("HEAD", "TRACE", "CONNECT")
        ]


class CustomSchemaGenerator(SchemaGenerator):
    endpoint_inspector_cls = CustomEndpointEnumerator


class CustomSchema(AutoSchema):
    method_mapping = {
        "get": "retrieve",
        "post": "create",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
        "options": "metadata",
    }
