import requests
from django.core.management.base import BaseCommand
from chat.models import Agent


class Command(BaseCommand):
    help = 'Load agents from GitHub repository'

    GITHUB_API_URL = (
        "https://api.github.com/repos/"
        "danielmiessler/Fabric/contents/data/patterns"
    )
    RAW_BASE_URL = (
        "https://raw.githubusercontent.com/"
        "danielmiessler/Fabric/main/data/patterns"
    )

    def handle(self, *args, **kwargs):
        response = requests.get(self.GITHUB_API_URL)

        if response.status_code != 200:
            self.stdout.write(
                self.style.ERROR("Failed to fetch pattern folders from GitHub")
            )
            return

        folders = [
            item["name"]
            for item in response.json()
            if item["type"] == "dir"
        ]

        for folder in folders:
            try:
                system_md_url = f"{self.RAW_BASE_URL}/{folder}/system.md"
                md_response = requests.get(system_md_url)

                if md_response.status_code != 200:
                    self.stdout.write(
                        self.style.WARNING(f"No system.md found for {folder}")
                    )
                    continue

                system_prompt = md_response.text

                # Category = first token, name = rest
                parts = folder.split("_")
                category = parts[0].capitalize()
                name = " ".join(parts[1:]).title() if len(parts) > 1 else folder.title()

                agent, created = Agent.objects.update_or_create(
                    folder_name=folder,
                    defaults={
                        "name": name,
                        "category": category,
                        "system_prompt": system_prompt,
                        "description": f"Agent for {name.lower()}",
                    },
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created agent: {agent.name}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Updated agent: {agent.name}")
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error loading {folder}: {str(e)}")
                )
