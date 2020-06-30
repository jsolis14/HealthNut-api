from app import app


if __name__ == '__main__':
    port = os.environ.get('PORT') or 5000

app.run("0.0.0.0", port=port)
