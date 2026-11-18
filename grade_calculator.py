def validate_marks(marks):
    if not marks:
        raise ValueError("Marks list cannot be empty.")

    for mark in marks:
        if not isinstance(mark, (int, float)):
            raise ValueError("Marks must be numeric.")

        if mark < 0 or mark > 100:
            raise ValueError("Marks must be between 0 and 100.")

    return True


def calculate_total(marks):
    validate_marks(marks)
    return sum(marks)


def calculate_average(marks):
    validate_marks(marks)
    return calculate_total(marks) / len(marks)


def calculate_grade(average):
    if not isinstance(average, (int, float)) or not 0 <= average <= 100:
        raise ValueError("Average must be between 0 and 100.")

    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def main():
    try:
        count = int(input("Enter number of subjects: "))

        if count <= 0:
            raise ValueError("Number of subjects must be positive.")

        marks = []

        for i in range(count):
            mark = float(input(f"Enter marks for subject {i + 1}: "))
            marks.append(mark)

        total = calculate_total(marks)
        average = calculate_average(marks)
        grade = calculate_grade(average)

        print("\n----- STUDENT RESULT -----")
        print("Total:", total)
        print("Average:", round(average, 2))
        print("Grade:", grade)

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
  
