import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "digital_folder.main:create_app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        reload_dirs=["digital_folder"],
        factory=True,
    )
