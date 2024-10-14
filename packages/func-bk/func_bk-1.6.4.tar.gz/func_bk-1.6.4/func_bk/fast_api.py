from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.utils import generate_unique_id
from typing import Any, Callable, Dict, List, Type, Union
from enum import Enum

from markupsafe import Markup
from pydantic import BaseModel


def path(
        app: FastAPI,
        func: callable,
        type: str,
        path: str,
        response_model: Any = None,
        status_code: int = None,
        tags: List[Union[str, Enum]] = None,
        dependencies = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses = None,
        deprecated: bool = None,
        operation_id = None,
        response_model_include = None,
        response_model_exclude = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: type[Response] = JSONResponse,
        name: str = None,
        callbacks = None,
        openapi_extra = None,
        generate_unique_id_function = generate_unique_id
    ):
    type = type.lower()
    route_function = None
    if type == "get":
        route_function = app.get
    elif type == "post":
        route_function = app.post
    elif type == "put":
        route_function = app.put
    elif type == "delete":
        route_function = app.delete
    elif type == "patch":
        route_function = app.patch

    if route_function:
        route_function(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function
        )(func)



def parse_data(cls: Type):
    def decorator(func: Callable):
        async def wrapper(request: Request):
            try:
                data = await request.json()
                instance = cls(**data)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
            return await func(instance)
        return wrapper
    return decorator

class MetaBaseData(type):
    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if callable(value) and not key.startswith("__"):
                annotations = dct.get("__annotations__", {})
                if key in annotations:
                    dct[key] = parse_data(annotations[key])(value)
        return super().__new__(cls, name, bases, dct)

class BaseData(metaclass=MetaBaseData):
    pass





class Label(BaseData):
    type: str
    id: str
    placeholder: str
    help_text: str
    style_input:str
    label: str
    none:bool
    def __init__(self, type:str, id:str, place:str = "", help:str = "", style:str = None,label:str = '', none:bool = False):
        self.type=type
        self.id=id
        self.placeholder=place
        self.help_text=help
        self.style_input=style
        self.label = label
        self.none=none

class BForm(BaseData):
    def labels(self) -> List[Label]:
        a=[]
        cls=type(self)
        for i in cls.__dict__:
            if isinstance(cls.__dict__[i], Label):
                a.append(cls.__dict__[i])   
        return a
    def Dlabels(self) -> Dict[str, Any]:
        return {label.id: {'value': label.value, 'required': label.required} for label in self.labels()}

    def as_p(self):
        a=''
        all=self.labels()

        for i in all:
            if i.label:
                a+=f'<label for="{i.id}">{i.label}</label> \n'
            
            if not(i.style_input):
                a += f"<input type='{i.type}' id='{i.id}' name='{i.id}' placeholder='{i.placeholder}' "
            else:
                a += f"<input class='{i.style_input}' type='{i.type}' id='{i.id}' name='{i.id}' placeholder='{i.placeholder}' "
            
            if not(i.none):
                a += 'required'

            a += f"> {i.help_text} \n"
        return Markup(a)
    def upgrade_value(self):
            a="""
            <script>
            document.addEventListener("DOMContentLoaded", function() {
                function handleFormSubmit(event) {
                    event.preventDefault(); // Предотвратить отправку формы
                    var formData = new FormData(event.target); // Получить данные формы
                    var formIndex = Array.from(document.forms).indexOf(event.target); // Получить индекс текущей формы

                    // Найти соответствующий объект BForm по индексу формы
                    var form = forms[formIndex];
                    if (form) {
                        formData.forEach(function(value, key) {
                            // Найти соответствующий объект Label в метках формы
                            var label = form.labels().find(function(item) {
                                return item.id === key;
                            });
                            if (label) {
                                // Обновить атрибуты объекта Label
                                label.value = value;
                            }
                        });
                    }
                }

                Array.from(document.forms).forEach(function(form) {
                    form.addEventListener('submit', handleFormSubmit);
                });
            });
            </script>
            """
            return Markup(a)
    def is_valid(self):
        errors = {}
        all_labels = self.Dlabels()
        for field_name, field_data in all_labels.items():
            field_value = field_data['value']
            required = field_data['required']
            if required and not field_value:
                errors[field_name] = "Это обязательное поле"
        if errors:
            return False, errors
        return True, None


