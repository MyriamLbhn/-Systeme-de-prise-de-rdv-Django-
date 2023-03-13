from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from bookingapp.models import Appointment, NoteForm
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail


def booking(request):
    """Displays the available weekdays for booking within the next 21 days and handles booking requests.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object that contains the booking HTML template.
    """

    # Get a list of all the weekdays within the next 22 days
    weekdays = valid_weekday(22)

    # Filter out the weekdays that are already fully booked
    validateWeekdays = is_weekday_valid(weekdays)

    if request.method == 'POST':
        # Get the selected day from the form and store it in the Django session
        day = request.POST.get('day')
        request.session['day'] = day
        return redirect('booking_submit')
    
    # Get weekdays that are not full and are weekdays, sort them by date and time
    weekdays_available = sorted(set(weekdays).intersection(validateWeekdays),
                                key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

    return render(request, 'booking.html', {
            'weekdays': weekdays,
            'weekdays_available': weekdays_available,
        })

def booking_submit(request):
    """Handles booking submission and displays the available booking times for a selected day. 
    Gives the possibility to add input a motive for the appointment.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object that contains the booking_submit HTML template.
    """

    # Get the current user and the available booking times
    user = request.user
    times = [
        "9 AM", "10 AM", "11 AM", "12 AM", "1:30 PM", "2:30 PM", "3:30 PM"
    ]

    # Get the minimum and maximum dates for booking
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    # Get the selected day from the Django session
    day = request.session.get('day')

    # Only show the time of the day that has not been selected before
    hour = check_time(times, day)
    if request.method == 'POST':
        # Get the selected time and motif from the form
        time = request.POST.get("time")
        date = day_to_weekday(day)
        motif = request.POST.get("motif")

        # Check if the selected day is within the booking range and is a valid weekday
        if day <= maxDate and day >= minDate:
            if date == 'Tuesday' or date == 'Wednesday' or date == 'Thursday' or date == 'Friday' or date == 'Monday':
                # Check if there are still available slots for the selected day
                if Appointment.objects.filter(day=day).count() < 8:
                    # Check if the selected time is still available for the selected day
                    if Appointment.objects.filter(day=day, time=time).count() < 1:
                        AppointmentForm = Appointment.objects.get_or_create(
                            user = user,
                            day = day,
                            time = time,
                            motif = motif
                        )
                        return redirect('user_appointment')

    return render(request, 'booking_submit.html', {
        'times':hour,
    })

def user_appointment(request):
    """Displays the user's future appointments.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object that contains the user_appointment HTML template.
    """
    # Get the current user
    user = request.user

    # Retrieve upcoming appointments that belong to the current user
    appointments = Appointment.objects.filter(user=user, day__gt=datetime.now().date()).order_by('day', 'time')

    # Get the current date
    now = datetime.today().date()

    return render(request, 'user_appointment.html', {
        'user': user,
        'appointments': appointments,
        'now': now,
    })
    
def user_infos(request):
    """Displays the user's information.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object that contains the user_infos HTML template.
    """
    user = request.user
    return render(request, 'user_infos.html', {
        'user':user
    })

def client_history(request):
    """Displays the user's past appointments.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object that contains the client_history HTML template.
    """
    user = request.user
    
    # Retrieve past appointments that belong to the current user
    old_appointments = Appointment.objects.filter(user=user, day__lt=datetime.now().date()).order_by('day', 'time')
    
    now = datetime.today().date()
    return render(request, 'client_history.html', {
        'user':user,
        'old_appointments':old_appointments,
        'now': now,
    })

def user_update_appointment(request, id:int):
    """Displays the form to update a specific appointment.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        id (int): The ID of the appointment to be updated.

    Returns:
        HttpResponse: The HTTP response object that contains the user_update_appointment HTML template.
    """
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = valid_weekday(22)

    #Only show the days that are not full:
    validateWeekdays = is_weekday_valid(weekdays)
    

    if request.method == 'POST':
        day = request.POST.get('day')

        #Store day in django session:
        request.session['day'] = day

        return redirect('user_update_submit_appointment', id=id)


    return render(request, 'user_update_appointment.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def user_update_submit_appointment(request, id:int):
    """Update a user's appointment with the specified ID.

    Args:
        request (HttpRequest): The HTTP request object for this view.
        id (int): The ID of the appointment to update.

    Returns:
        HttpResponse: A response indicating the result of the operation.
    """
    user = request.user
    times = [ 
        "9 AM", "10 AM", "11 AM", "12 AM", "1:30 PM", "2:30 PM", "3:30 PM"
        ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = check_edit_time(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = day_to_weekday(day)
        motif = request.POST.get("motif")


        if day <= maxDate and day >= minDate:
            if date == 'Tuesday' or date == 'Wednesday' or date == 'Thursday' or date == 'Friday' or date == 'Monday':
                if Appointment.objects.filter(day=day).count() < 11:
                    if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                        AppointmentForm = Appointment.objects.filter(pk=id).update(
                            user = user,
                            day = day,
                            time = time,
                            motif = motif

                            ) 
                        return redirect('user_appointment')

    return render(request, 'user_update_submit_appointment.html', {
        'times':hour,
        'id': id,
    })
    
def staff_appointment(request):
    """View for displaying a list of upcoming appointments and allowing staff to update appointment notes and reasons for cancellations.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object that contains the staff_appointment HTML template.
    """
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        motif = request.POST.get("motif")
        notes = request.POST.get("notes")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.notes = notes
        appointment.motif = motif
        appointment.save()
    items = Appointment.objects.filter(day__gte=datetime.now().date()).order_by('day', 'time')
    return render(request, 'staff_appointment.html', {'items':items})

def staff_history(request):
    """Displays a list of past appointments for staff users.

    Args:
        request (HttpRequest): An HTTP request object that contains metadata about the request.

    Returns:
        HttpResponse: An HTTP response containing a list of past appointments.
    """
    old_items = Appointment.objects.filter(day__lt=datetime.now().date()).order_by('day', 'time')
    return render(request, 'staff_history.html', {'old_items':old_items})

def day_to_weekday(x):
    """Converts a date in the format YYYY-MM-DD to the corresponding weekday.

    Args:
        x (str): A string representing a date in the format "YYYY-MM-DD".

    Returns:
        str: The corresponding weekday in full name (e.g., "Monday", "Tuesday", etc.).
    """
    # the strptime method parse the input string x into a datetime object,
    # "%Y-%m-%d" specifies the format of the input string
    z = datetime.strptime(x, "%Y-%m-%d")
    # convert the datetime object z into a string that represents the weekday, 
    # '%A' specifies that the full weekday name should be used (e.g., Monday, Tuesday, etc.).
    y = z.strftime('%A')
    return y

def valid_weekday(days:int)-> list:
    """Return a list of weekdays for the next `days` days, excluding Saturdays and Sundays.

    Args:
        days (int): Number of days to generate the list of weekdays for.

    Returns:
        list[str]: A list of strings representing the dates for each weekday in the format '%Y-%m-%d'.

    """
    #Loop days you want in the next 21 days:
    today = datetime.now()+ timedelta(days=1)
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y != 'Saturday' and y != 'Sunday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def is_weekday_valid(x:list)-> list:
    """Filters out invalid weekdays from the given list of weekdays.

    Args:
        x (list): A list of weekdays in string format ('YYYY-MM-DD').

    Returns:
        list: A filtered list of weekdays that have less than 7 appointments already scheduled.
    """
    validate_weekdays = []
    for j in x:
        num_appointments = Appointment.objects.filter(day=j).count()
        if num_appointments < 7:
            validate_weekdays.append(j)
    return validate_weekdays

def check_time(times:list, day:str)-> list:
    """Returns a list of times that have not been already selected for the given day.

    Args:
        times (list): List of all available times.
        day (str): The day to check for available times.

    Returns:
        list: List of times that have not been selected for the given day.
    """
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def check_edit_time(times:list, day:str, id:int)-> list:
    """Returns a list of available times for a given day, excluding the currently selected time in the appointment with the specified ID.

    Args:
        times (list): A list of time slots to check for availability.
        day (str): A string representing the day for which availability is being checked in the format 'YYYY-MM-DD'.
        id (int): The ID of the appointment whose selected time should be excluded from the list of available times.

    Returns:
        list: A list of available time slots for the given day.
    """
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x

def cancel_appointment(request, appointment_id:int):
    """Delete the appointment with the given ID from the database and send an email to the user to inform them of the cancellation.

    Args:
        request: the HTTP request object.
        appointment_id: the ID of the appointment to be cancelled.

    Returns:
        HttpResponse: The HTTP response object that contains the staff_appointment HTML template.
.
    """
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    # # Envoyer un email au patient ou pour les informer de l'annulation ou confirmer 
    subject = 'Annulation de rendez-vous'
    message = f"Votre rendez-vous du {appointment.day} à {appointment.time} a été annulé."
    from_email = 'noreply@votresite.com'
    to_list = [appointment.user.email]

    send_mail(subject, message, from_email, to_list, fail_silently=True)
    
    return redirect('staff_appointment')

#Same fonction than cancel_appointment but redirecting to user_appointment.html :
def cancel_user_appointment(request, appointment_id:int):
    """Delete the appointment with the given ID from the database.

    Args:
        request: the HTTP request object.
        appointment_id: the ID of the appointment to be cancelled.

    Returns:
        HttpResponse: The HTTP response object that contains the user_appointment HTML template.
.
    """
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()    
    return redirect('user_appointment')

def appointment_notes(request, appointment_id:int):
    """Display and process a form for adding or editing notes for a specific appointment.

    Args:
        request (HttpRequest): The current request object.
        appointment_id (int): The ID of the appointment to add/edit notes for.

    Returns:
        HttpResponse: A rendered HTML response containing a form for adding/editing notes for the appointment, 
        or a redirect to the appointment detail page upon successful form submission.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    print(appointment)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            appointment.notes = form.cleaned_data['notes']
            appointment.save()
            return redirect('appointment_detail', appointment_id=appointment_id)
    else:
        form = NoteForm(initial={'notes': appointment.notes})
    return render(request, 'appointment_notes.html', {'appointment': appointment, 'form': form})

def appointment_detail(request, appointment_id:int):
    """Renders the details of a specific appointment.

    Args:
        request (HttpRequest): A HttpRequest object that contains metadata about the current request.
        appointment_id (int): An integer that represents the unique identifier of the appointment to be displayed.

    Returns:
        HttpResponse: A HttpResponse object that renders the appointment detail template with the context containing the appointment object.
    """
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

def delete_note(request, appointment_id:int):
    """Deletes the notes for an appointment and redirects to the staff appointment page.

    Args:
        request (HttpRequest): The HTTP request object.
        appointment_id (int): The ID of the appointment.

    Returns:
        HttpResponseRedirect: A redirect to the staff appointment page.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.notes = ''
    appointment.save()
    return redirect('staff_appointment')


