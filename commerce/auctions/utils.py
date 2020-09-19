from .models import Watchlist

def get_watchlist_count(user):
    watchlist_count = ""
    try:
        watchlist_count = Watchlist.objects.filter(user=user).count()
    except:
        pass

    return watchlist_count