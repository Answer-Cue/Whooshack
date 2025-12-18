from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from src.WhooPy import Client


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="change-me")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    token = request.session.get("token")
    if token:
        client = Client(access_token=token)
        try:
            info = client.info()
            user = info.get("user", {})
        except Exception:
            user = {}
        return templates.TemplateResponse("map.html", {"request": request, "user": user})
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        client = Client()
        data = client.email_login(email=email, password=password)
    except Exception:
        raise HTTPException(status_code=401, detail="login failed")
    request.session["token"] = data["access_token"]
    return RedirectResponse("/", status_code=302)


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


def get_client(request: Request) -> Client:
    token = request.session.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="not logged in")
    return Client(access_token=token)


@app.post("/update_location")
async def update_location(
    lat: float = Form(...),
    lon: float = Form(...),
    client: Client = Depends(get_client),
):
    client.update_location({"latitude": lat, "longitude": lon})
    return {"status": "ok"}


@app.get("/locations")
async def locations(client: Client = Depends(get_client)):
    return client.get_locations()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

