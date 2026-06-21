from fastapi import FastAPI

from api.routes import router



app = FastAPI(

    title="RAG Events API",

    description="""
    API REST exposant
    le système RAG événements.
    """,

    version="1.0"
)


app.include_router(router)


#app.include_router(
#    router,
#    prefix="/api"
#)



@app.get("/")
def root():

    return {

        "message":
        "RAG API running"

    }
