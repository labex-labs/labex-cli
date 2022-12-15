import os
import json
from rich.prompt import Prompt
from rich import print


class Create:
    """Create a new lab or challenge
    """

    def __init__(self) -> None:
        self.lab_type = Prompt.ask(
            "Select Lab Type", choices=["lab", "challenge"], default="lab"
        )
        self.lab_title = Prompt.ask("Enter Lab Title (e.g. Hello World)").title()
        self.lab_slug = f'{self.lab_type}-{self.lab_title.lower().replace(" ", "-")}'
        self.lab_diff = Prompt.ask(
            "Select Lab Difficulty",
            choices=["Beginner", "Intermediate", "Advanced"],
            default="Beginner",
        )
        self.lab_time = Prompt.ask("Enter Lab Time", default="5 minutes")
        self.lab_steps = int(Prompt.ask("Enter Number of Steps", default="3"))
        self.lab_image_id = Prompt.ask(
            "Select Image ID",
            choices=["vnc-ubuntu:2004", "webide-ubuntu:2004"],
            default="vnc-ubuntu:2004",
        )
        self.if_assets = Prompt.ask(
            "Does it contain pictures or other attachments?",
            choices=["yes", "no"],
            default="yes",
        )

    def init_step(self, step_index: int):
        """Initialize a step

        Args:
            step_index (int): lab step index

        Returns:
            _type_: step config
        """
        # step index.json config template
        step_config = {
            "title": "Please replace this text with the title of the step",
            "text": f"step{step_index}.md",
            "verify": [
                {
                    "name": "Please replace this text with the target of the verify script",
                    "file": f"verify{step_index}.sh",
                    "hint": "Please replace this text with the hint of the verify script",
                    "timeout": 0,
                    "showstderr": False,
                }
            ],
            "skills": ["Please copy the skill ID from the official skill tree"],
        }
        # create step file
        step_file = open(f"{self.lab_slug}/step{step_index}.md", "w")
        step_file.write(f"# Step {step_index} Title")
        # create verify file
        verify_file = open(f"{self.lab_slug}/verify{step_index}.sh", "w")
        verify_file.write("#!/bin/zsh")
        return step_config

    def check_if_exists(self):
        if os.path.exists(self.lab_slug):
            print("[red]✕[/red] Lab Title already exists, please choose another one.")
            exit(1)
        else:
            os.mkdir(self.lab_slug)
            print(f"[green]✓[/green] {self.lab_slug} is created.")

    def init_base(self):
        # create folder
        self.check_if_exists()
        # create basic files
        intro_file = open(f"{self.lab_slug}/intro.md", "w")
        intro_file.write(f"# {self.lab_title}")
        finish_file = open(f"{self.lab_slug}/finish.md", "w")
        finish_file.write(f"# Summary")
        setup_file = open(f"{self.lab_slug}/setup.sh", "w")
        setup_file.write("#!/bin/zsh")
        # base index.json config template
        base_config = {
            "type": self.lab_type,
            "title": self.lab_title,
            "description": "",
            "difficulty": self.lab_diff,
            "time": self.lab_time,
            "details": {
                "steps": [],
                "intro": {"text": "intro.md", "background": "setup.sh"},
                "finish": {"text": "finish.md"},
            },
            "backend": {"imageid": self.lab_image_id},
        }
        # add steps config
        for step_index in range(1, self.lab_steps + 1):
            base_config["details"]["steps"].append(self.init_step(step_index))
        # write index.json
        base_file = open(f"{self.lab_slug}/index.json", "w")
        base_file.write(json.dumps(base_config, indent=4))
        # if a challenge, create solution file
        if self.lab_type == "challenge":
            solution_folder = f"{self.lab_slug}/solution"
            os.mkdir(solution_folder)
            solution_file = open(f"{solution_folder}/solution.md", "w")
            solution_file.write(f"# Solution")
        # if assets, create assets folder
        if self.if_assets == "yes":
            assets_folder = f"{self.lab_slug}/assets"
            os.mkdir(assets_folder)