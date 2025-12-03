import random
from django.shortcuts import render
from django.http import JsonResponse

from .models import ABTestLog

def ab_test_view(request):
    # Check if user already has a variant in session
    variant = request.session.get('ab_variant')
    
    if not variant:
        # Assign random variant: 'A' (kudos) or 'B' (thanks)
        variant = random.choice(['A', 'B'])
        request.session['ab_variant'] = variant

    # Log the view
    ABTestLog.objects.create(
        variant=variant,
        event_type='view',
        session_key=request.session.session_key,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )

    button_text = "kudos" if variant == 'A' else "thanks"
    
    context = {
        'team_members': ["Furui Guan", "Yichen Li", "Yilun Yang", "Aozuo Zheng"],
        'button_text': button_text,
        'variant': variant
    }
    return render(request, 'analytics/ab_test.html', context)


def ab_test_click(request):
    if request.method == 'POST':
        variant = request.session.get('ab_variant')
        
        # Check if already clicked in this session
        if request.session.get('ab_clicked'):
             return JsonResponse({'status': 'error', 'message': 'Already clicked'})

        if variant:
            ABTestLog.objects.create(
                variant=variant,
                event_type='click',
                session_key=request.session.session_key,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            # Mark session as clicked
            request.session['ab_clicked'] = True
            return JsonResponse({'status': 'success'})
            
    return JsonResponse({'status': 'error'}, status=400)
