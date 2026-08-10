import os
import time
from pathlib import Path


OUTPUT_DIR = Path("generated_videos")
OUTPUT_DIR.mkdir(exist_ok=True)


def prepare_shot(shot_number, prompt, duration_seconds=8):
    """
    Prepare one video shot for the AI video engine.
    """

    return {
        "shot_number": shot_number,
        "prompt": prompt,
        "duration_seconds": duration_seconds,
        "status": "waiting"
    }


def generate_shot(shot):
    """
    Placeholder for the real AI video model.

    The actual Wan/LTX/etc. model will be connected here.
    """

    print(f"Generating shot {shot['shot_number']}...")
    print(f"Prompt: {shot['prompt']}")

    # The actual GPU model will replace this section.
    time.sleep(1)

    filename = (
        OUTPUT_DIR /
        f"shot_{shot['shot_number']:04d}.mp4"
    )

    return {
        "shot_number": shot["shot_number"],
        "status": "ready",
        "file": str(filename)
    }


def generate_video_from_shots(shots):
    """
    Process all shots sequentially.
    """

    results = []

    total = len(shots)

    for index, shot in enumerate(shots, start=1):

        result = generate_shot(shot)

        results.append(result)

        progress = int((index / total) * 100)

        print(
            f"Progress: {progress}% "
            f"({index}/{total})"
        )

    return results


if __name__ == "__main__":

    example_shots = [
        prepare_shot(
            1,
            "A cinematic morning view of Vrindavan beside the Yamuna.",
            8
        ),
        prepare_shot(
            2,
            "Bal Krishna walking through Vrindavan with his friends.",
            8
        )
    ]

    results = generate_video_from_shots(example_shots)

    print("\nGeneration finished:")
    print(results)
