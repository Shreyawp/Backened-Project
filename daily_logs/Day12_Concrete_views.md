### Concrete View Classes

This is concise methods that extend to `GenericAPIView` and its Model Mixins
Imported from `rest_framework.generics`

- CreateAPIView --> provides `post` method handler
- ListAPIView & RetrieveAPIView --> provides `get` method handler
- DestroyAPIView --> provides `delete` method handler
- UpdateAPIView --> provides `put` and `patch` method handler

Here, I Used 
ListCreateAPIView --> used for read-write endpoints to repreent a collection of model instances,
provides `put` and `patch` method handler
Its combination of:
`ListCreateAPIView = GenericAPIView + ListModelMixin + CreateModelMixin`

RetrieveUpdateDestroyAPIView --> used for read-write-delete endpoints to represent single model instance.
provides `get`, `put`, `patch` and `delete` methods handlers.

`RetrieveUpdateDestroyAPIView = GenericAPIView + RetrieveModelMixin + UpdateModelMixin + DestroyModelMixin`

```python
class OrderList(generics.ListCreateAPIView):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer
```
