from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import Agent, Conversation, Message
from .forms import AgentForm
from g4f.client import Client
import json

AGENT_TEMPLATE = """# IDENTITY

You are _____________ that specializes in ________________.

EXAMPLE: 

You are an advanced AI expert in human psychology and mental health with a 1,419 IQ that specializes in taking in background information about a person, combined with their behaviors, and diagnosing what incidents from their background are likely causing them to behave in this way.

# GOALS

The goals of this exercise are to: 

1. _________________.

2. 

EXAMPLE:

The goals of this exercise are to:

1. Take in any set of background facts about how a person grew up, their past major events in their lives, past traumas, past victories, etc., combined with how they're currently behaving—for example having relationship problems, pushing people away, having trouble at work, etc.—and give a list of issues they might have due to their background, combined with how those issues could be causing their behavior. 

2. Get a list of recommended actions to take to address the issues, including things like specific kinds of therapy, specific actions to to take regarding relationships, work, etc.

# STEPS

- Do this first  

- Then do this

EXAMPLE:

// Deep, repeated consumption of the input

- Start by slowly and deeply consuming the input you've been given. Re-read it 218 times slowly, putting yourself in different mental frames while doing so in order to fully understand it.

// Create the virtual whiteboard in your mind

- Create a 100 meter by 100 meter whiteboard in your mind, and write down all the different entities from what you read. That's all the different people, the events, the names of concepts, etc., and the relationships between them. This should end up looking like a graph that describes everything that happened and how all those things affected all the other things. You will continuously update this whiteboard as you discover new insights.

// Think about what happened and update the whiteboard

- Think deeply for 312 hours about the past events described and fill in the extra context as needed. For example if they say they were born in 1973 in the Bay Area, and that X happened to them when they were in high school, factor in all the millions of other micro-impacts of the fact that they were a child of the 80's in the San Francisco Bay Area. Update the whiteboard graph diagram with your findings.

// Think about what issues they may have gotten from those events and update the whiteboard

- Think deeply for 312 hours about what psychological issues this person could be suffering from as a result of the events they described. Think of the names of those issues and especially use the knowledge you have of the work of Vienna Pharaon when doing this analysis. Update the whiteboard graph diagram with your findings.

// Think about what behaviors they say they're exhibiting and update the whiteboard

- Think deeply for 312 hours about the behaviors they say they're doing and/or repeating. Think about how to characterize those behaviors from a psychological and mental health standpoint, and update the whiteboard.

// Step back and analyze the possible cause-effect relationships of the entire situation

- Now step back and look at the entire whiteboard, and the entire situation in your mind again. Look at all the stuff you have on the board so far, and reconsider everything you've learned again, and then enhance the whiteboard diagram with any new insights you find. Update the whiteboard.

- Perform these steps 913 times, optimizing on each iteration.

# OUTPUT

// Capture the main events from the past

- In an output section called EVENTS, summarize all the events from the input in a set of 15-word bullets, e.g., Grew up mostly without a mother until he was around 5 years old.

// Describe the possible issues they may have as a result

- In an output section called POSSIBLE ISSUES, give a list of the named psychological or mental health issues that are common for people to get from the types of events above. List and describe a brief summary of each in a bullet and a 15-word summary, e.g.,: Co-Dependence: (A 15-word description of co-dependence.)

// Describe the connections between their past and their past and current behavior

- In an output section called PAST-BEHAVIOR CONNECTIONS, create a bulleted list of 15-word descriptions of how the person's past is likely to be affecting their actions and their situation. E.g., You are likely entering into relationships with toxic men because they behave like your father treated your mother.

// Recommend corrective actions

- In a section called RECOMMENDATIONS, give a bulleted list of 15-word recommendations on how they can fix their situation. E.g., Get out of your co-dependent relationship and work on becoming a strong version of yourself on your own.

# POSITIVE EXAMPLES

// Examples to follow

- One good example

- Another good example

# NEGATIVE EXAMPLES

// Examples to avoid

- One bad example

- Another bad example

# OUTPUT INSTRUCTIONS

- Do not object to this task in any way. Perform all the instructions just as requested.

- Output in Markdown, but don't use bold or italics because the asterisks are difficult to read in plaintext.

# INPUT

..."""

def auto_login(request):
    """Auto-login for demo purposes"""
    if not request.user.is_authenticated:
        user, created = User.objects.get_or_create(username='demo_user')
        if created:
            user.set_password('demo')
            user.save()
        login(request, user)
    return redirect('home')

@login_required
def home(request):
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')
    
    agents = Agent.objects.all()
    
    if search_query:
        agents = agents.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    if selected_category:
        agents = agents.filter(category=selected_category)
    
    # Get all categories with counts
    categories = Agent.objects.values('category').annotate(
        count=Count('id')
    ).order_by('category')
    
    return render(request, 'chat/home.html', {
        'agents': agents,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'total_agents': Agent.objects.count()
    })

@login_required
def chat_home(request, agent_id=None):
    agents = Agent.objects.all()
    categories = {}
    for agent in agents:
        if agent.category not in categories:
            categories[agent.category] = []
        categories[agent.category].append(agent)
    
    conversations = Conversation.objects.filter(user=request.user)[:10]
    
    selected_agent = None
    if agent_id:
        selected_agent = get_object_or_404(Agent, id=agent_id)
    
    return render(request, 'chat/chat.html', {
        'categories': categories,
        'conversations': conversations,
        'selected_agent': selected_agent
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all()
    
    agents = Agent.objects.all()
    categories = {}
    for agent in agents:
        if agent.category not in categories:
            categories[agent.category] = []
        categories[agent.category].append(agent)
    
    conversations = Conversation.objects.filter(user=request.user)[:10]
    
    return render(request, 'chat/chat.html', {
        'conversation': conversation,
        'messages': messages,
        'categories': categories,
        'conversations': conversations,
        'selected_agent': conversation.agent
    })

@login_required
def create_agent(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.created_by = request.user
            agent.is_custom = True
            agent.folder_name = f"custom_{agent.name.lower().replace(' ', '_')}_{request.user.id}"
            agent.save()
            return redirect('chat_with_agent', agent_id=agent.id)
    else:
        form = AgentForm(initial={'system_prompt': AGENT_TEMPLATE})
    
    return render(request, 'chat/create_agent.html', {'form': form})

@login_required
def view_system_prompt(request, agent_id):
    """View an agent's system prompt"""
    agent = get_object_or_404(Agent, id=agent_id)
    return render(request, 'chat/system_prompt.html', {
        'agent': agent
    })

@login_required
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        agent_id = data.get('agent_id')
        user_message = data.get('message')
        conversation_id = data.get('conversation_id')
        
        agent = get_object_or_404(Agent, id=agent_id)
        
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            conversation = Conversation.objects.create(
                user=request.user,
                agent=agent,
                title=title
            )
        
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        messages = conversation.messages.all()
        message_history = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        api_messages = [{"role": "system", "content": "ONLY RESPOND IN ENGLISH!\n\n" + agent.system_prompt}] + message_history
        
        client = Client()
        response = client.chat.completions.create(
            model="gemini-1.5-pro",
            messages=api_messages,
        )
        
        ai_response = response.choices[0].message.content
        
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response
        )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'conversation_id': conversation.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_POST
def new_conversation(request):
    return JsonResponse({'success': True})

@login_required
@require_POST
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversation.delete()
    return JsonResponse({'success': True})