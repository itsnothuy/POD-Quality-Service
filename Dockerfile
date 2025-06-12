FROM python:3.12-slim

# 1. System-level deps: OpenCV needs libglib & libsm…
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends libglib2.0-0 libsm6 libxext6 libxrender-dev && \
#     rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*
# 2. Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy application code last (better layer caching during dev)
COPY . .

# 4. Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
