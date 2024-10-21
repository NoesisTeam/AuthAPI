from fastapi import FastAPI
from controllers import auth_controller

# Crear la instancia de la aplicación
app = FastAPI()

# Incluir los routers (controladores)
app.include_router(auth_controller.router)

# Código para correr la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

