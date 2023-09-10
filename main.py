from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database
from models import dependant, user, supportTicket, profile, notification, membership, beneficiary, saved_payment, temp_membership
from routers import user as user_router, authentication as authentication_router, supportTicket as support_ticket_router, profile as profile_router, notification as notification_router, membership as membership_router, beneficiary as beneficiary_router, dependant as dependant_router, saved_payment as saved_payment_router, temp_membership as temp_membership_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

user.Base.metadata.create_all(bind=database.engine)
supportTicket.Base.metadata.create_all(bind=database.engine)
profile.Base.metadata.create_all(bind=database.engine)
notification.Base.metadata.create_all(bind=database.engine)
membership.Base.metadata.create_all(bind=database.engine)
beneficiary.Base.metadata.create_all(bind=database.engine)
dependant.Base.metadata.create_all(bind=database.engine)
saved_payment.Base.metadata.create_all(bind=database.engine)
temp_membership.Base.metadata.create_all(bind=database.engine)

# Routers
app.include_router(user_router.router)
app.include_router(authentication_router.router)
app.include_router(profile_router.router)
app.include_router(membership_router.router)
app.include_router(temp_membership_router.router)
app.include_router(beneficiary_router.router)
app.include_router(dependant_router.router)
app.include_router(saved_payment_router.router)
app.include_router(support_ticket_router.router)
app.include_router(notification_router.router)

@app.get("/")
def index():
    return { "details": "EHA Membership API" }
