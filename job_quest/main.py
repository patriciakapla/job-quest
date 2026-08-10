from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def main():
    print('Oh, hi! This is job-quest :)')
    return {'message': 'Oh, hi! This is job-quest :)'}
