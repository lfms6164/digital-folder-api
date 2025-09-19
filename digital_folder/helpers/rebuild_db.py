from sqlalchemy.orm import Session

from digital_folder.core.config import project_settings
from digital_folder.db.db import engine, Base, get_db
from digital_folder.db.models import Group, Tag


def rebuild_db():
    are_you_sure = False
    if project_settings.env.lower() == "dev" and are_you_sure:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)

    db: Session = next(get_db())

    try:
        print("Inserting seed data...")

        # Groups
        backend = Group(name="Backend")
        database = Group(name="Database")
        frontend = Group(name="Frontend")
        other = Group(name="Other")
        db.add_all([backend, database, frontend, other])
        db.commit()
        print("Groups created...")

        # Tags
        angular = Tag(name="Angular", icon="angularjs", color="#C4002B", group=frontend)
        c = Tag(name="C", icon="language-c", color="#A4B4C8", group=other)
        cpp = Tag(name="C++", icon="language-cpp", color="#2E609C", group=other)
        csharp = Tag(name="C#", icon="language-csharp", color="#1D9923", group=backend)
        docker = Tag(name="Docker", icon="docker", color="#1D63ED", group=other)
        git = Tag(name="Git", icon="git", color="#F05133", group=other)
        github_actions = Tag(
            name="GitHub Actions", icon="github", color="#000000", group=other
        )
        graphql = Tag(name="GraphQL", icon="graphql", color="#DE33A6", group=other)
        html5 = Tag(
            name="Html5", icon="language-html5", color="#FF7A00", group=frontend
        )
        java = Tag(name="Java", icon="language-java", color="#F29111", group=backend)
        lua = Tag(name="Lua", icon="language-lua", color="#113573", group=backend)
        nodejs = Tag(name="Node.js", icon="nodejs", color="#56A544", group=backend)
        postgresql = Tag(
            name="PostgreSQL", icon="elephant", color="#699DC9", group=database
        )
        python = Tag(
            name="Python", icon="language-python", color="#C6AA0D", group=backend
        )
        react = Tag(name="React", icon="react", color="#61DAFB", group=backend)
        rails = Tag(
            name="Rails", icon="language-ruby-on-rails", color="#D30001", group=backend
        )
        ruby = Tag(name="Ruby", icon="language-ruby", color="#DA3206", group=backend)
        rust = Tag(name="Rust", icon="language-rust", color="#000000", group=backend)
        typescript = Tag(
            name="TypeScript",
            icon="language-typescript",
            color="#00B5FF",
            group=frontend,
        )
        vuejs = Tag(name="Vue", icon="vuejs", color="#41B883", group=frontend)
        vuetify = Tag(name="Vuetify", icon="vuetify", color="#7BC6FF", group=frontend)
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
