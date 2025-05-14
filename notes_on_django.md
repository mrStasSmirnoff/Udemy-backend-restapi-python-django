FastAPI → Django/DRF Translation Map

| Concept                      | **FastAPI**                                    | **Django / DRF**                                                       |
| ---------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------- |
| Define endpoint              | `@app.get("/path")`                            | `def list(self, request):` inside `ModelViewSet`                       |
| Group routes                 | `APIRouter()`                                  | `DefaultRouter()` + `router.register()`                                |
| Route logic per method       | Explicit per decorator (`@get`, `@post`, etc.) | Implicit via method names (`list`, `create`, etc.)                     |
| Request/response models      | `Pydantic` models (`BaseModel`)                | `Serializers` (`serializers.ModelSerializer`)                          |
| Auto generate CRUD           | No, manual via `@router.get/post/...`          | `ModelViewSet` handles all CRUD out of the box                         |
| Database models              | `SQLAlchemy`                                   | `Django ORM` (`models.Model`)                                          |
| Authenticated user           | `Depends(get_current_user)`                    | `request.user`                                                         |
| Enforce authentication       | `Depends()` + logic                            | `permission_classes = [IsAuthenticated]`                               |
| Set logged-in user on create | `obj.user_id = user.id`                        | `perform_create(self, serializer): serializer.save(user=request.user)` |
| Filter by current user       | `query.filter_by(user_id=user.id)`             | `get_queryset(self): return queryset.filter(user=request.user)`        |
| Test client                  | `TestClient(app)`                              | `APIClient()`                                                          |
| Auth test client             | `headers = {"Authorization": "Bearer ..."}`    | `client.force_authenticate(user=user)`                                 |
| Admin panel                  | Build manually or use a library                | Built-in via `admin.site.register()`                                   |
| Form-based views / templates | Optional add-on (e.g., Jinja2 templates)       | Native in Django (`views`, `render(request, ...)`)                     |



### Mental Models for Django Abstractions
#### ModelViewSet = Controller + Router + Handler + Schema Mapper
```python
class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
```
Equivalent to manually defining:
```python
@router.get("/recipes/")
def list_recipes(): ...

@router.post("/recipes/")
def create_recipe(): ...

@router.get("/recipes/{id}/")
def get_recipe(): ...
```

ModelViewSet wires HTTP methods to internal methods:
- list() → GET /recipes/
- create() → POST /recipes/
- retrieve() → GET /recipes/{id}/
- update() → PUT /recipes/{id}/
- partial_update() → PATCH /recipes/{id}/
- destroy() → DELETE /recipes/{id}/

#### Serializer = Pydantic + Validation + ORM Adapter + Save Logic
```python
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
```
Equivalent to:
```python
class TagSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
```
But also:
- Validates input
- Formats output
- Can .save() or .update() model instances

#### queryset and get_queryset() = Default Query + Optional Dynamic Filter
```python
queryset = Recipe.objects.all()

def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
```

Equivalent to:

```python
db.query(Recipe).filter(Recipe.user_id == user.id)
```
Use get_queryset() when you want to inject dynamic filtering per request/user.

#### perform_create() = Pre-Save Hook
```python
def perform_create(self, serializer):
    serializer.save(user=self.request.user)
```
Equivalent to:
```python
recipe_data = recipe.dict()
recipe_data["user_id"] = user.id
db.add(Recipe(**recipe_data))
```
Hook to attach metadata before saving the object (e.g., current user).

#### permission_classes = Dependency-Based Access Control
```python
permission_classes = [IsAuthenticated]
```
Equivalent to:
```
def endpoint(user: User = Depends(get_current_user)):
```
Applies global or per-view access rules like login required, roles, etc.

#### DRF Router = Route Generator
```python
router = DefaultRouter()
router.register('recipes', RecipeViewSet)
```
Generates:
- GET /recipes/ → list()
- POST /recipes/ → create()
- GET /recipes/{id}/ → retrieve()
- PUT/PATCH /recipes/{id}/ → update(), partial_update()
- DELETE /recipes/{id}/ → destroy()

