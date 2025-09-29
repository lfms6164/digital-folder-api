from passlib.hash import bcrypt

from digital_folder.core.config import project_settings
from digital_folder.db.db import Base, engine, SessionLocal
from digital_folder.db.models import Group, Tag, User, UserRole


def rebuild_db():
    are_you_sure = False
    is_dev_env = project_settings.env.lower() == "dev"

    if is_dev_env and are_you_sure:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)

    populate_db = True
    if populate_db:
        db = SessionLocal()
        try:
            print("Inserting seed data...")

            # Users
            admin = User(
                username="df_admin",
                password=bcrypt.hash("df_admin"),
                role=UserRole.ADMIN,
            )
            user = User(
                username="df_user",
                password=bcrypt.hash("df_user"),
                role=UserRole.USER,
            )
            viewer = User(
                username="df_viewer",
                password=bcrypt.hash("df_viewer"),
                role=UserRole.VIEWER,
            )
            db.add_all([admin, user, viewer])
            db.commit()
            print("Users created...")

            created_by = admin.id
            if created_by:
                # Groups
                backend = Group(name="Backend", created_by=created_by)
                database = Group(name="Database", created_by=created_by)
                frontend = Group(name="Frontend", created_by=created_by)
                other = Group(name="Other", created_by=created_by)
                db.add_all([backend, database, frontend, other])
                db.commit()
                print("Groups created...")

                # Tags
                angular = Tag(
                    name="Angular",
                    icon="angularjs",
                    color="#C4002B",
                    group=frontend,
                    created_by=created_by,
                )
                c = Tag(
                    name="C",
                    icon="language-c",
                    color="#A4B4C8",
                    group=other,
                    created_by=created_by,
                )
                cpp = Tag(
                    name="C++",
                    icon="language-cpp",
                    color="#2E609C",
                    group=other,
                    created_by=created_by,
                )
                csharp = Tag(
                    name="C#",
                    icon="language-csharp",
                    color="#1D9923",
                    group=backend,
                    created_by=created_by,
                )
                docker = Tag(
                    name="Docker",
                    icon="docker",
                    color="#1D63ED",
                    group=other,
                    created_by=created_by,
                )
                git = Tag(
                    name="Git",
                    icon="git",
                    color="#F05133",
                    group=other,
                    created_by=created_by,
                )
                github_actions = Tag(
                    name="GitHub Actions",
                    icon="github",
                    color="#000000",
                    group=other,
                    created_by=created_by,
                )
                graphql = Tag(
                    name="GraphQL",
                    icon="graphql",
                    color="#DE33A6",
                    group=other,
                    created_by=created_by,
                )
                html5 = Tag(
                    name="Html5",
                    icon="language-html5",
                    color="#FF7A00",
                    group=frontend,
                    created_by=created_by,
                )
                java = Tag(
                    name="Java",
                    icon="language-java",
                    color="#F29111",
                    group=backend,
                    created_by=created_by,
                )
                lua = Tag(
                    name="Lua",
                    icon="language-lua",
                    color="#113573",
                    group=backend,
                    created_by=created_by,
                )
                nodejs = Tag(
                    name="Node.js",
                    icon="nodejs",
                    color="#56A544",
                    group=backend,
                    created_by=created_by,
                )
                postgresql = Tag(
                    name="PostgreSQL",
                    icon="elephant",
                    color="#699DC9",
                    group=database,
                    created_by=created_by,
                )
                python = Tag(
                    name="Python",
                    icon="language-python",
                    color="#C6AA0D",
                    group=backend,
                    created_by=created_by,
                )
                react = Tag(
                    name="React",
                    icon="react",
                    color="#61DAFB",
                    group=frontend,
                    created_by=created_by,
                )
                rails = Tag(
                    name="Rails",
                    icon="language-ruby-on-rails",
                    color="#D30001",
                    group=backend,
                    created_by=created_by,
                )
                ruby = Tag(
                    name="Ruby",
                    icon="language-ruby",
                    color="#DA3206",
                    group=backend,
                    created_by=created_by,
                )
                rust = Tag(
                    name="Rust",
                    icon="language-rust",
                    color="#000000",
                    group=backend,
                    created_by=created_by,
                )
                typescript = Tag(
                    name="TypeScript",
                    icon="language-typescript",
                    color="#00B5FF",
                    group=frontend,
                    created_by=created_by,
                )
                vuejs = Tag(
                    name="Vue",
                    icon="vuejs",
                    color="#41B883",
                    group=frontend,
                    created_by=created_by,
                )
                vuetify = Tag(
                    name="Vuetify",
                    icon="vuetify",
                    color="#7BC6FF",
                    group=frontend,
                    created_by=created_by,
                )
                db.add_all(
                    [
                        angular,
                        c,
                        cpp,
                        csharp,
                        docker,
                        git,
                        github_actions,
                        graphql,
                        html5,
                        java,
                        lua,
                        nodejs,
                        postgresql,
                        python,
                        react,
                        rails,
                        ruby,
                        rust,
                        typescript,
                        vuejs,
                        vuetify,
                    ]
                )
                db.commit()
                print("Tags created...")
        finally:
            db.close()
            print("rebuild_db complete!")


if __name__ == "__main__":
    rebuild_db()
