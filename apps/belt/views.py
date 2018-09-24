from django.shortcuts import render, redirect
from .models import *
import bcrypt, time


def index(request):

    return render(request, "belt/index.html")


def reg(request):

    errors = User.objects.validate_reg(request.POST)

    if errors:
        for key, val in errors.items():
            messages.info(request, val, extra_tags=key)
        request.session["first_name"] = request.POST["first_name"]
        request.session["last_name"] = request.POST["last_name"]
        request.session["email"] = request.POST["email"]
        return redirect("/")    # failure
    else:
        request.session.clear()
        hash_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=hash_pw)
        request.session["user_id"] = new_user.id
        request.session["user_name"] = new_user.first_name + " " + new_user.last_name

        return redirect("/dashboard")    # success


def login(request):

    result = User.objects.validate_login(request.POST)
    errors = result[0]

    if len(errors):
        for val in errors:
            messages.warning(request, val)
            request.session["email2"] = request.POST["email"]
        return redirect("/")    # failure
    else:
        request.session["user_id"] = result[1]["id"]
        request.session["user_name"] = result[1]["first_name"] + " " + result[1]["last_name"]
        request.session["secret_key"] = bcrypt.hashpw(str(result[1]["created_at"]).encode(), bcrypt.gensalt()).decode('utf8')

        return redirect("/dashboard")    # success


def dashboard(request):

    if "user_id" in request.session.keys():
        all_granted = Wish.objects.exclude(granted=False).order_by("-updated_at")
        wishes = Wish.objects.filter(user_id=request.session["user_id"]).exclude(granted=True)

        for wish in all_granted:
            wish.count_likes = len(Like.objects.filter(wish_id=wish.id))

        context = {
            "all_granted" : all_granted,
            "wishes" : wishes
        }
        
        return render(request, "belt/dashboard.html", context)

    return redirect("/")


def stats(request):

    if "user_id" in request.session.keys():
        wishes = Wish.objects.filter(granted=True)
        current_wishes = Wish.objects.filter(user_id=request.session["user_id"]).exclude(granted=True)
        granted_wishes = Wish.objects.filter(user_id=request.session["user_id"], granted=True)
    
    print(wishes)
    context = {
        "wishes" : len(wishes),
        "current_wishes" : len(current_wishes),
        "granted_wishes" : len(granted_wishes)
    }
    return render(request, "belt/stats.html", context)


def wish(request, id=None):

    if not "user_id" in request.session.keys():
        return redirect ("/")

    context = {}
    if id:
        wish = Wish.objects.get(id=id)
        context["wish"] = wish

    return render(request, "belt/wish.html", context)


def granted(request, id):

    if not "user_id" in request.session.keys():
        return redirect ("/")

    wish = Wish.objects.get(id=id)
    wish.granted = True
    wish.save()

    return redirect("/dashboard")


def like(request, id):

    if not "user_id" in request.session.keys():
        return redirect ("/")

    liked = Like.objects.filter(wish_id=id, user_id=request.session["user_id"])

    if not liked:
        Like.objects.create(wish_id=id, user_id=request.session["user_id"])

    return redirect("/dashboard")


def form(request, id=None): 

    if not "user_id" in request.session.keys():
        return redirect ("/")

    errors = {}

    if len(request.POST["wish"]) < 3:
        errors["wish"] = "Wish must be at least 3 characters"

    if len(request.POST["description"]) < 3:
        errors["description"] = "Description must be at least 3 characters"

    if errors and id:
        for key, val in errors.items():
            messages.info(request, val, extra_tags=key)
        return redirect("/wish/%s" % id)

    elif errors:
        for key, val in errors.items():
            messages.info(request, val, extra_tags=key)
        request.session["wish"] = request.POST["wish"]
        request.session["description"] = request.POST["description"]
        return redirect("/wish")


    if id:
        wish = Wish.objects.get(id=id)
        wish.wish = request.POST["wish"]
        wish.description = request.POST["description"]
        wish.save()
        return redirect("/dashboard")
    else:
        request.session.pop("wish", None)
        request.session.pop("description", None)
        Wish.objects.create(user=User.objects.get(id=request.session["user_id"]), wish=request.POST["wish"], description=request.POST["description"], granted=False)
        return redirect("/dashboard")


def logout(request):

    request.session.clear()

    return redirect("/")


def remove(request, id):

    if not "user_id" in request.session.keys():
        return redirect ("/")

    wish = Wish.objects.get(id=id)
    wish.delete()

    return redirect("/dashboard")



