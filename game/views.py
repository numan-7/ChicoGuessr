from django.shortcuts import render, redirect
from game.forms import GuessForm
from game.forms import JoinForm, LoginForm
from game.models import Game, Score, Leaderboard
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
import os, math, json, random
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import requests
from django.http import JsonResponse

def calculate_distance(correct_lat, correct_lng, guess_lat, guess_lng):
    # Convert the latitudes and longitudes to radians
    correct_lat, correct_lng, guess_lat, guess_lng = map(math.radians, [correct_lat, correct_lng, guess_lat, guess_lng])

    # Calculate the distance using the Haversine formula
    dlat = guess_lat - correct_lat
    dlon = guess_lng - correct_lng
    a = math.sin(dlat/2)**2 + math.cos(correct_lat) * math.cos(guess_lat) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # Approximate radius of the earth in km
    return distance

def update_leaderboard():
    scores = Score.objects.exclude(high_score=0).order_by('-high_score', '-average_score')
    leaderboard_entries = []
    for score in scores:
        leaderboard_entry, _ = Leaderboard.objects.get_or_create(user=score.user)
        leaderboard_entry.score = score.high_score
        leaderboard_entry.average_score = score.average_score
        leaderboard_entry.save()
        leaderboard_entries.append(leaderboard_entry)
    return leaderboard_entries


@login_required(login_url='/login/')
def user_stats(request):
    update_leaderboard()
    try:
        score_instance = Score.objects.get(user=request.user)
        high_score = score_instance.high_score
        last_score = score_instance.last_score
        games_played = score_instance.games_played
        created_at = score_instance.created_at
        lowest_score = score_instance.lowest_score
        average_score = score_instance.average_score

    except ObjectDoesNotExist:
        # If the user does not have a score instance, set high_score to 0
        high_score = 0
        last_score = 0
        games_played = 0
        lowest_score = 0
        average_score = 0
        last_score = 0
        created_at = timezone.now()
    leaderboard = Leaderboard.objects.order_by('-score', '-average_score')
    # Find the user's position on the leaderboard
    user_position = -1
    for position, entry in enumerate(leaderboard, start=1):
        if entry.user == request.user:
            user_position = position
            break
    average_score = round(average_score, 2)
    return render(request, 'userstats.html', {'high_score': high_score, 'lowest_score': lowest_score, 'average_score': average_score, 'last_score': last_score, 'games_played': games_played, 'leaderboard': leaderboard, 'created_at': created_at, 'user_position': user_position})

@login_required(login_url='/login/')
def search_user_stats(request, userid):
    try:
        score_instance = Score.objects.get(user_id=userid)
        # Find the user's position on the leaderboard
        leaderboard = Leaderboard.objects.order_by('-score', '-average_score')
        user_position = -1
        for position, entry in enumerate(leaderboard, start=1):
            if entry.user_id == userid:
                user_position = position
                break
        data = {
            'high_score': score_instance.high_score,
            'lowest_score': score_instance.lowest_score,
            'average_score': round(score_instance.average_score, 2),
            'last_score': score_instance.last_score,
            'games_played': score_instance.games_played,
            'created_at': score_instance.created_at,
            'user_position': user_position,
        }
        return JsonResponse(data)

    except ObjectDoesNotExist:
        return JsonResponse({
            'error': 'User not found or user does not have any stats.'
        }, status=404)

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def about_us(request):
    return render(request, 'about.html')

@login_required(login_url='/login/')
def loadStreetAPI(request):
    if request.META.get('HTTP_SEC_FETCH_DEST') == 'document':
        return HttpResponseForbidden("L")
    else:
        API_KEY = os.getenv('API_KEY')
        url = f'https://maps.googleapis.com/maps/api/js?key={API_KEY}&callback=initStreetView'
        response = requests.get(url)
        return HttpResponse(response.content, content_type='application/javascript')

@login_required(login_url='/login/')
def loadMapAPI(request):
    if request.META.get('HTTP_SEC_FETCH_DEST') == 'document':
        return HttpResponseForbidden("L")
    else:
        API_KEY = os.getenv('API_KEY')
        url = f'https://maps.googleapis.com/maps/api/js?key={API_KEY}&callback=initMap'
        response = requests.get(url)
        return HttpResponse(response.content, content_type='application/javascript')


@login_required(login_url='/login/')
def game(request):
    # Load the locations data from the locations.json file
    with open('./static/locations/locations.json', 'r') as f:
        locations_data = json.load(f)
    # Retrieve or create the game associated with the user
    user_game, _ = Game.objects.get_or_create(user=request.user)
    # If a user refreshes on the results page
    if request.method == 'POST' and not user_game.random_location:
        return HttpResponseRedirect(('/game/'))
    # Check if this is the final round
    if user_game.round == 5:
        # This is the final round, so calculate the final score and render the final template
        final_score = user_game.score
        guesses = user_game.guesses
        # Reset game state
        user_game.save_game(0, 0, [])
        context = {
            'final_score': round(final_score),
            'guesses': guesses
        }
        return render(request, 'final.html', context)

    if request.method == 'POST' and 'coords_guess' in request.POST:
        # Get the current random location from the session and remove it
        lat, lng = [float(coord) for coord in user_game.random_location.split(",")]
        # Set the location to the one from the session
        lat = float(lat)
        lng = float(lng)
        # Create a form instance and populate it with data from the request
        form = GuessForm(request.POST)
        if form.is_valid():
            # Get the latitude and longitude values from the form
            guess_lat = float(form.cleaned_data['guessLat'])
            guess_lng = float(form.cleaned_data['guessLng'])
            # Get Distance Difference
            distance = calculate_distance(lat, lng, guess_lat, guess_lng)
            # Calculate Score
            if(distance < 0.0325):
                score = 5000
            else:
                score = 5000 * math.exp(-0.15 * distance)
            # Convert To Miles
            distance *= 0.621371
            # Update game state
            user_game.save_game(user_game.score + score, user_game.round + 1, user_game.guesses + [(guess_lat, guess_lng, lat, lng)], "")
            # Round Distance
            mile_difference = round(distance, 2)
            # Pass the variables to the result template
            context = {
                'correct_coords': [lat, lng],
                'guess_coords': [guess_lat, guess_lng],
                'score': round(score),
                'round': user_game.round,
                'mile_difference': mile_difference,
            }
            return render(request, 'result.html', context)
        else:
            print(form.errors)
    else:
        # Check if the game already has a random location
        if not user_game.random_location:
            # Get a new random location
            random_location = random.choice(locations_data)
            lat, lng = [float(coord) for coord in random_location]
            # Store the location in the game model
            user_game.save_game(user_game.score, user_game.round, user_game.guesses, f"{lat},{lng}")
        else:
            # Get the stored random location and convert it to floats
            lat, lng = [float(coord) for coord in user_game.random_location.split(",")]
        # Initialize the GuessForm with the correct coordinates
        form = GuessForm()
        # Increment the round number
        roundNum = user_game.round + 1
    # Pass the lat, lng variables to the template along with the form
    context = {'lat': lat, 'lng': lng, 'form': form, 'round': roundNum}
    return render(request, 'game.html', context)

def join(request):
    if (request.method == "POST"):
        jform = JoinForm(request.POST)
        if (jform.is_valid()):
            N_user = jform.save()
            N_user.set_password(N_user.password)
            N_user.save()
            score_instance = Score.objects.create(user=N_user, created_at=timezone.now())
            score_instance.save()
            return redirect("/")
        else:
            page_data = { "join_form": jform }
            return render(request, 'join.html', page_data)
    else:
        jform = JoinForm()
        page_data = { "join_form": jform }
        return render(request, 'join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data["username"]
            password = lform.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect("/")
                else:
                    return HttpResponse("This account is not active.")
            else:
                return render(request, 'login.html', {"login_form": LoginForm, "correct": False})
    else:
        return render(request, 'login.html', {"login_form": LoginForm, "correct": True})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login/')
def server_info(request):
    server_geodata = requests.get('https://ipwhois.app/json/').json()
    settings_dump = settings.__dict__
    combined_data = {**server_geodata, **settings_dump}
    context = {'combined_data': combined_data}
    return render(request, 'serverinfo.html', context)
