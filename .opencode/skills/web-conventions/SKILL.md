---
name: web-conventions
description: |
  Professional web development conventions for FastAPI + Vue 3 projects.
  Covers project structure, naming, coding standards, code quality tooling,
  git conventions, security, and performance best practices.

  Use this skill to:
  - Structure FastAPI backends with proper layering (router/service/repository)
  - Write Vue 3 SFCs with Composition API, Pinia stores, and composables
  - Apply consistent naming and file organization
  - Set up linting, formatting, and pre-commit hooks
  - Follow security and performance best practices
  - Write conventional commits and manage git workflow
---

<objective>
Provide a comprehensive, battle-tested set of conventions for professional web development projects using FastAPI (Python) + Vue 3 (JavaScript/TypeScript). These conventions prioritize consistency, maintainability, testability, and team scalability.

Tech stack covered:
- **Backend**: FastAPI, Pydantic v2, SQLite/SQLAlchemy, openpyxl, Uvicorn
- **Frontend**: Vue 3 (Composition API, `<script setup>`), Pinia, Vue Router, Ant Design Vue, Vite, Axios, Chart.js
</objective>

<context>
This skill is designed for the Excel Data Entry System project at `excel_project/`. The project is a full-stack application for importing, managing, and visualizing Excel data with a FastAPI backend and Vue 3 frontend. Apply these conventions consistently across all new code and refactoring efforts.
</context>

<process>
1. Read this skill before starting any coding task
2. Apply the relevant section based on whether you're working on backend or frontend
3. Run linting/formatting tools before committing (see Code Quality section)
4. Follow git conventions for all commits
5. For Phase 3 refactoring, reference the `.planning/phases/03-refactor-code/` plans for domain-driven structure
</process>

---

# 1. General Principles

## 1.1 Consistency Over Cleverness
- Write boring, predictable code. Clever code is satisfying to write but painful to maintain.
- Every file in the same category should look and feel the same.
- If a pattern exists in the codebase, mirror it — don't introduce a new style unless refactoring the whole area.

## 1.2 Single Responsibility
- Each function, component, module, and service should have exactly one clear purpose.
- A function that does two things should be split into two functions.
- A component that fetches data, transforms it, and renders UI is doing three jobs — split them.

## 1.3 DRY (Don't Repeat Yourself)
- Extract repeated logic into shared functions, composables, or services.
- Avoid premature abstraction — wait until a pattern repeats three times before extracting.

## 1.4 Readability First
- Code is written for humans first, machines second.
- Use meaningful names: `getUserById()` not `getData()`.
- Comment the **why**, not the **what**. The code itself should explain what it does.
- Keep functions short — if a function needs scrolling to follow, split it.

## 1.5 Fail Fast, Fail Loud
- Validate inputs at the boundary (Pydantic for API, props for components).
- Configuration errors should crash at startup, not mid-request.
- Never silently swallow errors — log them properly.

---

# 2. Project Structure

## 2.1 Backend Structure

```
backend/
  main.py                  # App factory + lifespan + router registration
  config.py                # Pydantic Settings (typed config)
  db.py                    # Database connection management (SQLite)
  schemas.py               # Pydantic request/response models
  routes/                  # Thin HTTP layer — one file per domain
    __init__.py
    records.py
    goi.py
    upload.py
    dashboard.py
  services/                # Business logic — no HTTP details
    __init__.py
    excel_service.py
    records_service.py
    goi_service.py
  repositories/            # (optional) Data access layer — CRUD only
```

### Rules:
- **Routers are thin**: Only handle request parsing and response formatting. No business logic.
- **Services own business logic**: Testable without HTTP context. No direct DB access — use repositories.
- **Repositories own data access**: Pure CRUD operations. Swap DB without touching services.
- **Schemas are the contract**: Separate input models (`RecordCreate`) from output models (`RecordResponse`). Never return ORM objects directly.

## 2.2 Frontend Structure

```
frontend/src/
  main.js                  # App bootstrap: register plugins
  App.vue                  # Root layout + navigation
  style.css                # Global styles + Ant Design overrides
  router/
    index.js               # Route definitions
  stores/                  # Pinia stores
    dataStore.js
  services/
    api.js                 # Axios instance + all API calls
  components/              # Feature components
    Dashboard.vue
    DataEntryForm.vue
    DataTable.vue
    GoiManager.vue
  composables/             # (future) Shared reactive logic
  assets/                  # Static assets (images, icons)
```

### Refactoring Target (Phase 3):
```
frontend/src/
  components/
    dashboard/             # Feature-based grouping
      Dashboard.vue
      StatsCards.vue
      RevenueChart.vue
    data-entry/
      DataEntryForm.vue
      BasicInfoSection.vue
      ServiceSection.vue
      FinancialSection.vue
    data-table/
      DataTable.vue
    goi-manager/
      GoiManager.vue
      GoiFormModal.vue
  stores/
    dataStore.js           # (split into) formStore.js, recordStore.js, goiStore.js
  composables/
    useFormCalculations.js
    useExcelUpload.js
```

---

# 3. Backend Conventions (FastAPI)

## 3.1 Async vs Sync

| Scenario | Use | Reason |
|----------|-----|--------|
| I/O-bound with async library (httpx, async DB driver) | `async def` | Await non-blocking calls |
| Synchronous library (openpyxl, sqlite3) | `def` | FastAPI offloads to threadpool |
| CPU-intensive | `def` + task queue | GIL prevents async benefit |
| Mixed sync + async I/O | `def` | Safest default when unsure |

**Golden rule**: Use `async def` only when you truly `await` inside. A blocking call inside `async def` freezes the entire event loop.

## 3.2 Pydantic Models

```python
# schemas.py

# Input model — what the client sends
class RecordCreate(BaseModel):
    model_config = {"extra": "forbid"}  # Reject unexpected fields
    ho_ten: str = Field(..., min_length=1, max_length=100)
    sdt: Optional[str] = None
    # ...

# Output model — what the API returns (never expose internal fields)
class RecordResponse(BaseModel):
    stt: int
    ho_ten: str
    sdt: Optional[str] = None
    ngay_tao: Optional[str] = None
    # ...
```

### Rules:
- **Always separate input and output models**. Never use the same model for both.
- Input models use `extra="forbid"` to reject unexpected fields.
- Output models **never** include password hashes, internal IDs, or secrets.
- Use `Field()` constraints (`min_length`, `max_length`, `ge`, `le`) for boundary validation.
- Prefer `Optional[str]` over `str | None` for consistency with existing code.

## 3.3 Dependency Injection

```python
from fastapi import Depends, APIRouter
from typing import Annotated

# Define dependency
def get_db():
    conn = db.get_conn()
    try:
        yield conn
    finally:
        conn.close()

# Use with Annotated (FastAPI 0.95+)
DbDep = Annotated[sqlite3.Connection, Depends(get_db)]

@router.get("/records")
def list_records(db: DbDep):
    return records_service.get_all(db)
```

### DI Tiers:
| Tier | How | Scope | Use Case |
|------|-----|-------|----------|
| Global | `FastAPI(dependencies=[...])` | All endpoints | API key validation, common headers |
| Router | `APIRouter(dependencies=[...])` | Feature group | Admin auth, tenant resolution |
| Decorator | `@router.get(..., dependencies=[Depends(...)])` | Single endpoint | Rate limiting, permission check |
| Parameter | `param: DbDep` | Single endpoint | Using return value (DB session, current user) |

**Decision**: Does the handler body use the return value? → Yes: Parameter DI. No: Decorator/Global/Router DI.

## 3.4 Router/Service/Repository Layering

```python
# routes/records.py — THIN
@router.get("/records")
def list_records(db: DbDep):
    records = records_service.get_all(db)
    return records

# services/records_service.py — BUSINESS LOGIC
def get_all(db: sqlite3.Connection) -> list[dict]:
    return db.execute("SELECT * FROM records ORDER BY stt").fetchall()

def add_record(db: sqlite3.Connection, record: RecordCreate) -> int:
    # Business rules live here
    next_stt = _get_next_stt(db)
    db.execute("INSERT INTO records (stt, ...) VALUES (?, ...)", (next_stt, ...))
    return next_stt
```

### Rules:
- Router never contains `SELECT`, `INSERT`, or business conditions.
- Service never references `Request`, `Response`, or HTTP concepts.
- Do not introduce repositories unless CRUD logic becomes complex enough to warrant it (YAGNI).

## 3.5 Error Handling

```python
# Structured error response
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, message: str, code: str, status: int = 400):
        self.message = message
        self.code = code
        self.status = status

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status,
            content={"error": {"message": exc.message, "code": exc.code}}
        )

    @app.exception_handler(Exception)
    async def general_handler(request: Request, exc: Exception):
        # Log full traceback internally
        return JSONResponse(
            status_code=500,
            content={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}}
        )
```

### Rules:
- **4xx**: Return immediately with clear message (client can fix).
- **5xx**: Return generic message + log full details. Never expose stack traces to client.
- Always return structured JSON errors, not raw strings.

## 3.6 Configuration

```python
# config.py — Use Pydantic Settings (not os.getenv scattered everywhere)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    spreadsheet_id: str = ""
    sheet1_name: str = "Sheet1"
    service_account_file: str = "service-account.json"
    use_local_fallback: bool = True
    local_excel_file: str = "../data.xlsx"
    template_file: str = "../template/template.xlsx"
    debug: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Rules:
- One typed settings object, loaded once at startup via `@lru_cache`.
- Never use `os.getenv` directly in application code.
- Configuration crashes at startup if required values are missing.

## 3.7 App Factory Pattern

```python
# main.py — Use factory instead of global `app`
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield

def create_app() -> FastAPI:
    app = FastAPI(title="Excel Data Entry API", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
    app.include_router(records_router, prefix="/api")
    app.include_router(goi_router, prefix="/api")
    app.include_router(upload_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")
    register_exception_handlers(app)
    return app

app = create_app()
```

### Benefits:
- Fresh app per test — no global state contamination between tests.
- Easy to override dependencies in tests via `app.dependency_overrides`.
- All assembly visible in one place.

---

# 4. Frontend Conventions (Vue 3)

## 4.1 File Naming

| What | Convention | Example |
|------|-----------|---------|
| SFC component | `PascalCase.vue` | `UserCard.vue` |
| View/route component | `*View.vue` or feature name | `Dashboard.vue` |
| Composable | `useCamelCase.js` | `useFormCalculations.js` |
| Pinia store | `camelCase.js` | `dataStore.js` |
| API service module | `camelCase.js` | `api.js` |
| Test file | `*.spec.js` colocated | `DataEntryForm.spec.js` |

## 4.2 SFC Structure

Always use `<script setup>` for new components:

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDataStore } from '@/stores/dataStore'

const props = defineProps({
  record: { type: Object, default: null }
})

const emit = defineEmits(['save', 'cancel'])

const store = useDataStore()
const loading = ref(false)

const isValid = computed(() => props.record?.ho_ten?.length > 0)

async function handleSave() {
  loading.value = true
  try {
    await store.saveRecord(props.record)
    emit('save')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  store.loadDropdowns()
})
</script>

<template>
  <a-form @submit="handleSave">
    <a-form-item label="Họ tên">
      <a-input v-model:value="props.record.ho_ten" />
    </a-form-item>
    <a-button type="primary" :loading="loading" @click="handleSave">
      Lưu
    </a-button>
  </a-form>
</template>

<style scoped>
.form { max-width: 600px; }
</style>
```

### Section Order (within `<script setup>`):
1. Imports
2. `defineProps` / `defineEmits`
3. Store instances
4. Local state (`ref`, `reactive`)
5. `computed`
6. Functions / methods
7. Lifecycle hooks (`onMounted`, `onBeforeUnmount`)

### When NOT to use `<script setup>`:
- Components that need `name` for recursive references
- Components with complex render functions instead of templates

## 4.3 Reactivity Primitives

### Prefer `ref` over `reactive`

```javascript
// ✅ GOOD — ref works for everything
const count = ref(0)
const user = ref({ name: 'John', age: 30 })

// ✅ ref auto-unwraps in <script setup> template
// Template: {{ count }} not {{ count.value }}

// ❌ AVOID — reactive breaks on destructuring
const state = reactive({ count: 0, name: 'John' })
const { count } = state  // count is NOT reactive
```

### Rules:
- `ref` for everything (primitives AND objects) — consistent, no destructuring footgun.
- `reactive` only when team convention explicitly requires it (avoid in new code).
- `shallowRef` for large, immutable data structures (10k+ rows) to avoid deep reactivity overhead.
- `computed` for derived state — never put logic in template expressions.
- `watch` only for side effects (async operations, DOM updates). Use `computed` for derived values.

## 4.4 Composable Conventions

```javascript
// composables/useFormCalculations.js
import { ref, computed } from 'vue'

export function useFormCalculations(form) {
  // State
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const tongTien = computed(() => {
    return (form.value.tongTienBaoLuu || 0) + (form.value.tongTienBuoiDay || 0)
  })

  const ngayKetThuc = computed(() => {
    if (!form.value.ngayBatDau || !form.value.tongSoThang) return ''
    // calculation logic...
    return ''
  })

  // Methods
  function reset() {
    loading.value = false
    error.value = null
  }

  // Lifecycle
  onBeforeUnmount(() => {
    // Cleanup timers, listeners, etc.
  })

  return {
    loading,
    error,
    tongTien,
    ngayKetThuc,
    reset
  }
}
```

### Rules:
- Name: `useCamelCase()`.
- Take refs as input, return refs as output.
- Clean up side effects in `onBeforeUnmount`.
- One composable = one concern (SRP).
- No UI-specific logic (no toasts, no DOM access).
- Keep composables pure — makes them easy to test with Vitest.

## 4.5 Pinia Store Conventions

Use **composition stores** (not options stores) to match `<script setup>` style:

```javascript
// stores/dataStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchAllRecords, createRecord, updateRecord, deleteRecord } from '@/services/api'

export const useDataStore = defineStore('data', () => {
  // State
  const records = ref([])
  const loading = ref(false)

  // Getters (computed)
  const activeRecords = computed(() =>
    records.value.filter(r => r.tinhTrang !== 'Het han')
  )

  // Actions
  async function loadRecords() {
    loading.value = true
    try {
      records.value = await fetchAllRecords()
    } finally {
      loading.value = false
    }
  }

  async function saveRecord(record) {
    if (record.stt) {
      await updateRecord(record.stt, record)
    } else {
      await createRecord(record)
    }
    await loadRecords()  // Reload after save
  }

  return { records, loading, activeRecords, loadRecords, saveRecord }
})
```

### When to use Pinia vs Composables:
| Scenario | Solution |
|----------|----------|
| State needed globally (auth, theme) | Pinia store |
| Complex multi-step actions needing tracking | Pinia store |
| State only needed by 1-2 related components | Shared composable |
| Local component state | `ref()` in component |

## 4.6 Props, Emits, Slots Typing

```vue
<script setup>
// Props — use defineProps with type literals or interfaces
const props = defineProps({
  record: { type: Object, default: null },
  disabled: { type: Boolean, default: false }
})

// Emits — use defineEmits
const emit = defineEmits({
  save: (record) => record?.ho_ten?.length > 0,  // Validator
  cancel: () => true
})

// Slots — useRenderSlot or template
</script>
```

### Rules:
- Define all props explicitly with types and defaults.
- Never mutate props directly — use `defineModel` (Vue 3.4+) or emit events.
- Validate emits with optional validators.

## 4.7 Ant Design Vue Conventions

### UI Library: Ant Design Vue 4.x
- All components use `a-` prefix: `a-table`, `a-form`, `a-modal`, `a-button`.
- Grid system: `a-row` + `a-col` for layout.
- Forms: always wrap fields in `a-form-item` with proper labels.
- Locale: app already imports `vi_VN` locale — use `a-config-provider` for date pickers, etc.

### Form Patterns
```vue
<template>
  <a-form :model="form" layout="vertical">
    <a-row :gutter="16">
      <a-col :span="12">
        <a-form-item label="Họ tên" required>
          <a-input v-model:value="form.ho_ten" placeholder="Nhập họ tên" />
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item label="Số điện thoại">
          <a-input v-model:value="form.sdt" />
        </a-form-item>
      </a-col>
    </a-row>
  </a-form>
</template>
```

### Table Patterns
```vue
<a-table
  :dataSource="records"
  :columns="columns"
  :pagination="{ pageSizeOptions: ['10', '20', '50', '100'], showSizeChanger: true }"
  :scroll="{ x: 3000 }"
  rowKey="stt"
  :loading="loading"
>
  <template #bodyCell="{ column, record }">
    <template v-if="column.key === 'action'">
      <a-button type="link" @click="editRecord(record)">Sửa</a-button>
      <a-button type="link" danger @click="deleteRecord(record)">Xóa</a-button>
    </template>
  </template>
</a-table>
```

## 4.8 API Service Layer

```javascript
// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Records
export const fetchAllRecords = () => api.get('/records').then(r => r.data)
export const createRecord = (data) => api.post('/records', data).then(r => r.data)
export const updateRecord = (stt, data) => api.put(`/records/${stt}`, data).then(r => r.data)
export const deleteRecord = (stt) => api.delete(`/records/${stt}`)

// Goi
export const fetchGoiList = () => api.get('/goi').then(r => r.data)

// Upload
export const previewUpload = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload/preview', formData).then(r => r.data)
}
```

### Rules:
- One API function per endpoint, named clearly.
- All base URL and auth configuration in the Axios instance.
- Error handling at the component/store level, not in api.js (unless global interceptor).

## 4.9 Eliminate Template Repetition with `v-for`

When templates contain repeated blocks with the same structure (stat cards, form fields, table columns), use `v-for` with a configuration array to DRY them up.

### Pattern: Extract field configs to an array

```vue
<script setup>
const statCards = [
  { title: 'Doanh thu', valueKey: 'totalRevenue', formatMoney: true },
  { title: 'Hợp đồng', valueKey: 'totalContracts' },
  { title: 'Đang hoạt động', valueKey: 'activeContracts', valueStyle: { color: '#3f8600' } },
  { title: 'Hết hạn', valueKey: 'expiredContracts', valueStyle: { color: '#cf1322' } },
  { title: 'Khách hàng', valueKey: 'totalCustomers' },
  { title: 'Gói tập', valueKey: 'totalPackages' },
]
</script>

<template>
  <a-col v-for="s in statCards" :key="s.valueKey">
    <a-statistic :title="s.title" :value="stats[s.valueKey]" :value-style="s.valueStyle" />
  </a-col>
</template>
```

### Pattern: Form fields with different input types

```vue
<script setup>
const formRows = [
  [
    { key: 'maGoi', label: 'Mã gói', span: 12 },
    { key: 'clb', label: 'CLB', span: 12 },
  ],
  [
    { key: 'loaiThe', label: 'Loại thẻ', span: 8 },
    { key: 'maGoiHoatDong', label: 'Mã gói hoạt động', span: 8 },
    { key: 'phanBo', label: 'Phân bổ', span: 8 },
  ],
]

const moneyFields = [
  { key: 'tongTien', label: 'Tổng tiền', span: 3, disabled: true },
  { key: 'mucUuDai', label: 'Mức ưu đãi (%)', span: 3, editable: true, props: { min: 0, max: 100 } },
]
</script>

<template>
  <a-row v-for="(row, ri) in formRows" :key="ri" :gutter="16">
    <a-col v-for="f in row" :key="f.key" :span="f.span">
      <a-form-item :label="f.label">
        <a-input-number v-if="f.type === 'number'" v-model:value="form[f.key]" v-bind="f.props" />
        <a-input v-else v-model:value="form[f.key]" />
      </a-form-item>
    </a-col>
  </a-row>
</template>
```

### Guidelines:
- Only refactor when 3+ identical blocks exist (YAGNI — don't over-abstract 2 items).
- Keep field configs simple — if the config becomes harder to read than the original template, stop.
- Use `:key` for stable identity (use a unique field, not array index for reorderable lists).
- Place config arrays close to the template in `<script setup>` for easy reference.
- Define formatter/parser functions once and reuse them across fields (e.g., `formatMoney`, `formatPercent`).
- ❌ Don't put `computed()` refs inside plain arrays — reactivity breaks. Keep computed at the top level or use `reactive()` container.

## 4.10 Anti-Patterns (Avoid)

### Frontend:
- ❌ `<script>` without `setup` for new Vue 3 components.
- ❌ Mixing Options API and Composition API in same component.
- ❌ Destructuring `reactive()` objects without `toRefs()`.
- ❌ Mutating props directly — use `defineModel` or emit.
- ❌ Logic in template expressions (`{{ items.filter(...).map(...) }}`) — extract to computed.
- ❌ `v-html` without sanitization.
- ❌ Forgetting `:key` on `v-for`, or using index as key for reorderable lists.
- ❌ Using `process.env.X` — use `import.meta.env.VITE_*` (Vite convention).
- ❌ Over-abstracting — don't use `v-for` for 1-2 items. Wait until the 3rd repetition.

### Backend:
- ❌ Returning ORM/dict objects directly from endpoints — always use response model.
- ❌ Blocking calls inside `async def` routes.
- ❌ One massive `main.py` — split by domain.
- ❌ Hardcoded secrets/config — use Pydantic Settings + `.env`.
- ❌ Stack traces in production error responses.

---

# 5. Code Quality Tools (Recommended Setup)

## 5.1 Backend — Ruff

```ini
# pyproject.toml (backend/)
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "ARG"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Commands**:
```bash
ruff check .          # Lint
ruff format .         # Format
ruff check --fix .    # Auto-fix
```

## 5.2 Frontend — ESLint + Prettier

```json
// .eslintrc.cjs
module.exports = {
  root: true,
  env: { browser: true, es2022: true, node: true },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
  ],
  parser: 'vue-eslint-parser',
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/require-default-prop': 'warn',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
  }
}
```

```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

## 5.3 Pre-commit Hooks (Husky + lint-staged)

```json
// package.json (root or frontend)
{
  "lint-staged": {
    "*.{js,vue}": ["eslint --fix", "prettier --write"],
    "*.py": ["ruff check --fix", "ruff format"]
  }
}
```

## 5.4 VSCode Settings

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "always"
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "files.associations": {
    "*.vue": "vue"
  }
}
```

---

# 6. Git Conventions

## 6.1 Commit Messages (Conventional Commits)

```
<type>(<scope>): <short summary>

[optional body — explain WHY, not what]
```

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `style` | Formatting, linting (no logic change) |
| `docs` | Documentation only |
| `chore` | Tooling, deps, CI config |
| `test` | Adding/updating tests |

**Examples**:
```
feat(api): add record upload endpoint with Excel preview
fix(data-entry): correct ngayKetThuc calculation for leap years
refactor(backend): split sheets_service into domain services
chore: configure ruff + eslint for code quality
```

## 6.2 Branch Strategy
- `main` — production-ready, protected
- Feature branches: `feat/<description>` or `phase-03/<plan-name>`
- Bug fixes: `fix/<short-description>`

---

# 7. Security Best Practices

## 7.1 Backend
- **Validate all inputs**: Pydantic handles type coercion and constraints. Use `extra="forbid"` on input models.
- **Never hardcode secrets**: API keys, DB paths, passwords → `.env` + Pydantic Settings.
- **CORS**: Restrict `allow_origins` in production (not `["*"]`).
- **SQL injection**: Already prevented by using parameterized queries (`execute("...", (val,))` vs f-strings).
- **Error responses**: Never return stack traces or internal exception messages to clients.
- **HTTPS**: Terminate TLS at reverse proxy (Nginx/Caddy).

## 7.2 Frontend
- **v-html**: Never use with user-supplied content (XSS risk).
- **API tokens**: Never store in `localStorage` — use `HttpOnly` cookies.
- **Dependencies**: Run `npm audit` regularly. Fix critical vulnerabilities immediately.
- **Ant Design sanitization**: The library handles XSS prevention — but be careful with custom HTML rendering.

---

# 8. Performance Best Practices

## 8.1 Backend
- **N+1 queries**: Avoid querying the DB in a loop — batch operations where possible.
- **Connection management**: SQLite connections should be short-lived. Open per request, close after.
- **Heavy work**: Offload Excel parsing, report generation to `BackgroundTasks` or a task queue.

## 8.2 Frontend
- **Lazy loading**: Route-based code splitting via dynamic imports (Vue Router already supports this).
- **shallowRef**: Use for large datasets (10k+ records) to skip deep reactivity.
- **v-once / v-memo**: Static content → `v-once`. Long lists → `v-memo` with specific deps.
- **v-for + :key**: Always provide a stable `:key` (not index for reorderable lists).
- **Bundle size**: Keep critical JS under ~200KB. Lazy-load chart.js and other heavy libs.
- **Ant Design imports**: Import only needed components instead of `app.use(Antd)` (tree-shaking may handle this partially).

---

# 9. Testing Conventions

## 9.1 Backend Testing
```python
# tests/test_records.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_list_records():
    response = client.get("/api/records")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_record():
    response = client.post("/api/records", json={"ho_ten": "Test User"})
    assert response.status_code == 200
```

### Testing Layers:
| Layer | Scope | Speed |
|-------|-------|-------|
| Unit (service) | Business logic with mocked DB | Fast |
| Integration (route) | Real DB, real deps | Medium |
| E2E | Full stack via Playwright | Slow (few tests) |

## 9.2 Frontend Testing
- Composables: Test with `@vue/test-utils` + Vitest.
- Components: Test user behavior (click, input, form submit) — not implementation details.
- Use `data-testid` attributes for stable selectors (avoid CSS class selectors).

---

# 10. Quick Reference Checklist

## Before writing code:
- [ ] File naming follows conventions
- [ ] Component/service has single responsibility
- [ ] Props/Methods named clearly (not ambiguous)

## Before committing:
- [ ] Run linter (`ruff check` / `eslint .`)
- [ ] Run formatter (`ruff format` / `prettier --write`)
- [ ] No hardcoded secrets, no `console.log` / `print()`
- [ ] Commit message follows Conventional Commits

## Before deploying:
- [ ] CORS restricted in production
- [ ] Docs/OpenAPI disabled or auth-protected
- [ ] HTTPS configured
- [ ] `.env` values set for production
- [ ] Error responses don't leak internals
