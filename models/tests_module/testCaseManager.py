from models.stories_module.userStory import UserStory

# Class for generating the python test case from a UserStory and stores it into a file.

class TestCaseManager:
    def __init__(self):
        self.test_cases_folder = "tests"

    def create_test_case_code(self, user_story: UserStory):
        code = [
            "from playwright.sync_api import sync_playwright",
            "",
            "def test_user_story():",
            "    with sync_playwright() as p:",
            "        browser = p.chromium.launch(headless=False)",
            "        page = browser.new_page()",
            f"        page.goto('{user_story.get_first_action().current_url}')"
        ]
        
        for step in user_story.actions:
            if step.eventType == "click":
                code.append(f"        page.click('{step.eventClass}')")
            elif step.eventType == "input":
                code.append(
                    f"        page.fill('{step.eventClass}', '{step.elementText}')"
                )
            elif step.eventType == "navigation":
                code.append(f"        page.goto('{step.current_url}')")

        code.extend([
            "        browser.close()",
            ""
        ])
        return "\n".join(code)
            
    def save_test_case(self, user_story: UserStory, test_case_code):
        filename = f"{self.test_cases_folder}/test_case_{user_story.id}.py"
        with open(filename, "w") as file:
            file.write(test_case_code)