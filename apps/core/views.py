from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from apps.events.models import Event
from apps.post.models import Post
from apps.stats.models import Fixture, get_top_scorers_summary, Injury
from .models import get_featured


def recent_posts_or_events():
    posts = list(Post.recent())
    events = list(Event.recent())
    p_o_e = posts + events
    p_o_e.sort(key=lambda x: x.date, reverse=True)
    return p_o_e


def google_form(request):
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfJr3rNG5zTRF_w_aSaVffzLWuJRa-nI5Ji6-YvdlTQjF7Mvw/viewform")


def home(request):
    next_match = Fixture.get_next_match()
    recent_results = Fixture.recent_results().select_related('opponent')
    standings = cache.get('epl_standings')
    top_scorers = get_top_scorers_summary()
    injuries = Injury.get_current_injuries()
    recent_posts = recent_posts_or_events()
    featured = get_featured()
    context = {
        'next_match': next_match,
        'recent_results': recent_results,
        'standings': standings,
        'players': top_scorers,
        'injuries': injuries,
        'posts': recent_posts,
        'featured': featured,
    }
    return render(request, 'home.html', context)


@user_passes_test(lambda u: u.is_superuser)
def clear_cache(request):
    from django.core.cache import cache
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    from django.contrib import messages

    cache.clear()

    try:
        cache._cache.flush_all()
    except AttributeError:
        pass
    try:
        cache._cache.clear()
    except AttributeError:
        pass
    try:
        cache._expire_info.clear()
    except AttributeError:
        pass

    # django-redis
    try:
        cache.cache.clear()
    except AttributeError:
        pass

    # django-cacheops
    try:
        from cacheops.conf import redis_client

        redis_client.flushdb()
    except ImportError:
        pass

    messages.info(request, "Cache Cleared")
    try:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except KeyError:
        return HttpResponseRedirect(reverse("admin:index"))
    return HttpResponseRedirect(reverse("admin:index"))
