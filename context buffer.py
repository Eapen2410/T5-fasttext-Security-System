from collections import deque
from datetime import datetime
import numpy as np

context_buffer = deque(maxlen=5)
def add_to_context(query, label):
    context_buffer.append({
        "query": query,
        "label": label,
        "timestamp": datetime.now()
    })
for query in queries:
    label, confidence = model.predict(query)
    confidence = np.asarray(confidence)

    print(f"Query: {query}\nPredicted: {label[0]} | Confidence: {confidence[0]:.4f}\n")

    context_buffer.append({
        "query": query,
        "label": label[0],
        "confidence": float(confidence[0]),
        "timestamp": datetime.now()
    })
import pandas as pd
df = pd.DataFrame(list(context_buffer))
df.to_csv("context_buffer_log.csv", index=False)
