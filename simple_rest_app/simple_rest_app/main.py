import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()

# Таблица в оперативной памяти
table = []

# Словарь для хранения сессий
sessions = {}

# Счётчики
counter = 0
transaction_id = 0

# Генерация уникального идентификатора
async def get_new_id():
    global counter
    counter = counter + 1
    return counter

# Генерация уникального идентификатора транзакции
async def generate_transaction_id():
    global transaction_id
    transaction_id = transaction_id + 1
    return transaction_id

# Middleware для создания fingerprint и идентификатора сессии
async def gen_session_fingerprint(request: Request):
    fingerprint_headers = [
        'user-agent',
        'accept-language'
    ]
    fingerprint_data = "-".join([request.headers.get(header, '') for header in fingerprint_headers])
    fingerprint = hash(fingerprint_data.encode())
    session_id = fingerprint
    return session_id
# Роут для получения всей таблицы
@app.get("/select")
async def select():
    return table

# Роут для добавления записи в таблицу
@app.post("/insert")
async def insert(request: Request):
    payload = await request.json()
    value = payload.get('value')
    session_id = await gen_session_fingerprint(request)
    if sessions.get(session_id):
        item = await add_transaction(session_id, "insert", value)
        return {"message": f"{item} added to transaction"}
    else:
        new_id = await get_new_id()
        new_item = {"id": new_id, "value": value}
        table.append(new_item)
        return new_item

# Роут для удаления записи из таблицы по id
@app.delete("/delete/{id}")
async def delete(id: int, request: Request):
    session_id = await gen_session_fingerprint(request)
    if sessions.get(session_id):
        is_open = await transaction_is_open(session_id)
        if is_open:
            item = await add_transaction(session_id, "delete", id)
            return {"message": f"{item} added to transaction"}
    else:
        record = next((item for item in table if item["id"] == id), None)
        if record:
            table.remove(record)
            return {"message": "Record deleted successfully"}
        else:
            return {"message": "Record not found"}

# Функция для проверки, открыта ли транзакция для данной сессии
async def transaction_is_open(session_id):
    session = sessions.get(session_id)
    if session:
        return len(session["transactions"]) > 0
    return False

# Функция для добавления действия в транзакцию
async def add_transaction(session_id, action_type, action_value):
    session = sessions.get(session_id)
    if session:
        transaction = session["transactions"][-1]
        new_action = {'type': action_type, 'value': action_value}
        transaction['actions'].append(new_action)
        return new_action
    return {"message": "Session not found"}

# Роут для открытия транзакции
@app.post("/begin")
async def begin_transaction(request: Request):
    session_id = await gen_session_fingerprint(request)
    if sessions.get(session_id) is None:
        sessions[session_id] = {"fingerprint": session_id, "transactions": []}
    session = sessions.get(session_id)
    transaction_id = await generate_transaction_id()
    session["transactions"].append({"id": transaction_id, "actions": []})
    return {"message": "Transaction opened"}

# Роут для закрытия транзакции и выполнения изменений
@app.post("/commit")
async def commit_transaction(request: Request):
    session_id = await gen_session_fingerprint(request)
    session = sessions.get(session_id)
    if session:
        for transaction in session["transactions"]:
            for action in transaction['actions']:
                action_type = action['type']
                action_value = action['value']
                if action_type == "insert":
                    new_id = await get_new_id()
                    table.append({"id": new_id, "value": action_value})
                elif action_type == "delete":
                    record = next((item for item in table if item["id"] == action_value), None)
                    if record:
                        table.remove(record)
        sessions.pop(session_id)
        return {"message": "Transaction committed successfully"}
    return {"message": "Session not found"}

# Роут для отката транзакции
@app.post("/rollback")
async def rollback_transaction(request: Request):
    session_id = await gen_session_fingerprint(request)
    session = sessions.get(session_id)
    if session:
        sessions.pop(session_id)
        return {"message": "Transaction rolled back successfully"}
    return {"message": "Session not found"}


def run():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("simple_rest_app.main:app", host="0.0.0.0", port=8080, reload=True)
