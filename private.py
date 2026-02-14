import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import employMaster_router, bank_router, location_router, ctc_router, pt_mast_router, tax_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employMaster_router.router)
app.include_router(bank_router.router)
app.include_router(location_router.router)
app.include_router(ctc_router.router)
app.include_router(pt_mast_router.router)
app.include_router(tax_router.router)

if __name__ == '__main__':
    uvicorn.run("private:app", host='0.0.0.0',
                port=6002, log_level="info", reload=True)
