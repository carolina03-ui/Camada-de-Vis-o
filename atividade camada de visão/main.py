from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from service.event_service import EventService
from models.event import Event

app = FastAPI()

# Configuração do Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    events = EventService.get_all_events()
    return templates.TemplateResponse("index.html", {"request": request, "events": events})

@app.get("/add", response_class=HTMLResponse)
async def add_event(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "event": None})

@app.post("/create")
async def create_event(id: int = Form(...), name: str = Form(...), date: str = Form(...)):
    EventService.create_event(id, name, date)
    return RedirectResponse("/", status_code=303)


@app.get("/edit/{event_id}", response_class=HTMLResponse)
async def edit_event(request: Request, event_id: int):
    event = EventService.search_event(event_id)
    if not event:
        return templates.TemplateResponse("index.html", {"request": request, "message": "Evento não encontrado"})
    
    return templates.TemplateResponse("form.html", {"request": request, "event": event})

@app.post("/update/{event_id}")
async def update_event(
    event_id: int,
    id: int = Form(...),
    name: str = Form(...),
    date: str = Form(...)
):
    event = EventService.search_event(event_id)
    
    if not event:
        raise HTTPException(status_code=404, detail=f"Evento com ID {event_id} não encontrado.")
    
    event = EventService.update_event(event_id, id, name, date)

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{event_id}")
async def delete_event(event_id: int):
    EventService.delete_event(event_id)
    return RedirectResponse("/", status_code=303)
