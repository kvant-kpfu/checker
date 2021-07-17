#!/usr/bin/env python3

from db_api.test_case import TestCase
from checker_ui import Ui_MainWindow
from task_info import Ui_Dialog as Ui_TaskInfoDialog
from add_task import Ui_Dialog as Ui_AddTaskDialog
from add_solution import Ui_Dialog as Ui_AddSolutionDialog
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QApplication,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
)
import db_api as api
from db_api.task import Task
from db_api.solution import Solution
import checker
import sys
import os

api.global_init(api.sqlite_format_string("db/checker_db.sqlite3"))


class TaskInfoDialog(QDialog, Ui_TaskInfoDialog):
    """Dialog to show selected task info.

    Its contents should be initialized after the object.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class AddTaskDialog(QDialog, Ui_AddTaskDialog):
    """Dialog to get new task information from a user.

    Its contents should be initialized after the object.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class AddSolutionDialog(QDialog, Ui_AddSolutionDialog):
    """Dialog to get new solution information from a user.

    Its contents should be initialized after the object.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class App(QMainWindow, Ui_MainWindow):
    """Main window of a GUI application."""

    def __init__(self):
        super().__init__()

        # Initializing
        self.setupUi(self)
        self.initialize()

        # Default parameters
        self.autoDetectLang = True

        # If the solution was selected, show its contents.
        self.listSolutions.itemClicked.connect(self.showSolution)

        # If the solution was double-clicked, remove it.
        self.listSolutions.itemDoubleClicked.connect(self.removeSolution)

        # If the task was selected, show corresponding solutions.
        self.taskSelect.currentIndexChanged.connect(
            lambda _: self.fillSolutions()
        )

        # Buttons and menu actions.
        self.taskInfo.clicked.connect(self.showTaskInfo)
        self.actionAdd_Task.triggered.connect(self.addTask)
        self.actionAdd_Solution.triggered.connect(self.addSolution)
        self.runTests.clicked.connect(self.checkSolution)
        self.actionDetect_language.triggered.connect(
            lambda: self.setParameters(detect_language=not self.autoDetectLang)
        )

    def setParameters(self, **kwargs):
        """Sets the parameters in the format param_name=value.

        Currently supported parameters:
            detect_language (bool): to determine whether to detect language
            automatically based on file extension or not.
        """
        for key, value in kwargs.items():
            if key == "detect_language":
                if value:
                    self.actionDetect_language.setText("Detect language: On")
                else:
                    self.actionDetect_language.setText("Detect language: Off")
                self.autoDetectLang = value

    def initialize(self):
        """Initializing main widgets."""

        self.codeBrowser.setMarkdown("``````")  # Empty code block.
        self.solutionTitle.setText("Select a solution.")
        self.fillTasks()
        self.fillSolutions()

    def fillTasks(self):
        """Function to update "tasks" combobox."""
        self.taskSelect.clear()
        with api.create_session() as session:
            self.taskSelect.addItems(
                [item.name for item in api.get_all(session, Task)]
            )

    def fillSolutions(self):
        """Function to update "solutions" list.

        Only solutions for the selected task will be displayed.
        """
        self.listSolutions.clear()
        if self.taskSelect.count() > 0:
            with api.create_session() as session:
                for i in session.query(Solution).filter_by(
                    task_id=session.query(Task)
                    .filter_by(name=self.taskSelect.currentText())
                    .first()
                    .id
                ):
                    item = QListWidgetItem(i.filename)
                    item.setToolTip(i.sender)
                    self.listSolutions.addItem(item)

    def addTests(self):
        """Function to let users select tests and add them to the database.

        Supports multiple selection.
        """
        fdialog = QFileDialog()
        fdialog.setFileMode(QFileDialog.ExistingFiles)
        if (
            QMessageBox(
                QMessageBox.Information,
                "Select input files",
                "Please select only input files.",
                QMessageBox.Cancel | QMessageBox.Ok,
            ).exec()
            == QMessageBox.Ok
        ):
            fin = fdialog.getOpenFileNames(self, "Upload input files")[0]
            # TODO: Automatically generate outputs
            # if QMessageBox(
            #     QMessageBox.Question,
            #     'Question',
            #     'Do you want to automatically generate outputs?\n'
            #     'Select "No" to choose outputs manually.',
            #     QMessageBox.Yes | QMessageBox.No,
            # ).exec() == QMessageBox.Yes:
            #     pass
            if (fin) and (
                QMessageBox(
                    QMessageBox.Information,
                    "Select output files",
                    "Now, please select the same number of output files.\n"
                    "Input and output files will be bonded in alphabetical "
                    "order.",
                    QMessageBox.Cancel | QMessageBox.Ok,
                ).exec()
                == QMessageBox.Ok
            ):
                fout = fdialog.getOpenFileNames(self, "Upload output files")[0]
                if not fout:
                    return None
                if len(fout) > len(fin):
                    QMessageBox(
                        QMessageBox.Critical,
                        "Error",
                        "Too much output files",
                        QMessageBox.Ok,
                    ).exec()
                    return None
                if len(fout) < len(fin):
                    QMessageBox(
                        QMessageBox.Critical,
                        "Error",
                        "Not enough output files",
                        QMessageBox.Ok,
                    ).exec()
                    return None
                fin.sort()
                fout.sort()
                with api.create_session() as session:
                    for i in range(len(fin)):
                        if fin[i] != "" and fout[i] != "":
                            api.create_test_case_by_task_name(
                                session,
                                fin[i],
                                fout[i],
                                self.taskSelect.currentText(),
                            )
                        session.commit()

    def addTask(self):
        """Function to let users create a task, and add it to the database."""
        dialog = AddTaskDialog()
        if dialog.exec() and dialog.taskName.text() != "":
            if dialog.taskName.text() in [
                self.taskSelect.itemText(i)
                for i in range(self.taskSelect.count())
            ]:
                QMessageBox(
                    QMessageBox.Critical,
                    "This task already exists.",
                    "This task already exists. "
                    "The name must be unique for each task.",
                    QMessageBox.Ok,
                ).exec()
                return None
            with api.create_session() as session:
                api.create_task(
                    session,
                    dialog.taskName.text(),
                    dialog.taskDescription.toPlainText(),
                )
                session.commit()
            self.fillTasks()

    def addSolution(self):
        """Function to let user select a solution and add it to the database.

        Updates list of solutions afterwards."""
        fdialog = QFileDialog()
        fdialog.setFileMode(QFileDialog.ExistingFile)
        file = fdialog.getOpenFileName(self, "Upload solution")[0].strip()
        if file:
            dialog2 = AddSolutionDialog()
            dialog2.taskSelect.addItems(
                [
                    self.taskSelect.itemText(i)
                    for i in range(self.taskSelect.count())
                ]
            )
            dialog2.taskSelect.setCurrentText(self.taskSelect.currentText())
            if dialog2.exec() and dialog2.senderName.text():
                with api.create_session() as session:
                    task_id = (
                        session.query(Task)
                        .filter_by(name=dialog2.taskSelect.currentText())
                        .first()
                        .id
                    )
                    if (
                        session.query(Solution)
                        .filter_by(
                            filename=file,
                            task_id=task_id,
                        )
                        .first()
                    ):
                        QMessageBox(
                            QMessageBox.Critical,
                            "This solution already exists",
                            "This solution already exists under this task.",
                            QMessageBox.Ok,
                        ).exec()
                        return None
                    api.create_solution(
                        session,
                        file,
                        dialog2.senderName.text(),
                        task_id,
                    )
                    session.commit()
                self.taskSelect.setCurrentText(
                    dialog2.taskSelect.currentText()
                )
                self.fillSolutions()

    def showSolution(self, item):
        """Function to show the selected solution.

        Displays the code of the solution, its author (sender) and its
        filename."""

        def code_to_html(text: str) -> str:
            """Returns html code block with text inside."""
            return (
                "<div><pre><code>"
                + text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                + "</code></pre></div>"
            )

        if os.path.exists(item.text()):
            with open(item.text(), "r") as file:
                self.codeBrowser.setHtml(code_to_html(file.read()))
            self.solutionTitle.setText(
                item.toolTip() + " - " + os.path.split(item.text())[-1]
            )
            if self.autoDetectLang:
                if os.path.splitext(item.text())[-1] == ".py":
                    self.langSelect.setCurrentText("python")
                elif os.path.splitext(item.text())[-1] == ".go":
                    self.langSelect.setCurrentText("golang")
                elif os.path.splitext(item.text())[-1] in (
                    ".C",
                    ".cc",
                    ".cpp",
                    ".CPP",
                    ".c++",
                    ".cp",
                    ".cxx",
                ):
                    self.langSelect.setCurrentText("cpp")
        else:
            QMessageBox(
                QMessageBox.Critical,
                "File not found error",
                "File " + item.text() + " does not exist.",
            ).exec()

    def removeSolution(self, item):
        """Function to remove the selected solution."""
        if (
            QMessageBox(
                QMessageBox.Warning,
                "Remove a solution",
                "Are you sure you want to remove this solution?",
                QMessageBox.Yes | QMessageBox.Cancel,
            ).exec()
            == QMessageBox.Yes
        ):
            with api.create_session() as session:
                api.remove_solution(
                    session,
                    session.query(Solution)
                    .filter_by(
                        sender=item.toolTip(),
                        filename=item.text(),
                        task_id=session.query(Task)
                        .filter_by(name=self.taskSelect.currentText())
                        .first()
                        .id,
                    )
                    .first()
                    .id,
                )
                session.commit()
            self.fillSolutions()

    def showTaskInfo(self):
        """Function to show the selected task information.

        Shows task description and its test cases in a separate dialog."""
        dialog = TaskInfoDialog()

        def updateDialog(dialog):
            """Updates widgets of task information dialog."""
            with api.create_session() as session:
                task = (
                    session.query(Task)
                    .filter_by(name=self.taskSelect.currentText())
                    .first()
                )
                dialog.description.setMarkdown(task.description)
                dialog.listTests.clear()
                i = 1
                for item in (
                    session.query(TestCase).filter_by(task_id=task.id).all()
                ):
                    dialog.listTests.addItem(
                        f"""Test #{i}
Input: {item.input_filename}
Output: {item.output_filename}"""
                    )
                    i += 1

        def clickedAddTests():
            """Runs addTests function and updates
            the task information dialog."""
            self.addTests()
            updateDialog(dialog)

        def removeItem(item):
            """Removes the selected test case."""
            if (
                QMessageBox(
                    QMessageBox.Warning,
                    "Remove an item",
                    "Are you sure you want to remove this item?",
                    QMessageBox.Yes | QMessageBox.Cancel,
                ).exec()
                == QMessageBox.Yes
            ):
                temp = item.text().splitlines()
                with api.create_session() as session:
                    api.remove_test_case(
                        session,
                        session.query(TestCase)
                        .filter_by(
                            input_filename=temp[1][6:].strip(),
                            output_filename=temp[2][7:].strip(),
                        )
                        .first()
                        .id,
                    )
                    session.commit()
                updateDialog(dialog)

        def removeSelf():
            """Removes the task, the information of which is being displayed.

            Closes the window afterwards."""
            if (
                QMessageBox(
                    QMessageBox.Warning,
                    "Remove task",
                    "Are you sure you want to remove this task?",
                    QMessageBox.Yes | QMessageBox.Cancel,
                ).exec()
                == QMessageBox.Yes
            ):
                with api.create_session() as session:
                    api.remove_task(
                        session,
                        (
                            session.query(Task)
                            .filter_by(name=self.taskSelect.currentText())
                            .first()
                            .id
                        ),
                    )
                    session.commit()
                self.fillTasks()
                dialog.close()

        updateDialog(dialog)

        dialog.addTests.clicked.connect(clickedAddTests)
        dialog.listTests.itemDoubleClicked.connect(removeItem)
        dialog.removeTask.clicked.connect(removeSelf)
        dialog.exec()

    def checkSolution(self):
        """Runs tests on the selected solution, and displays the results."""
        if len(self.listSolutions.selectedItems()) == 0:
            QMessageBox(
                QMessageBox.Critical,
                "The solution is not selected.",
                "The solution is not selected. "
                "You need to select the solution first.",
                QMessageBox.Ok,
            ).exec()
            return None
        langChecker = {
            "python": checker.PythonChecker,
            "cpp": checker.CppChecker,
            "golang": checker.GolangChecker,
        }[self.langSelect.currentText()]
        with api.create_session() as session:
            task_id = (
                session.query(Task)
                .filter_by(name=self.taskSelect.currentText())
                .first()
                .id
            )
            selectedSolution = (
                session.query(Solution)
                .filter_by(
                    sender=self.listSolutions.currentItem().toolTip(),
                    filename=self.listSolutions.currentItem().text(),
                    task_id=task_id,
                )
                .first()
            )
            inputs = []
            outputs = []
            for item in (
                session.query(TestCase).filter_by(task_id=task_id).all()
            ):
                inputs.append(item.input_filename)
                outputs.append(item.output_filename)

        self.solutionOutput.setText(
            "Running "
            + os.path.split(self.listSolutions.currentItem().text())[-1]
            + " by "
            + self.listSolutions.currentItem().toolTip()
            + "...\n"
        )
        self.repaint()

        res = langChecker(
            checker.Test.load_multiple(inputs, outputs)
        ).check_solution(selectedSolution.filename)

        self.solutionOutput.setPlainText(
            self.solutionOutput.toPlainText()
            + f"{res.count(checker.TestResult.OK)}/{len(res)} tests solved."
        )
        for i, val in enumerate(res):
            self.solutionOutput.setPlainText(
                self.solutionOutput.toPlainText()
                + "\n"
                + f"Test {i + 1}: {val.name}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
