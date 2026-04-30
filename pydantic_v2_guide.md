# Pydantic v2 — Vue d'ensemble pratique

## 1. Philosophie en une phrase

Pydantic est un moteur de **validation et de sérialisation de données** basé sur les annotations de type Python. Tu déclares la *forme* attendue des données via des classes typées, et Pydantic se charge à la fois de valider les entrées (parsing strict ou coercitif), de produire des messages d'erreur exploitables, et de sérialiser/désérialiser vers JSON, dict, ou autres formats.

La v2 a été réécrite avec un cœur en Rust (`pydantic-core`), ce qui la rend **5 à 50× plus rapide** que la v1 selon les opérations. Elle introduit aussi une API plus cohérente, mais casse pas mal de choses par rapport à v1 — attention si tu lis du code ancien.

---

## 2. Le cœur : `BaseModel`

```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    signup_date: datetime
    is_active: bool = True  # valeur par défaut

# Validation à l'instanciation
user = User(
    id="42",                          # str → int (coercition)
    name="Alice",
    email="alice@example.com",
    signup_date="2024-03-15T10:30:00" # str ISO → datetime
)

print(user.id)  # 42 (int)
print(user.model_dump())  # dict
print(user.model_dump_json())  # str JSON
```

Points importants :
- Les **annotations de type sont la source de vérité**. Pas de `Field()` magique requis pour les cas simples.
- La validation se fait **à la création** de l'instance (pas paresseusement).
- Par défaut, Pydantic est **coercitif** : `"42"` devient `42` pour un champ `int`. Si tu veux un mode strict, tu peux le configurer.
- Les méthodes principales sont préfixées `model_*` en v2 (`model_dump`, `model_validate`, `model_json_schema`, etc.) — c'est l'un des changements de nommage majeurs vs v1.

---

## 3. Types inclus

### 3.1 Types Python standards (gérés nativement)

Pydantic comprend l'essentiel du `typing` standard :

| Type | Comportement |
|------|--------------|
| `int`, `float`, `str`, `bool` | Validation + coercition par défaut |
| `bytes` | Accepte `bytes` ou `str` (encodé) |
| `list[T]`, `tuple[T, ...]`, `set[T]`, `frozenset[T]` | Collections typées, valide chaque élément |
| `dict[K, V]` | Mapping typé clé/valeur |
| `Optional[T]` / `T \| None` | Champ pouvant être `None` |
| `Union[A, B]` / `A \| B` | Tente de matcher le premier type valide (mode "smart" en v2) |
| `Literal["a", "b"]` | Valeur restreinte à un ensemble fini |
| `Enum` | Valide que la valeur est dans l'enum |
| `datetime`, `date`, `time`, `timedelta` | Parse ISO 8601 et timestamps Unix |
| `UUID` | Parse les UUIDs sous forme str ou bytes |
| `Decimal` | Précision décimale exacte |
| `Path` (pathlib) | Convertit str en `Path` |

### 3.2 Types contraints (le vrai apport métier)

C'est ici que Pydantic dépasse les `dataclass` standard. Tu peux contraindre les valeurs sans écrire de validateur :

```python
from pydantic import BaseModel, Field, PositiveInt, NegativeInt, NonNegativeFloat
from typing import Annotated

class Product(BaseModel):
    # Approche 1 : types préconstruits
    quantity: PositiveInt          # > 0
    discount: NonNegativeFloat     # >= 0
    
    # Approche 2 : Annotated + Field (plus expressive et recommandée en v2)
    name: Annotated[str, Field(min_length=1, max_length=100)]
    price: Annotated[float, Field(gt=0, lt=10000)]
    sku: Annotated[str, Field(pattern=r"^[A-Z]{3}-\d{4}$")]
    tags: Annotated[list[str], Field(min_length=1, max_length=10)]
```

Types numériques préconstruits disponibles : `PositiveInt`, `NegativeInt`, `NonNegativeInt`, `NonPositiveInt`, et leurs équivalents `Float`. Pour aller plus loin, `Field(gt=, ge=, lt=, le=, multiple_of=)`.

Pour les chaînes : `min_length`, `max_length`, `pattern` (regex), `to_lower`, `to_upper`, `strip_whitespace`.

### 3.3 Types spécialisés (réseau, fichier, etc.)

Importables depuis `pydantic` ou `pydantic_networks` selon les versions :

```python
from pydantic import BaseModel, EmailStr, HttpUrl, IPvAnyAddress, AnyUrl, FileUrl
from pydantic import Json
from pydantic_extra_types.phone_numbers import PhoneNumber  # paquet séparé
from pydantic_extra_types.payment import PaymentCardNumber  # paquet séparé

class Contact(BaseModel):
    email: EmailStr              # nécessite `pip install pydantic[email]`
    website: HttpUrl             # valide une URL HTTP/HTTPS
    api_endpoint: AnyUrl         # n'importe quelle URL bien formée
    server_ip: IPvAnyAddress     # IPv4 ou IPv6
    raw_config: Json             # accepte une str JSON et la parse automatiquement
```

À noter : certains types autrefois inclus en v1 (numéros de téléphone, cartes bancaires, codes pays, couleurs, ULID...) sont déplacés dans le paquet séparé `pydantic-extra-types` en v2. C'est un choix délibéré pour réduire la surface du paquet principal.

### 3.4 Types "secrets" (anti-fuite)

```python
from pydantic import BaseModel, SecretStr, SecretBytes

class DatabaseConfig(BaseModel):
    host: str
    password: SecretStr  # n'apparaît pas dans repr() ni model_dump() par défaut

config = DatabaseConfig(host="localhost", password="hunter2")
print(config)  # password=SecretStr('**********')
print(config.password.get_secret_value())  # "hunter2" — accès explicite requis
```

Utile pour éviter de leak des credentials dans les logs ou les traces d'erreur. Ne te dispense pas d'une vraie gestion de secrets (vault, variables d'environnement chiffrées), mais c'est une couche de défense raisonnable.

### 3.5 Types stricts

Si tu veux désactiver la coercition pour un champ donné :

```python
from pydantic import BaseModel, StrictInt, StrictStr, StrictBool

class StrictModel(BaseModel):
    count: StrictInt  # "42" sera rejeté, seul 42 (int) passe
    name: StrictStr
    active: StrictBool
```

Tu peux aussi activer le mode strict globalement via `model_config = ConfigDict(strict=True)`.

---

## 4. Validators : logique de validation custom

### 4.1 `field_validator` — validation au niveau d'un champ

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str
    age: int

    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("username doit être alphanumérique")
        return v.lower()  # tu peux aussi transformer la valeur

    @field_validator("age")
    @classmethod
    def age_must_be_realistic(cls, v: int) -> int:
        if v > 150:
            raise ValueError("âge irréaliste")
        return v
```

Modes : `mode="before"` (avant la validation de type) ou `mode="after"` (par défaut, après).

### 4.2 `model_validator` — validation transverse

Quand la validation dépend de plusieurs champs :

```python
from pydantic import BaseModel, model_validator
from typing_extensions import Self

class DateRange(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_range(self) -> Self:
        if self.start >= self.end:
            raise ValueError("start doit être strictement inférieur à end")
        return self
```

---

## 5. Serializers : contrôler la sortie

Symétrique des validators, pour transformer la donnée à la sérialisation :

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    occurred_at: datetime

    @field_serializer("occurred_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%d/%m/%Y %H:%M")  # format français au lieu d'ISO
```

Tu peux aussi exclure des champs au dump : `model.model_dump(exclude={"password"})` ou `exclude_none=True`, `exclude_unset=True`, `by_alias=True`...

---

## 6. Computed fields

Champs calculés à partir d'autres champs, qui apparaissent à la sérialisation :

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

r = Rectangle(width=3, height=4)
print(r.model_dump())  # {'width': 3.0, 'height': 4.0, 'area': 12.0}
```

---

## 7. Configuration : `ConfigDict`

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(
        strict=True,                  # désactive la coercition
        extra="forbid",               # rejette les champs inconnus (sinon "ignore" ou "allow")
        frozen=True,                  # immuable après création
        str_strip_whitespace=True,    # strip auto sur tous les str
        populate_by_name=True,        # accepte le nom du champ même si un alias existe
        json_schema_extra={"example": {"name": "Alice"}},
    )
    name: str
```

`extra="forbid"` est particulièrement utile pour les API : tu détectes les fautes de frappe côté client au lieu de les ignorer silencieusement.

---

## 8. `pydantic-settings` : gestion de configuration

Paquet séparé (`pip install pydantic-settings`) qui était intégré en v1 sous le nom `BaseSettings`. Lit automatiquement depuis variables d'environnement, fichiers `.env`, etc. :

```python
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
    )
    
    debug: bool = False
    database_url: PostgresDsn
    secret_key: SecretStr
    allowed_hosts: list[str] = ["localhost"]

settings = AppSettings()  # lit APP_DEBUG, APP_DATABASE_URL, APP_SECRET_KEY...
```

C'est une alternative crédible à `python-decouple` ou à la config Django classique pour la partie "settings typés et validés au démarrage". À considérer sérieusement si tu en as marre des `os.environ.get()` éparpillés.

---

## 9. Cas d'usage concrets

### 9.1 Validation de payload d'API externe

Tu consommes une API tierce (Stripe, Github, météo...) et tu veux valider/typer la réponse plutôt que manipuler des `dict` opaques :

```python
import httpx
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class GithubRepo(BaseModel):
    id: int
    name: str
    full_name: str
    html_url: HttpUrl
    description: str | None
    stargazers_count: int
    created_at: datetime

response = httpx.get("https://api.github.com/repos/pydantic/pydantic")
repo = GithubRepo.model_validate(response.json())
print(repo.stargazers_count)  # int garanti, pas un Any
```

Bénéfice : autocomplétion IDE, détection précoce si l'API change de format, code plus lisible que `data["stargazers_count"]`.

### 9.2 Webhooks entrants

Stripe, Github, Slack t'envoient des payloads JSON complexes. Pydantic les valide à la frontière de ton système :

```python
from pydantic import BaseModel, Field
from typing import Literal

class StripeEvent(BaseModel):
    id: str
    type: Literal["payment_intent.succeeded", "payment_intent.failed", "charge.refunded"]
    api_version: str
    created: int
    data: dict  # à raffiner selon le type d'événement

# Dans une vue Django
def stripe_webhook(request):
    try:
        event = StripeEvent.model_validate_json(request.body)
    except ValidationError as e:
        return HttpResponseBadRequest(e.json())
    # ... logique métier avec event typé
```

### 9.3 Configuration applicative

Voir section 8 — alternative typée à `settings.py`.

### 9.4 DTO de domaine, séparés de l'ORM Django

Si tu fais du DDD ou que tu veux découpler ta logique métier de Django, Pydantic peut servir de couche "objets de transfert" entre tes services :

```python
from pydantic import BaseModel
from decimal import Decimal

class OrderDTO(BaseModel):
    customer_id: int
    items: list["OrderItemDTO"]
    total: Decimal
    
    @classmethod
    def from_orm_order(cls, order):
        return cls(
            customer_id=order.customer_id,
            items=[OrderItemDTO.model_validate(item, from_attributes=True) for item in order.items.all()],
            total=order.total,
        )

class OrderItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # autorise model_validate sur des objets ORM
    product_id: int
    quantity: int
    unit_price: Decimal
```

`from_attributes=True` (anciennement `orm_mode` en v1) permet à Pydantic de lire directement depuis les attributs d'un objet (instance Django) au lieu d'un dict.

### 9.5 django-ninja

Si tu commences un nouveau projet d'API en Django, **django-ninja** (inspiré de FastAPI) utilise Pydantic comme schémas natifs. Tu remplaces les serializers DRF par des `Schema` Pydantic :

```python
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class UserIn(Schema):
    username: str
    email: str

class UserOut(Schema):
    id: int
    username: str

@api.post("/users", response=UserOut)
def create_user(request, payload: UserIn):
    user = User.objects.create(**payload.dict())
    return user
```

Si tu hésites entre DRF et django-ninja, l'argument Pydantic est solide : moins de boilerplate, validation plus expressive, perf supérieure, doc OpenAPI auto. Le contre-argument : DRF a 10+ ans de stabilité et un écosystème (permissions, throttling, viewsets, browsable API) plus mature.

---

## 10. Limites et points critiques

Quelques choses qu'on lit rarement dans les tutos :

**Le coût de la coercition implicite.** Par défaut, `"42"` devient `42`. C'est pratique pour les API, mais ça peut masquer des bugs en interne. Je recommande `strict=True` pour les modèles internes et la coercition seulement aux frontières (entrée API).

**La duplication avec les modèles Django.** Si tu utilises Pydantic *en plus* des `models.Model` Django, tu te retrouves vite avec deux représentations de la même entité. Soit tu acceptes cette duplication explicitement (modèles ORM = persistance, modèles Pydantic = transport/domaine), soit tu génères l'un à partir de l'autre (`django-pydantic` et autres bibliothèques tierces existent, qualité variable).

**Migration v1 → v2.** Si tu hérites d'une codebase v1, la migration n'est pas triviale : changement de noms de méthodes, de validators, de config, abandon de certains types. Pydantic fournit `bump-pydantic` pour automatiser une partie, mais prévois du temps.

**Performance vs `dataclass`.** Pydantic v2 est rapide, mais reste plus lent qu'une `dataclass` simple ou un `NamedTuple` pour la création d'objets *sans* validation. Si tu n'as pas besoin de valider, n'utilise pas Pydantic.

**Messages d'erreur.** Excellents par défaut (chemin du champ, valeur reçue, contrainte violée), mais le format JSON n'est pas toujours adapté à un affichage utilisateur final. Prévois une couche de traduction si tu exposes les erreurs à l'UI.

**Ce n'est pas un ORM.** Pydantic ne persiste rien, ne gère pas de relations bidirectionnelles, pas de migrations. Toute comparaison avec SQLAlchemy ou Django ORM est un faux débat — ce sont des outils complémentaires, pas concurrents. (À noter : `SQLModel` de Tiangolo combine Pydantic + SQLAlchemy si ce mariage t'intéresse.)

---

## 11. Quand ne pas utiliser Pydantic

Pour rester intellectuellement honnête :

- **Données purement internes, non sérialisées, sans validation requise** → `dataclass` ou `NamedTuple` suffit, plus léger.
- **Projet Django REST classique avec DRF déjà en place et fonctionnel** → ajouter Pydantic crée de la friction sans bénéfice clair. Reste sur les Serializers.
- **Calculs intensifs sur des objets Pydantic** → l'overhead de validation à la création peut peser. Crée tes objets une fois, manipule-les ensuite.
- **Tu maîtrises mal le `typing` Python** → Pydantic devient frustrant, ses messages d'erreur supposent que tu comprends `Annotated`, `Union`, `Generic`. Investis d'abord dans `typing` puis reviens.

---

## Ressources

- Documentation officielle : <https://docs.pydantic.dev>
- Guide migration v1 → v2 : <https://docs.pydantic.dev/latest/migration/>
- Paquet `pydantic-extra-types` : <https://github.com/pydantic/pydantic-extra-types>
- `pydantic-settings` : <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>
- django-ninja : <https://django-ninja.dev>
