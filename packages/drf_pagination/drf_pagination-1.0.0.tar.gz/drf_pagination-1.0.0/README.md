# drf-paginations
Other paginations based on Django REST framework


![PyPI - Version](https://img.shields.io/pypi/v/drf-patinations)
![PyPI - Downloads](https://img.shields.io/pypi/dw/drf-patinations)

* **Author**: [xcai](https://github.com/xcai/drf-patinations)
* **Version**: 1.0.0
* **License**: MIT

**drf-paginations** is a collections of paginations for Django REST framework. includes: LimitOffsetPaginationForDataTable...    

**drf-paginations** 增加适配前端[Datatable](https://datatables.net/)表格组件的limitoffset分页器，例如LimitOffsetPaginationForDataTable


## Documentation

* Install drf-paginations from PyPI（安装）:
```
        pip install drf-paginations
```
* Import the pagination class into your project（使用）:
```
from drf_pagination.pagination import LimitOffsetPaginationForDataTable
from rest_framework.generics import ListAPIView


class MyStoryListAPIView(ListAPIView):
    ...
    pagination_class = LimitOffsetPaginationForDataTable

```
* Response format data（接口返回数据格式，适配Datatable）:
```json
{
    "draw": 1,
    "recordsTotal": 100,
    "recordsFiltered": 10,
    "data": [
      {...},
      {...}
]}
```

