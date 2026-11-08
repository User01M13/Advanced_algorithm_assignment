
#University Course Prerequisite System

from collections import deque

# ---------------------------------------------------------------------------
# Generic graph data structure (no course-specific code)
# ---------------------------------------------------------------------------
class Graph:
    def __init__(self):
        # Each key is a vertex; its value is a list of outgoing neighbours.
        self.adjacency_list = {}

    def addVertex(self, vertex):
        #Add a vertex if it does not already exist.
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            return True
        return False

    def addEdge(self, source, destination):
        #Add the directed edge source -> destination.
        #Returns False if either vertex is missing or the edge already exists.
        if source not in self.adjacency_list or destination not in self.adjacency_list:
            return False
        if destination in self.adjacency_list[source]:
            return False  # Avoid duplicate edges.

        self.adjacency_list[source].append(destination)
        return True

    def removeEdge(self, source, destination):
        #Remove the directed edge source -> destination.#
        if self.hasEdge(source, destination):
            self.adjacency_list[source].remove(destination)
            return True
        return False

    def removeVertex(self, vertex):
        #Remove a vertex and all edges connected to it.#
        if vertex not in self.adjacency_list:
            return False

        # Remove this vertex from every other vertex's neighbour list.
        for neighbours in self.adjacency_list.values():
            if vertex in neighbours:
                neighbours.remove(vertex)

        del self.adjacency_list[vertex]
        return True

    def listAdjacentVertex(self, vertex):
        #Return outgoing neighbours of the vertex.
        return self.adjacency_list.get(vertex, []).copy()

    def listIncomingAdjacentVertex(self, vertex):
        #Return every vertex that has an edge pointing into the given vertex."""
        if vertex not in self.adjacency_list:
            return []
        return [source for source, neighbours in self.adjacency_list.items()
                if vertex in neighbours]

    def hasVertex(self, vertex):
        return vertex in self.adjacency_list

    def hasEdge(self, source, destination):
        return (source in self.adjacency_list
                and destination in self.adjacency_list[source])

    def hasPath(self, start, end):
        #Breadth-first search: can `end` be reached by following edges from `start`?"""
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return False

        visited = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current == end:
                return True
            for neighbour in self.adjacency_list[current]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return False

    def getVertices(self):
        #Return all vertices without their edges.
        return list(self.adjacency_list.keys())

    def getEdges(self):
        #Return all directed edges as (source, destination) tuples.
        return [(source, destination)
                for source, neighbours in self.adjacency_list.items()
                for destination in neighbours]

    def displayGraph(self, title="Graph (Adjacency List)"):
        #Display the graph as an adjacency list.
        print(f"\n{title}:")
        for vertex, neighbours in self.adjacency_list.items():
            targets = ", ".join(map(str, neighbours)) if neighbours else "None"
            print(f"{vertex} -> {targets}")

# ---------------------------------------------------------------------------
# Domain entity
# ---------------------------------------------------------------------------
class Course:
    #Stores the details of one university course.
    CORE = "Core"
    ELECTIVE = "Elective"
    TYPES = (CORE, ELECTIVE)

    def __init__(self, courseCode, courseName, creditHours, level, courseType):
        self.courseCode = courseCode
        self.courseName = courseName
        self.creditHours = creditHours
        self.level = level
        self.courseType = courseType

    def isCore(self):
        return self.courseType == Course.CORE

    def displayDetails(self):
        #Show every attribute, regardless of the course type.
        print("\nCourse Details")
        print("------------------------------")
        print(f"Course Code   : {self.courseCode}")
        print(f"Course Name   : {self.courseName}")
        print(f"Credit Hours  : {self.creditHours}")
        print(f"Level         : {self.level}")
        print(f"Course Type   : {self.courseType}")

    def displayProfile(self):
        #Visibility-aware profile: core shows everything, elective shows only the name."""
        if self.isCore():
            self.displayDetails()
        else:
            print("\nCourse Profile")
            print("------------------------------")
            print(f"Course Name   : {self.courseName}")
            print("(Other details are hidden for elective courses)")


# ---------------------------------------------------------------------------
# Application layer: connects Course objects to the Graph and provides the menu
# ---------------------------------------------------------------------------
class UniversityCourseSystem:
    MAX_COURSES = 10

    # Sample data kept as constants so it can be changed without touching the logic.
    SAMPLE_COURSES = [
        Course("PRG1015", "Programming Fundamentals", 3, "Year 1", Course.CORE),
        Course("MTH1003", "Discrete Mathematics", 3, "Year 1", Course.CORE),
        Course("PRG1024", "Object-Oriented Programming", 3, "Year 1", Course.CORE),
        Course("DSA2028", "Data Structures and Algorithms", 4, "Year 2", Course.CORE),
        Course("DBS2031", "Database Management", 3, "Year 2", Course.CORE),
        Course("SWE3203", "Software Engineering", 3, "Year 3", Course.CORE),
        Course("AIN3109", "Artificial Intelligence", 3, "Year 3", Course.ELECTIVE),
        Course("WEB3101", "Web Application Development", 3, "Year 3", Course.ELECTIVE),
    ]
    # (prerequisite, course it unlocks)
    SAMPLE_EDGES = [
        ("PRG1015", "PRG1024"),  # Programming Fundamentals -> Object-Oriented Programming
        ("PRG1024", "DSA2028"),  # Object-Oriented Programming -> Data Structures and Algorithms
        ("MTH1003", "DSA2028"),  # Discrete Mathematics -> Data Structures and Algorithms
        ("PRG1024", "DBS2031"),  # Object-Oriented Programming -> Database Management
        ("PRG1024", "WEB3101"),  # Object-Oriented Programming -> Web Application Development
        ("DBS2031", "WEB3101"),  # Database Management -> Web Application Development
        ("DSA2028", "AIN3109"),  # Data Structures and Algorithms -> Artificial Intelligence
        ("DSA2028", "SWE3203"),  # Data Structures and Algorithms -> Software Engineering
        ("DBS2031", "SWE3203"),  # Database Management -> Software Engineering
    ]

    def __init__(self):
        self.graph = Graph()
        self.courses = {}  # courseCode -> Course object
        self.running = True
        self.menu = self.buildMenu()
        self.createSampleCourses()

    # ---- Setup ----------------------------------------------------------
    def buildMenu(self):
        """Menu as data: adding a feature means adding one line here."""
        return [
            ("View All Courses", self.displayAllCourses),
            ("View Course Details", self.viewCourseDetails),
            ("View Prerequisites of a Course", self.viewPrerequisites),
            ("View Courses Unlocked by a Course", self.viewUnlockedCourses),
            ("Add a New Course", self.addCourseOnDemand),
            ("View Course Profile (elective details hidden)", self.viewCourseProfile),
            ("Add a Prerequisite", self.addPrerequisiteOnDemand),
            ("Remove a Prerequisite", self.removePrerequisiteOnDemand),
            ("Display Graph", self.displayGraph),
            ("Exit", self.exitProgram),
        ]

    def createSampleCourses(self):
        #Load the sample courses and their prerequisite edges.
        for course in self.SAMPLE_COURSES:
            self.courses[course.courseCode] = course
            self.graph.addVertex(course.courseCode)
        for source, destination in self.SAMPLE_EDGES:
            self.graph.addEdge(source, destination)

    def addCourse(self, course):
        #Add a course to both the course dictionary and the graph.
        code = course.courseCode

        if len(self.courses) >= self.MAX_COURSES:
            print(f"The course limit of {self.MAX_COURSES} has been reached.")
            return False
        if code in self.courses:
            print("A course with that code already exists.")
            return False

        self.courses[code] = course
        self.graph.addVertex(code)
        print(f"Course {code} added successfully.")
        return True

    # ---- Input helpers --------------------------------------------------
    @staticmethod
    def askCode(prompt):
        return input(prompt).strip().upper()

    def askExistingCourse(self, prompt):
        #Ask for a course code; return the Course, or None after printing why.
        code = self.askCode(prompt)
        course = self.courses.get(code)
        if course is None:
            print("Course not found.")
        return course

    # ---- Mandatory features --------------------------------------------
    def displayAllCourses(self):
        print("\nAvailable Courses:")
        for number, course in enumerate(self.courses.values(), start=1):
            print(f"{number}. {course.courseCode} - {course.courseName}")

    def viewCourseDetails(self):
        course = self.askExistingCourse("Enter Course Code: ")
        if course:
            course.displayDetails()  # The compulsory view shows all information.

    def viewPrerequisites(self):
        course = self.askExistingCourse("Enter Course Code: ")
        if course:
            self.printCourseList(
                f"Prerequisites for {course.courseCode} - {course.courseName}:",
                self.graph.listIncomingAdjacentVertex(course.courseCode),
                "No prerequisite courses")

    def viewUnlockedCourses(self):
        course = self.askExistingCourse("Enter Course Code: ")
        if course:
            self.printCourseList(
                f"Courses unlocked by {course.courseCode} - {course.courseName}:",
                self.graph.listAdjacentVertex(course.courseCode),
                "No courses are unlocked by this course")

    def printCourseList(self, title, codes, emptyMessage):
        print(f"\n{title}")
        if not codes:
            print(f"- {emptyMessage}")
        for code in codes:
            print(f"- {code} ({self.courses[code].courseName})")

    # ---- Advanced features ---------------------------------------------
    def addCourseOnDemand(self):
        """(a) Add a course on demand -> creates a new vertex."""
        if len(self.courses) >= self.MAX_COURSES:
            print(f"The course limit of {self.MAX_COURSES} has been reached.")
            return

        print("\nAdd a New Course")
        code = self.askCode("Course Code: ")
        if code in self.courses:
            print("A course with that code already exists.")
            return
        name = input("Course Name: ").strip()

        try:
            credits = int(input("Credit Hours: "))
        except ValueError:
            print("Please enter a valid whole number for credit hours.")
            return
        if credits <= 0:
            print("Credit hours must be greater than zero.")
            return

        level = input("Level (e.g. Year 1): ").strip()
        courseType = input(f"Course Type ({'/'.join(Course.TYPES)}): ").strip().title()

        if not code or not name or not level:
            print("Course code, name and level cannot be empty.")
            return
        if courseType not in Course.TYPES:
            print(f"Course type must be one of: {', '.join(Course.TYPES)}.")
            return

        self.addCourse(Course(code, name, credits, level, courseType))

    def viewCourseProfile(self):
        #(b) Core courses show all details; electives show only the name.
        course = self.askExistingCourse("Enter Course Code: ")
        if course:
            course.displayProfile()

    def addPrerequisiteOnDemand(self):
        #(c) Course X adds course Y as a prerequisite -> new edge Y -> X.
        x = self.askExistingCourse("Enter course X (the course that needs a prerequisite): ")
        if not x:
            return
        y = self.askExistingCourse("Enter course Y (to add as a prerequisite of X): ")
        if not y:
            return

        if x.courseCode == y.courseCode:
            print("A course cannot be its own prerequisite.")
        elif self.graph.hasEdge(y.courseCode, x.courseCode):
            print("The prerequisite relationship already exists.")
        elif self.graph.hasPath(x.courseCode, y.courseCode):
            # Y -> X would close a loop, since X already leads to Y.
            print(f"Cannot add: {y.courseCode} already depends on {x.courseCode}, "
                  f"so this would create a circular prerequisite.")
        else:
            self.graph.addEdge(y.courseCode, x.courseCode)
            print(f"{y.courseCode} is now a prerequisite of {x.courseCode}.")

    def removePrerequisiteOnDemand(self):
        #(d) Course X removes course Y as a prerequisite -> delete edge Y -> X.
        x = self.askExistingCourse("Enter course X (the course to remove a prerequisite from): ")
        if not x:
            return
        y = self.askExistingCourse("Enter course Y (the prerequisite to remove): ")
        if not y:
            return

        if self.graph.removeEdge(y.courseCode, x.courseCode):
            print(f"{y.courseCode} is no longer a prerequisite of {x.courseCode}.")
        else:
            print("That prerequisite relationship does not exist.")

    def displayGraph(self):
        self.graph.displayGraph("Course Prerequisite Graph (Adjacency List)")

    def exitProgram(self):
        print("Exiting program. Goodbye!")
        self.running = False

    # ---- Main loop ------------------------------------------------------
    def run(self):
        while self.running:
            print("\n****** University Course Prerequisite System ******")
            for number, (label, _) in enumerate(self.menu, start=1):
                print(f"{number}. {label}")

            try:
                choice = input("Enter choice: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                self.exitProgram()
                break

            if choice.isdigit() and 1 <= int(choice) <= len(self.menu):
                self.menu[int(choice) - 1][1]()
            else:
                print(f"Invalid choice. Please enter a number from 1 to {len(self.menu)}.")


if __name__ == "__main__":
    UniversityCourseSystem().run()