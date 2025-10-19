from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import StudyNote
from .forms import StudyNoteForm

@login_required
def notes_page(request):
    # Handle note upload
    if request.method == "POST":
        form = StudyNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploader = request.user
            note.save()
            messages.success(request, "Note uploaded successfully!")
            return redirect(f"{request.path}?highlight={note.id}")
    else:
        form = StudyNoteForm()

    # Handle search
    query = request.GET.get("q", "")
    if query:
        notes = StudyNote.objects.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(uploader__username__icontains=query)
        ).order_by("-upload_date")
    else:
        notes = StudyNote.objects.all().order_by("-upload_date")

    # Pagination
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    highlight_id = request.GET.get("highlight")

    return render(request, "notes/notes.html", {
        "form": form,
        "notes": page_obj,
        "highlight_id": highlight_id
    })
