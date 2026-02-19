from FastAPI import APIRouter
from FastAPI.middleware.cors import CORSMiddleware

router = APIRouter()

origins = [
   "http://[IP_ADDRESS]",
   "http://localhost",
   "http://localhost:3000",
   "http://localhost:8080",
]

router.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)