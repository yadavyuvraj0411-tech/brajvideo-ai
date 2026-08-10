def create_scene_plan(story, duration_minutes=10):
    """
    Creates a basic scene structure for a long AI video.

    Later we will connect this to an AI language model so
    the scenes are generated automatically.
    """

    total_shots = duration_minutes * 7

    scenes = []

    for i in range(1, total_shots + 1):
        scenes.append({
            "shot": i,
            "duration_seconds": 8,
            "prompt": story,
            "status": "waiting"
        })

    return {
        "duration_minutes": duration_minutes,
        "total_shots": total_shots,
        "shots": scenes
    }


if __name__ == "__main__":

    example = create_scene_plan(
        "Bal Krishna playing with his friends in Vrindavan",
        10
    )

    print(example)
