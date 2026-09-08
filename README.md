# todo-api

# Task API

A small CRUD API for managing a to-do list, built with **FastAPI** for the
FlyRank Internship — Backend Track, Week 2, Assignment A1.

Tasks are stored **in memory** (a plain Python list) — there is no database
yet, so all data is lost when the server restarts. That's expected at this
stage.

## Requirements

- Python 3.10+

## How to run it

One command, from the project folder:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The server starts on **http://localhost:8000**.

Interactive Swagger docs are available for free at **http://localhost:8000/docs**
(FastAPI generates these automatically — no extra setup).

## Endpoints

| Method | Path          | Description                        | Success | Errors                                       |
| ------ | ------------- | ---------------------------------- | ------- | -------------------------------------------- |
| GET    | `/`           | API info                           | 200     | —                                            |
| GET    | `/health`     | Health check                       | 200     | —                                            |
| GET    | `/tasks`      | List all tasks                     | 200     | —                                            |
| GET    | `/tasks/{id}` | Get one task                       | 200     | 404 if id doesn't exist                      |
| POST   | `/tasks`      | Create a task (`{"title": "..."}`) | 201     | 400 if title missing/empty                   |
| PUT    | `/tasks/{id}` | Update a task's title and/or done  | 200     | 404 if id doesn't exist, 400 if body invalid |
| DELETE | `/tasks/{id}` | Delete a task                      | 204     | 404 if id doesn't exist                      |

All errors return JSON in the shape `{"error": "..."}`.

## Example: curl -i output

```
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
date: Tue, 08 Sep 2026 02:33:58 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

## Trying it in Swagger UI

1. Run the server (see above).
2. Open http://localhost:8000/docs in your browser.
3. Expand any endpoint, click **"Try it out"**, fill in a body if needed, and
   click **Execute**. Try the full cycle: `POST /tasks`, `GET /tasks`,
   `PUT /tasks/{id}`, `DELETE /tasks/{id}`.

**Screenshot:** `swagger.png`

## The mortality experiment

Create a task, restart the server (`Ctrl+C` then run it again), then
`GET /tasks`. The task you created is gone — because it only ever lived in a
Python list in memory, not on disk. This is exactly why Week 3 introduces a
real database.
