import json
import argparse
from PIL import Image
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Source directory of img assets.")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output directory for resized images.",
        default="./",
    )
    parser.add_argument(
        "-s",
        "--subject",
        type=str,
        help="File to insert into the images.",
        default="src.png",
    )
    args = parser.parse_args()

    src_dir = args.source
    dst_dir = args.output
    src_img = args.subject

    src = Image.open(src_img)
    for file in os.listdir(src_dir):
        if not file.endswith(".json"):
            continue
        print(f"Proccessing {file}...")
        png = file[:-4]
        f = open(f"{src_dir}/{file}")
        data = json.load(f)["textures"][0]
        dst = Image.new("RGBA", (data["size"]["w"], data["size"]["h"]))

        for frame in data["frames"]:
            cur = src.resize((frame["sourceSize"]["w"], frame["sourceSize"]["h"]))
            Image.Image.paste(dst, cur, (frame["frame"]["x"], frame["frame"]["y"]))
        dst.save(f"{dst_dir}/{png}png")
    print("done")
