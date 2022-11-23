import os
import json
import argparse
import subprocess
import requests
from dotenv import load_dotenv
from tqdm import tqdm


def download_video_info(video_id: str) -> None:
    header = {"authorization": os.environ.get('BEARER_TOKEN')}
    for id in tqdm(video_id):
        os.makedirs(id, exist_ok=True)
        response = requests.get(
            f'https://api.p-c3-e.abema-tv.com/v1/video/programs/{id}', headers=header).json()

        with open(f"{id}/{id}.json", 'w') as f:
            json.dump(response, f, ensure_ascii=False)


def download_video(video_id: str) -> any:
    return_list = []
    if type(video_id) is list:
        for id in tqdm(video_id):
            os.makedirs(id, exist_ok=True)
            return_list.append(subprocess.call(
                ['streamlink',
                 f'https://abema.tv/video/episode/{id}', 'best', '-o', f'./{id}/{id}.ts']))
    return return_list


def download_thumbnail(video_id: str | list[str]) -> any:
    def download_process(video_id):
        os.makedirs(video_id, exist_ok=True)
        thumbnail_count = 1
        while True:
            response = requests.get(
                f'https://hayabusa.io/abema/programs/{video_id}/thumb00{thumbnail_count}')
            if response.status_code != 200:
                break
            with open(f'{video_id}/thumb00{thumbnail_count}.png', 'wb') as f:
                f.write(response.content)
            thumbnail_count += 1

    if type(video_id) is list:
        for id in tqdm(video_id):
            download_process(id)
    else:
        download_process()


def main():
    parser = argparse.ArgumentParser(
        prog='Peregrine Utility',
        usage='Tools for Peregrine.',
        description='description',
        epilog='end',
        add_help=True,
    )

    parser.add_argument('-vid', nargs='*')
    parser.add_argument('--skip-video-info-download',
                        default=False, action='store_true')
    parser.add_argument('--skip-thumbnail-download',
                        default=False, action='store_true')
    parser.add_argument('--skip-video-download',
                        default=False, action='store_true')
    args = parser.parse_args()

    if not args.skip_thumbnail_download:
        download_thumbnail(args.vid)
    if not args.skip_video_info_download:
        download_video_info(args.vid)
    if not args.skip_video_download:
        download_video(args.vid)


if __name__ == '__main__':
    load_dotenv()
    main()
