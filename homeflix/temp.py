from app import app


@app.get("/temp")
def temp():
    return "this is temp"
