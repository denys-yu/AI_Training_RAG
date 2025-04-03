from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import rag_service
import vector_db

app = FastAPI()

@app.on_event("startup")
async def check_db():
    if vector_db.collection_is_empty():
        print("⚠️ Увага: Векторна БД порожня. Запусти 'init_db.py' для заповнення.")

HTML_PAGE = """
<html>
<body>
<h2>RAG чат 🇺🇦</h2>
<form method="post">
<input type="text" name="query" style="width:70%;" />
<button type="submit">Надіслати</button>
</form>
{% if query %}
<hr>
<strong>Питання:</strong> {{ query }}<br>
<strong>Відповідь:</strong> {{ answer }}<br>
<strong>Документи:</strong> {{ sources }}<br>
{% endif %}
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_PAGE.replace("{% if query %}...{% endif %}", "")

@app.post("/", response_class=HTMLResponse)
async def handle_query(request: Request):
    form = await request.form()
    query = form["query"]
    answer, sources = rag_service.answer_question(query)
    sources_text = ", ".join(set(sources))
    html = HTML_PAGE.replace("{{ query }}", query).replace("{{ answer }}", answer).replace("{{ sources }}", sources_text)
    return html.replace("{% if query %}", "").replace("{% endif %}", "")

