import contextlib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.admin import admin as base_admin
from app.routers import *
from app.backend.session import create_all_table

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173",
]

description = """
Authenticated App. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
* **Update users** (_not implemented_).
* **Delete users** (_not implemented_).

* **Register users** (_not implemented_).
"""


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_table()
    yield


app = FastAPI(
    title="Authenticated App",
    description=description,
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    root_path="/v1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers.users import router as users_router

app.include_router(users_router, tags=["user"], prefix="/users")
app.include_router(auth_router, tags=["auth"], prefix="/auth")
base_admin.mount_to(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=4)
