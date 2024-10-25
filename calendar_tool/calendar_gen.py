# calendar_tool/calendar_gen.py

import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime, timedelta

def generate_workout_calendar(month, year=2024):
    """Generate a workout calendar for the given month and year, and save it as an .ics file."""
    # Get the start and end date for the given month
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, month, 31)

    # Generate the date range and create the DataFrame
    date_range = pd.date_range(start_date, end_date)
    workout_df = pd.DataFrame(date_range, columns=["Date"])

    # Define workout plan details
    strength_sets = {
        "Set 1": ["Pull-ups", "Push-ups", "Plank", "Dumbbell Rows", "Lunges"],
        "Set 2": ["Dips", "Chin-ups", "Planchettes Push-ups", "Goblet Squats", "Hanging Leg Raises"],
        "Set 3": ["Pull-ups", "Archer Push-ups", "Side Plank", "Overhead Press", "Bodyweight Squats"],
        "Set 4": ["Chin-ups", "Diamond Push-ups", "L-sit Hold", "Dumbbell Deadlift", "Calf Raises"]
    }

    # Assign activities based on a simplified rotation
    workout_df["Workout"] = workout_df["Date"].apply(lambda x: "Run" if x.day % 2 == 0 else "Strength")

    # Function to get strength set details based on date
    def get_strength_set(date):
        return strength_sets[f"Set {((date.day % len(strength_sets)) + 1)}"]

    # Define detailed running schedule
    def get_run_details(day_of_month):
        if day_of_month % 7 in [0, 4]:
            return "10+ mile long run"
        elif day_of_month % 2 == 0:
            return "5-7 mile distance run"
        else:
            return "4-mile tempo run"

    # Add workout details to the dataframe
    workout_df["Details"] = workout_df.apply(lambda row:
                                             get_run_details(row["Date"].day) if row["Workout"] == "Run"
                                             else get_strength_set(row["Date"]) if row["Workout"] == "Strength"
                                             else "Rest Day",
                                             axis=1)

    # Step 2: Create the .ics calendar file
    cal = Calendar()
    cal.add('prodid', f'-//Workout Calendar//{year} Month {month}//EN')
    cal.add('version', '2.0')

    # Function to create events for the calendar
    def create_event(row):
        event = Event()
        event.add('summary', f'{row["Workout"]}: {row["Details"]}' if row["Workout"] else "Rest Day")
        event.add('dtstart', row['Date'].date())
        event.add('dtend', (row['Date'] + timedelta(days=1)).date())
        event.add('description', f'Date: {row["Date"]}\nWorkout: {row["Workout"]}\nDetails: {row["Details"]}')
        return event

    # Add events to calendar
    for _, row in workout_df.iterrows():
        cal.add_component(create_event(row))

    # Save calendar to a file
    file_name = f'{year}_{month:02d}_Workout_Calendar.ics'
    with open(file_name, 'wb') as f:
        f.write(cal.to_ical())

    print(f"Calendar for {year}-{month:02d} saved as {file_name}")


def main():
    try:
        month = int(input("Enter the month number (1-12): ").strip())
        if 1 <= month <= 12:
            generate_workout_calendar(month)
        else:
            print("Please enter a valid month number between 1 and 12.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 12.")

if __name__ == "__main__":
    main()
