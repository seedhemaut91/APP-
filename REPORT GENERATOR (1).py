import functools
from datetime import datetime


# ==========================
# DECORATORS
# ==========================

def uppercase(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper


def add_border(char="-", length=50):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            border = char * length
            return f"{border}\n{text}\n{border}"
        return wrapper
    return decorator


def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} started")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} finished")
        return result
    return wrapper


# ==========================
# REPORT SECTION
# ==========================

class ReportSection:

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"{self.title}\n{self.content}"

    def __repr__(self):
        return f"ReportSection('{self.title}')"

    def __eq__(self, other):
        return (
            isinstance(other, ReportSection)
            and self.title == other.title
            and self.content == other.content
        )


# ==========================
# REPORT CLASS
# ==========================

class Report:

    templates = {}

    def __init__(self, title, author="Unknown"):
        self.title = title
        self.author = author
        self.sections = []
        self.created_on = datetime.now()

    # --------------------------
    # CLASS METHODS
    # --------------------------

    @classmethod
    def register_template(cls, name, section_titles):
        cls.templates[name] = section_titles
        print(f"Template '{name}' registered successfully.")

    @classmethod
    def from_template(cls, name, title, author="Unknown"):
        if name not in cls.templates:
            raise ValueError("Template not found!")

        report = cls(title, author)

        for heading in cls.templates[name]:
            report.add_section(heading, "<content pending>")

        return report

    @classmethod
    def available_templates(cls):
        return list(cls.templates.keys())

    # --------------------------
    # INSTANCE METHODS
    # --------------------------

    def add_section(self, title, content):
        self.sections.append(ReportSection(title, content))
        return self

    def set_content(self, title, content):
        for section in self.sections:
            if section.title == title:
                section.content = content
                return True
        return False

    @log_call
    @add_border("=", 50)
    def summary(self):
        return (
            f"Report : {self.title}\n"
            f"Author : {self.author}\n"
            f"Sections : {len(self.sections)}\n"
            f"Created : {self.created_on.strftime('%d-%m-%Y %H:%M')}"
        )

    @bold
    def title_line(self):
        return self.title

    # --------------------------
    # MAGIC METHODS
    # --------------------------

    def __str__(self):
        text = f"\nREPORT : {self.title}\n"
        text += f"Author : {self.author}\n"
        text += "-" * 40 + "\n"

        for section in self.sections:
            text += str(section) + "\n\n"

        return text

    def __repr__(self):
        return f"Report(title='{self.title}', author='{self.author}')"

    def __len__(self):
        return len(self.sections)

    def __getitem__(self, index):
        return self.sections[index]

    def __iter__(self):
        return iter(self.sections)

    def __contains__(self, title):
        return any(section.title == title for section in self.sections)

    def __add__(self, other):
        if not isinstance(other, Report):
            return NotImplemented

        merged = Report(
            self.title + " + " + other.title,
            self.author
        )

        merged.sections = self.sections + other.sections
        return merged

    def __eq__(self, other):
        return (
            isinstance(other, Report)
            and self.title == other.title
            and self.sections == other.sections
        )

    def __call__(self, formatter=None):
        output = str(self)

        if formatter:
            return formatter(output)

        return output


# ==========================
# MAIN PROGRAM
# ==========================

if __name__ == "__main__":

    # Register Templates
    Report.register_template(
        "project_report",
        [
            "Introduction",
            "Methodology",
            "Results",
            "Conclusion"
        ]
    )

    Report.register_template(
        "attendance_report",
        [
            "Summary",
            "Defaulter List"
        ]
    )

    print("\nAvailable Templates:")
    print(Report.available_templates())

    # Create Report from Template
    r1 = Report.from_template(
        "project_report",
        "AI Lab Mini Project",
        "Rahul"
    )

    r1.set_content(
        "Introduction",
        "This project explores dynamic report generation."
    )

    r1.set_content(
        "Methodology",
        "Decorators, Class Methods and Magic Methods are used."
    )

    r1.set_content(
        "Results",
        "Report generated successfully."
    )

    r1.set_content(
        "Conclusion",
        "Python OOP concepts were implemented successfully."
    )

    # Create Second Report
    r2 = Report(
        "Attendance Report",
        "Rahul"
    )

    r2.add_section(
        "Summary",
        "92% attendance this month."
    )

    r2.add_section(
        "Defaulter List",
        "No defaulters found."
    )

    # Demonstration
    print(r1.summary())

    print("\nTitle Line:")
    print(r1.title_line())

    print("\nReport:")
    print(r1)

    print("Number of Sections:", len(r1))

    print("\nFirst Section:")
    print(r1[0])

    print("\nContains 'Results'?", "Results" in r1)

    merged = r1 + r2

    print("\nMerged Report:")
    print(merged)

    print("\nCalling Report Object:")
    print(r1())

    print("\nCalling Report with Formatter:")
    print(r1(lambda text: text.upper()))
