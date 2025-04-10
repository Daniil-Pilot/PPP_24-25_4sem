import uvicorn

def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()


#### http://127.0.0.1:8000/docs
