from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import ProtectedError
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from hr.models import Employee, Department, Designation, Leave, CalendarEvent


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if Employee.objects.filter(user=user).exists():
                return redirect("employee_dashboard")
            return redirect("dashboard")
        return render(request,"login.html",{"error": "Invalid username or password"})
    return render(request, "login.html")


@login_required
@never_cache
def dashboard(request):
    return render(request, "dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@never_cache
def employee_list(request):
    employees = Employee.objects.select_related('designation','department').filter(status=True)
    return render(request, "employee_list.html",{"employees":employees})

@login_required
@never_cache
def employee_create(request):

    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        department_id = request.POST.get("department")
        designation_id = request.POST.get("designation")

        joining_date = request.POST.get("joining_date")
        employment_type = request.POST.get("employment_type")
        salary = request.POST.get("salary")
        address = request.POST.get("address")

        status = request.POST.get("status") == "on"
        if Employee.objects.filter(email=email).exists():
            messages.error(
                request,
                "Employee with this email already exists."
            )
            return redirect("employee_create")

        # Create Django User
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=name
        )

        # Disable password until employee creates one
        user.set_unusable_password()
        user.save()

        # Create Employee
        employee = Employee.objects.create(
            user=user,
            employee_id=employee_id,
            name=name,
            email=email,
            phone=phone,
            department_id=department_id,
            designation_id=designation_id,
            joining_date=joining_date,
            employment_type=employment_type,
            salary=salary,
            address=address,
            status=status
        )

        # Generate password setup token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Password setup URL
        setup_link = request.build_absolute_uri(
            reverse(
                "set_password",
                kwargs={
                    "uidb64": uid,
                    "token": token
                }
            )
        )

        # Send email
        send_mail(
            subject="CrewConnect - Set Your Password",
            message=f"""
Hello {name},

Your CrewConnect employee account has been created.

Please click the link below to create your password:

{setup_link}

After setting your password, you can log in to CrewConnect.

Regards,
CrewConnect HR
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return redirect("employee_list")

    return render(
        request,
        "employee_add_update.html",
        {
            "departments": departments,
            "designations": designations,
            "employment_types": Employee.EMPLOYMENT_TYPES,
            "is_update": False,
        }
    )

@login_required
@never_cache
def employee_update(request,id):
    employee = get_object_or_404(
        Employee,
        id=id
    )
    departments = Department.objects.all()
    designations = Designation.objects.all()
    if request.method == "POST":
        employee.employee_id = request.POST.get("employee_id")
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")
        employee.department_id = request.POST.get("department")
        employee.designation_id = request.POST.get("designation")
        employee.joining_date = request.POST.get("joining_date")
        employee.employment_type = request.POST.get("employment_type")
        employee.salary = request.POST.get("salary")
        employee.address = request.POST.get("address")
        employee.status = request.POST.get("status") == "on"
        employee.save()
        return redirect(
            "employee_list"
        )
    return render(
        request,
        "employee_add_update.html",
        {
            "employee": employee,
            "departments": departments,
            "designations": designations,
            "employment_types": Employee.EMPLOYMENT_TYPES,
            "is_update": True,
        }
    )

@login_required
@never_cache
def employee_delete(request, id):
    employee = get_object_or_404(
        Employee,
        id=id
    )
    employee.status = not employee.status
    employee.save()
    return redirect("employee_list")

@login_required
@never_cache
def leave_approve(request):
   # Check whether logged-in user is an employee
   if Employee.objects.filter(user=request.user).exists():
       return redirect("employee_dashboard")
   leaves = Leave.objects.select_related(
       "employee",
       "employee__department",
       "employee__designation"
   ).order_by("-applied_date")
   return render(
       request,
       "leave_approval.html",
       {
           "leaves": leaves,
           "is_employee": False,
       }
   )


@login_required
@never_cache
def leave_action(request, id):
    # Employee cannot approve/reject
    if Employee.objects.filter(user=request.user).exists():
        return redirect("employee_dashboard")
    if request.method == "POST":
        leave = Leave.objects.get(id=id)
        action = request.POST.get("action")
        if action == "approve":
            leave.status = "Approved"
            leave.save()
        elif action == "reject":
            leave.status = "Rejected"
            leave.save()
    return redirect("leave_approve")

@login_required
@never_cache
def department_list(request):
    departments = Department.objects.all().order_by("id")
    return render(
        request,
        "department_list.html",
        {"departments": departments}
    )


@login_required
@never_cache
def department_create(request):
    if request.method == "POST":

        department_id = request.POST.get("department_id")
        department_name = request.POST.get("department_name")

        if Department.objects.filter(id=department_id).exists():
            messages.error(
                request,
                "Department with this ID already exists."
            )
            return redirect("department_create")

        Department.objects.create(
            id=department_id,
            name=department_name
        )

        return redirect("department_list")

    return render(
        request,
        "department_add_update.html",
        {
            "is_update": False,
        }
    )


@login_required
@never_cache
def department_update(request, id):
    department = get_object_or_404(
        Department,
        id=id
    )

    if request.method == "POST":
        department.id = request.POST.get("department_id")
        department.name = request.POST.get("department_name")

        department.save()
        return redirect("department_list")

    return render(
        request,
        "department_add_update.html",
        {
            "department": department,
            "is_update": True,
        }
    )

@login_required
@never_cache
def department_delete(request, id):
    department = get_object_or_404(Department, id=id)
    try:
        department.delete()
        messages.success(request, f"Department '{department.name}' deleted successfully.")
    except ProtectedError:
        messages.error(
            request,
            f"Cannot delete '{department.name}' — it still has employees assigned to it."
        )
    return redirect("department_list")

@login_required
@never_cache
def designation_list(request):
    designation = Designation.objects.all().order_by("id")
    return render(
        request,
        "designation_list.html",
        {"designation": designation}
    )

def designation_create(request):
    if request.method == "POST":

        designation_id = request.POST.get("designation_id")
        designation_name = request.POST.get("designation_name")

        if Designation.objects.filter(id=designation_id).exists():
            messages.error(
                request,
                "Designation with this ID already exists."
            )
            return redirect("designation_create")

        Designation.objects.create(
            id=designation_id,
            name=designation_name
        )
        return redirect("designation_list")

    return render(
        request,
        "designation_add_update.html",
        {
            "is_update": False,
        }
    )

@login_required
@never_cache
def designation_update(request, id):
    designation = get_object_or_404(
        Designation,
        id=id
    )

    if request.method == "POST":
        designation.id = request.POST.get("designation_id")
        designation.name = request.POST.get("designation_name")

        designation.save()
        return redirect("designation_list")

    return render(
        request,
        "designation_add_update.html",
        {
            "designation": designation,
            "is_update": True,
        }
    )

@login_required
@never_cache
def designation_delete(request, id):
    designation = get_object_or_404(Designation, id=id)
    try:
        designation.delete()
        messages.success(request, f"Department '{designation.name}' deleted successfully.")
    except ProtectedError:
        messages.error(
            request,
            f"Cannot delete '{designation.name}' — it still has employees assigned to it."
        )
    return redirect("designation_list")




@login_required
def calendar_view(request):
    return render(request, 'leave_approve.html')


@login_required
def calendar_events(request):
    events = CalendarEvent.objects.all().order_by('start_date', 'start_time')

    event_list = []

    for event in events:

        event_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description or '',
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'allDay': event.all_day,
            'category': event.category,
        }

        if event.start_time and not event.all_day:
            event_data['start'] = (
                f"{event.start_date.isoformat()}T"
                f"{event.start_time.strftime('%H:%M:%S')}"
            )

        if event.end_time and not event.all_day:
            event_data['end'] = (
                f"{event.end_date.isoformat()}T"
                f"{event.end_time.strftime('%H:%M:%S')}"
            )

        event_list.append(event_data)

    return JsonResponse(event_list, safe=False)


@login_required
@require_http_methods(["POST"])
def create_calendar_event(request):

    try:
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_time = request.POST.get('start_time') or None
        end_time = request.POST.get('end_time') or None
        category = request.POST.get('category', 'other')
        all_day = request.POST.get('all_day') == 'true'

        if not title:
            return JsonResponse({
                'success': False,
                'error': 'Event title is required.'
            }, status=400)

        if not start_date:
            return JsonResponse({
                'success': False,
                'error': 'Start date is required.'
            }, status=400)

        if not end_date:
            end_date = start_date

        event = CalendarEvent.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            all_day=all_day,
            category=category,
            created_by=request.user
        )

        return JsonResponse({
            'success': True,
            'message': 'Event created successfully.',
            'event_id': event.id
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def update_calendar_event(request, event_id):

    event = get_object_or_404(
        CalendarEvent,
        id=event_id
    )

    try:

        event.title = request.POST.get(
            'title',
            event.title
        )

        event.description = request.POST.get(
            'description',
            ''
        )

        event.start_date = request.POST.get(
            'start_date',
            event.start_date
        )

        event.end_date = request.POST.get(
            'end_date',
            event.start_date
        )

        event.start_time = request.POST.get(
            'start_time'
        ) or None

        event.end_time = request.POST.get(
            'end_time'
        ) or None

        event.category = request.POST.get(
            'category',
            event.category
        )

        event.all_day = request.POST.get(
            'all_day'
        ) == 'true'

        event.save()

        return JsonResponse({
            'success': True,
            'message': 'Event updated successfully.'
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def delete_calendar_event(request, event_id):

    event = get_object_or_404(
        CalendarEvent,
        id=event_id
    )

    event.delete()

    return JsonResponse({
        'success': True,
        'message': 'Event deleted successfully.'
    })