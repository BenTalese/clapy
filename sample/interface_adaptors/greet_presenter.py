from sample.use_cases.greet.igreet_output_port import IGreetOutputPort
from src.clapy.outputs import ValidationResult


class GreetPresenter(IGreetOutputPort):

    async def present_greeting_async(self, greeting: str) -> None:
        print(greeting)

    async def present_validation_failure_async(self, validation_failure: ValidationResult) -> None:
        print(validation_failure.summary)

    async def present_missing_names_warning_async(self) -> bool:
        user_input = input("You only told me one of your names, do you want to continue? Enter 'Y' to continue or 'N' to stop.")
        return user_input == 'Y'
