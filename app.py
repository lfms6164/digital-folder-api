import uvicorn

from digital_folder.core.config import project_settings

if __name__ == "__main__":
    env = project_settings.env.lower()

    uvicorn.run(
        "digital_folder.main:create_app",
        host="127.0.0.1" if env == "dev" else "0.0.0.0",
        port=project_settings.port,
        reload=(env == "dev"),
        reload_dirs=["digital_folder"] if env == "dev" else [],
        factory=True,
    )
