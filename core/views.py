from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from chat.models import ChatRoom
from .forms import SignUpForm


@login_required
def frontpage(request):
    # Check if the request method is POST
    if request.method == "POST":
        room_name = request.POST.get(
            "name"
        )  # Retrieve the 'name' parameter from the POST data

        if ChatRoom.objects.filter(name=room_name).exists():
            # Room with the same name already exists, redirect to the existing room
            return redirect("/chat/messages/chat_" + room_name + "/")
        else:
            # Create a new room if it doesn't exist and redirect to the rooms list
            new_room = ChatRoom.objects.create(
                name=room_name, slug="chat_{}".format(room_name)
            )
            new_room.save()
            return redirect("/chat/chat_rooms")
    else:
        return render(request, "core/frontpage.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "core/signup.html", {"form": form})
