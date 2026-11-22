class InvalidSalaryRangeError(Exception):
    def __init__(self, salary_type: str) -> None:
        self.salary_type = salary_type

        super().__init__(
            f'{salary_type.capitalize()} maximum salary must be greater than '
            f'or equal to the {salary_type} minimum salary'
        )


class ApplicationNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('Job application not found')


class ResumeNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('Resume not found')
