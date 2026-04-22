from uuid import UUID

from digital_folder.db.models import ProjectUrl
from digital_folder.db.service import DbService
from digital_folder.packages.ProjectUrl.schemas import ProjectUrlCreate, ProjectUrlOut


class ProjectUrlDTO:
    def __init__(self, db: DbService):
        self.db = db

    def create(self, url_data: ProjectUrlCreate, project_id: UUID) -> None:
        """
        Create a new project url.

        Args:
            url_data (ProjectUrlCreate): The project url data.
            project_id (UUID): The parent project ID.
        """

        url_dict = url_data.dict()
        url_dict["url"] = str(url_dict["url"])
        url_dict["project_id"] = project_id
        self.db.create(ProjectUrl, url_dict)

    def delete_all_project_urls(self, project_id: UUID) -> None:
        """
        Delete all urls from a project.

        Args:
            project_id (UUID): The parent project ID.
        """

        urls = self.db.get_all_by_field(
            ProjectUrl, ProjectUrl.project_id, str(project_id)
        )
        for url in urls:
            self.db.delete(ProjectUrl, url.id)

    @staticmethod
    def url_parser(url: ProjectUrl) -> ProjectUrlOut:
        """
        This function takes project url data and turns it into a ProjectUrlOut object.

        Args:
            url (ProjectUrl): The project url data.

        Returns:
            ProjectUrlOut: The parsed project url data.
        """

        parsed_url = {
            "id": url.id,
            "name": url.name,
            "url": url.url,
        }

        return ProjectUrlOut(
            id=parsed_url["id"],
            name=parsed_url["name"],
            url=parsed_url["url"],
        )
