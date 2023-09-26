from flask import Flask,url_for
from worker import celery_init_app

from celery import shared_task
from celery.result import AsyncResult



app = Flask(__name__)

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis",
        result_backend="redis://redis",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }


@app.get("/test_task/<int:a>/<int:b>")
def start_add(a,b) -> dict[str, object]:
    result = add_together.delay(a, b)
    result_url = url_for('task_result',id=result.id)
    return {
        "result_id": result.id,
        "result_url":result_url
    }

if __name__ == '__main__':
    app.run()
