from fastapi import FastAPI
from controllers import auth_controller
from fastapi.middleware.cors import CORSMiddleware
# Crear la instancia de la aplicación
app = FastAPI()
# Incluir el middleware para permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","UPDATE"],
    allow_headers=["*"],
)
# Incluir los routers (controladores)
app.include_router(auth_controller.router)

# Código para correr la aplicación
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)

