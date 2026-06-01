from app import create_app

app = create_app()

# Only runs if I'm running this file directly, not if another file imports it
if __name__ == "__main__":
    # starts the Flask server on port 5000
    # `debug=True` means if I change any code, the server automatically restarts so I don't have to stop and start it manually every time
    app.run(debug=True)

