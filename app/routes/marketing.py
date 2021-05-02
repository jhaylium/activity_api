from fastapi import APIRouter
from app.models import mktg_subscription
from traceback import format_exc

router = APIRouter()


@router.get("/linkedin")
async def prospect():
    prospects = mktg_subscription.get_linkedin_prospects()
    return prospects

@router.post("/linkedin")
async def prospect(event: mktg_subscription.Prospect):
    try:
        body = {
                "name": event.name,
                "title": event.title,
                "company": event.company,
                "company_size": event.company_size
                }
        mktg_subscription.add_member_to_linkedin(body=body)
        return (0,body)
    except Exception:
        return (-1, format_exc())



@router.post("/mailinglist")
async def prospect(email: str):
    new_account = mktg_subscription.add_member_to_mailing_list_chimp(email=email,
                                                               list_id='a6c3a9acff')
    mktg_subscription.add_member_to_mailing_list_db(email)
    return new_account

@router.get("/mailinglist")
async def prospect():
    prospects = mktg_subscription.get_mailing_list()
    return prospects