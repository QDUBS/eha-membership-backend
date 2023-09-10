from __future__ import print_function
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os.path
from db.odoo import api
from sqlalchemy.orm import Session
from models import membership
from schemas.user import UserSchema
from schemas.membership import MembershipSchema, ShowMembership
from schemas.membership_field import membership_field, beneficiary_fields, dependants_fields
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/membership",
    tags=["Membership"],
    # responses={404: {"description": "Not found"}},
)

load_dotenv()

Partner = api.env["res.partner"]
Memberships = api.env["eha.membership"]
MembershipBeneficiaries = api.env["eha.membership.beneficiaries"]
MembershipDependents = api.env["eha.membership.dependents"]
Benefits = api.env["eha.membership.plan.benefits"]


class Member(BaseModel):
    membership_name: str


class Beneficiary(BaseModel):
    email: str
    hp_number: str
    membership_name: str
    dob: str


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_membership(request: MembershipSchema, db: Session = Depends(get_db)):
    new_membership = membership.Membership(user_id=request.user_id, primary_holder_id=request.primary_holder_id, membership_id=request.membership_id, state=request.state, name=request.name, start_date=request.start_date, 
                                           end_date=request.end_date, total_beneficiaries=request.total_beneficiaries, total_dependents=request.total_dependents, 
                                           total_qty=request.total_qty, membership_type=request.membership_type, category=request.category, plan=request.plan)
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)

    return new_membership


@router.get('/{id}', response_model=ShowMembership, status_code=status.HTTP_200_OK)
def get_membership(id: str, db: Session = Depends(get_db)):
    single_membership = db.query(membership.Membership).filter(
        membership.Membership.user_id == id).first()

    if not single_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Membership with id of {id} does not exist.")

    return single_membership


@router.post("/corporate")
def get_odoo_membership(req: Member):
    try:
        # initilize membership
        membership = {}
        membership["membership"] = Memberships.search_read(
            [("name", "=", req.membership_name)], membership_field)[0]

        # validate the of membership
        if membership["membership"]["state"] != "confirmed":
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"details": "Membership is not active", "state": "expired"})

        # # get all the beneficiaries related to the membership
        beneficiaries = MembershipBeneficiaries.search_read(
            [("membership_id.name", "=", req.membership_name)], beneficiary_fields)

        dependants = MembershipDependents.search_read(
            [("membership_id.name", "=", req.membership_name)], dependants_fields)

        category = membership["membership"].pop("category_id")
        plan = membership["membership"].pop("plan_id")
        primary_holder = membership["membership"].pop("partner_id")

        membership["membership"]["category"] = {
            "id": category[0], "name": category[1]}
        membership["membership"]["plan"] = {"id": plan[0], "name": plan[1]}
        membership["membership"]["primary_holder"] = {
            "id": primary_holder[0], "name": primary_holder[1]}
        membership["beneficiaries"] = beneficiaries
        membership["dependants"] = dependants

        return membership
    except IndexError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"details": "Not found"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "bad request"})


@router.post("/get-beneficiaries")
def get_odoo_beneficiaries(req: Member):
    try:
        # initilize membership
        membership = {}
        membership["membership"] = Memberships.search_read(
            [("name", "=", req.membership_name)], membership_field)[0]

        # validate the of membership
        if membership["membership"]["state"] != "confirmed":
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"details": "Membership is not active", "state": "expired"})

        # # get all the beneficiaries related to the membership
        beneficiaries = MembershipBeneficiaries.search_read(
            [("membership_id.name", "=", req.membership_name)], beneficiary_fields)

        return beneficiaries
    except IndexError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"details": "Not found"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "bad request"})


@router.post("/get-dependants")
def get_odoo_dependants(req: Member):
    try:
        # initilize membership
        membership = {}
        membership["membership"] = Memberships.search_read(
            [("name", "=", req.membership_name)], membership_field)[0]

        # validate the of membership
        if membership["membership"]["state"] != "confirmed":
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"details": "Membership is not active", "state": "expired"})

        # # get all the dependants related to the membership
        dependants = MembershipDependents.search_read(
            [("membership_id.name", "=", req.membership_name)], dependants_fields)

        return dependants
    except IndexError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"details": "Not found"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "bad request"})


@router.get("/individual")
def get_beneficiary(req: Beneficiary):
    try:
        membership = {}
        # get and validate the partner
        partner = Partner.search_read([("email", "=", req.email), ("hp_number", "=", req.hp_number), ("dob", "=", req.dob)], [
                                      "id", "email", "hp_number",])
        if not partner:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"details": "user or membership not found"})

        found_partner = partner[0]

        membership["membership"] = Memberships.search_read(
            [("name", "=", req.membership_name), ("partner_id.email", "=", req.email), ("partner_id.hp_number", "=", req.hp_number)], membership_field)[0]

        if found_partner['id'] != membership["membership"]["partner_id"][0] or found_partner["hp_number"] != req.hp_number:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"details": "user not found in membership"})

        # validate the state of membership
        if membership["membership"]["state"] != "confirmed":
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"details": "Membership is not active", "state": "expired"})

        membership_id = membership["membership"]["id"]

        # # get all the beneficiaries and dependants related to the membership
        beneficiaries = MembershipBeneficiaries.search_read([("membership_id.name", "=", req.membership_name), (
            "membership_id", "=", membership_id)], beneficiary_fields)

        dependants = MembershipDependents.search_read([("membership_id.name", "=", req.membership_name), (
            "membership_id", "=", membership_id)], dependants_fields)

        # get the related field for proper formatting
        catergory = membership["membership"].pop("category_id")
        plan = membership["membership"].pop("plan_id")
        primary_holder = membership["membership"].pop("partner_id")

        # assign corresponding fields to values
        membership["membership"]["catergory"] = {
            "id": catergory[0], "name": catergory[1]}
        membership["membership"]["plan"] = {"id": plan[0], "name": plan[1]}
        membership["membership"]["primary holder"] = {
            "id": primary_holder[0], "name": primary_holder[1]}
        membership["beneficiaries"] = beneficiaries
        membership["dependants"] = dependants

        return membership
    except IndexError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"details": "not found"})
    except Exception as exec:
        print(exec)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "bad request"})

