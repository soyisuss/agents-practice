from langchain_core.tools import tool


@tool(
    "book_appointment",
    description="book a medical appointment for a given date, time, doctor and patient",
)
def book_appointment(date: str, time: str, doctor: str, patient: str):
    ## TODO: Implement the booking logic

    return f"Appointment booked for {date} at {time} with {doctor} for {patient}"


@tool(
    "get_availability",
    description="get the availability for a doctor, you can filtered by date and time",
)
def get_availability(doctor: str, date: str, time: str):
    ## TODO: Implement the availability logic
    return f"""
    The availability slots for the {doctor} are:
    - Monday: 10:00-15:00
    - Wednesday: 10:00-15:00
    - Thursday: 10:00-15:00
    - Friday: 10:00-12:00
    """


tools = [book_appointment]
