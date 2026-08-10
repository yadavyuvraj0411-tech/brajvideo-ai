import uuid
from datetime import datetime

jobs = {}


def create_job(prompt, duration_minutes=10, language="Hindi"):
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "id": job_id,
        "prompt": prompt,
        "duration_minutes": duration_minutes,
        "language": language,
        "status": "queued",
        "created_at": datetime.utcnow().isoformat(),
        "progress": 0,
        "clips_generated": 0,
        "total_clips": duration_minutes * 7,
        "video_url": None
    }

    return jobs[job_id]


def update_job(job_id, progress, clips_generated):
    if job_id not in jobs:
        return None

    jobs[job_id]["progress"] = progress
    jobs[job_id]["clips_generated"] = clips_generated

    if progress >= 100:
        jobs[job_id]["status"] = "completed"
    else:
        jobs[job_id]["status"] = "generating"

    return jobs[job_id]


def get_job(job_id):
    return jobs.get(job_id)


if __name__ == "__main__":
    job = create_job(
        "Create a story about Bal Krishna in Vrindavan",
        10,
        "Brajbhasha"
    )

    print("Created job:")
    print(job)
