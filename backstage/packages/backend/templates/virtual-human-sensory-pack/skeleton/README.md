# VH Sensory Pack

This project will receive kafka messages in a text format, 
extract emotion using a specific LLM and send the message
containing user emotion and query back using kafka.

## The emotion list

This emotions can be given back in the response
```json
[
    "Hope", "Gratitude", "Admiration", "Gratification", "HappyFor", "Joy", "Love",
    "Pride", "Relief", "Satisfaction", "Gloating", "Remorse", "Disappointment",
    "Fear", "Shame", "Resentment", "Fears-confirmed", "Pity", "Distress",
    "Anger", "Hate", "Reproach", "Amusement", "Annoyance", "Approval", "Caring", "Confusion", "Curiosity",
    "Desire", "Disapproval", "Disgust", "Embarrassment", "Excitement", "Grief",
    "Nervousness", "Optimism", "Realization", "Sadness", "Surprise"
]
```
