import time
from datetime import datetime

from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from freelance_tasks.models import Project, ProjectOwner, Projects


def normalize_month(date_str):
    months_genitive_to_nominative = {
        "января": "Январь",
        "февраля": "Февраль",
        "марта": "Март",
        "апреля": "Апрель",
        "мая": "Май",
        "июня": "Июнь",
        "июля": "Июль",
        "августа": "Август",
        "сентября": "Сентябрь",
        "октября": "Октябрь",
        "ноября": "Ноябрь",
        "декабря": "Декабрь",
    }

    for genitive, nominative in months_genitive_to_nominative.items():
        date_str = date_str.replace(genitive, nominative)

    return date_str


class HabrParser:
    def __init__(self):
        self.base_url = "https://freelance.habr.com"
        self.tasks_url = f"{self.base_url}/tasks"
        self.link_project = f"{self.tasks_url}/{{id}}"

        self.session = Session()
        retry_strategy = Retry(
            total=1,
            backoff_factor=1,
            status_forcelist=[
                500,
                502,
                503,
                504,
            ],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def parse_projects(self, first_id: int, last_id: int) -> Projects:
        projects = Projects()
        for id in range(first_id, last_id):
            project = self.get_project(id)
            if project is None:
                continue
            projects.items.append(project)
            projects.count += 1
        return projects

    def get_project(self, id: int) -> Project | None:
        try:
            resp = self.session.get(self.link_project.format(id=id))
            print(f"[GET {id}] {resp.status_code=}")
            if not resp.ok:
                return
            soup = BeautifulSoup(resp.text, "lxml")
            project: Project = self.parse_project(id, soup)
            return project
        except Exception as e:
            print(e)
            return None

    def parse_project(self, id: int, soup: BeautifulSoup) -> Project:
        user: ProjectOwner = self.parse_user_project_page(soup)

        title = (
            soup.find("h2", class_="task__title")
            .get_text()
            .replace("\n", " ")
            .strip()
        )

        description = (
            soup.find("div", class_="task__description")
            .prettify()
            .replace('<div class="task__description">', " ")
            .replace("</div>", "")
        )

        tags = [item.text for item in soup.find_all("li", class_="tags__item")]

        try:
            element = (
                soup.find("div", class_="task__finance")
                .find("span", class_="count")
                .get_text()
            )
            price = float(element.split("руб.")[0].strip().replace(" ", ""))
        except Exception:
            price = None

        public_at = normalize_month(
            soup.find("div", class_="task__meta")
            .find(text=True, recursive=False)
            .replace("•", "")
            .strip()
        )

        return Project(
            id=id,
            url=self.link_project.format(id=id),
            title=title,
            description=description,
            public_at=datetime.strptime(public_at, "%d %B %Y, %H:%M"),
            tags=tags,
            price=price,
            owner=user,
        )

    def parse_user_project_page(self, soup) -> ProjectOwner:
        full_name_element = soup.find("div", class_="fullname").find("a")
        tags = [
            item
            for item in soup.find("div", class_="specialization")
            .get_text()
            .split(",")
        ]
        owner = ProjectOwner(
            url=self.base_url + full_name_element["href"],
            username=full_name_element["href"].split("/")[-2],
            full_name=full_name_element.get_text(),
            img=soup.find("img", class_="avatario")["src"],
            tags=tags,
            online_at=datetime.now(),
        )

        return owner

    def parse_all_projects(self):
        project_id = self.get_new_project_id(0)[0]
        projects = self.parse_projects(0, project_id)
        projects += self.wait_new_projects(start_project_id=project_id)

    def wait_new_projects(self, wait=10, project_id=None):
        project_id = project_id or max(self.get_new_project_id(0))
        while True:
            project_ids = self.get_new_project_id(project_id)
            for id in project_ids:
                project = self.get_project(id)
                if project:
                    yield project
            if project_ids:
                project_id = max(project_ids)
            time.sleep(wait)

    def get_new_project_id(self, old_project_id=0) -> list[int] | None:
        try:
            resp = self.session.get(self.tasks_url)
            print(f"[GET ] {resp.status_code=}")
            if resp.ok:
                soup = BeautifulSoup(resp.text, "lxml")
                return self.parse_projects_page(soup, old_project_id)
        except Exception as e:
            print("хабр сломался или не пускает")
            raise e

    def parse_projects_page(
        self,
        soup: BeautifulSoup,
        old_id=0,
    ) -> list[int]:
        ul_element = soup.find("ul", {"id": "tasks_list"})
        titles = ul_element.find_all("div", class_="task__title")
        if not titles:
            raise Exception("No li elements found")
        return [
            int(id_)
            for li in titles
            if (id_ := li.a["href"].split("/")[-1]).isdigit()
            and int(id_) > old_id
        ]
