import os
import argparse

use_hour = False


def hour(start):
    if int(start.split(':')[0]) > 0:
        use_hour = True
        return True
    else:
        return False


class Track():
    def __init__(self, title='', performer='', index=0, start=''):
        self.title = title
        self.performer = performer
        self.index = index
        self.start = start
        self.uses_hour = hour(start)

    def __str__(self) -> str:
        if self.uses_hour:
            return f'{self.start}: {self.title} - {self.performer}'
        else:
            return f'{self.start.split(":", 1)[1]}: {self.title} - {self.performer}'


def parse(lines):
    title = ""
    performer = ""
    index = ""
    start = ""
    for line in lines:
        line = line.strip()
        if line.startswith('TITLE'):
            title = line.split('"')[1]
        elif line.startswith('PERFORMER'):
            performer = line.split('"')[1]
        elif line.startswith('INDEX'):
            index = int(line.split(' ')[1])
            start = line.split(' ')[2]
    return Track(title, performer, index, start)


def parse_cue(cue_file):
    tracks = []
    with open(cue_file, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        if lines[i].startswith('TRACK'):
            track = parse(lines[i:i + 5])
            tracks.append(track)
    return tracks


def write_txt(txt_file, tracks):
    with open(txt_file, 'w') as f:
        for track in tracks:
            f.write(str(track) + '\n')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert recordbox to txt')
    parser.add_argument('--cue', type=str, default=None, help='tracklist.cue file')
    parser.add_argument('--txt', type=str, default=None, help='tracklist.txt file')
    parser.add_argument('--overwrite', action='store_true', help='overwrite txt file')

    args = parser.parse_args()

    pwd = os.getcwd()
    if not args.cue:
        for file in os.listdir('.'):
            if file.endswith('.cue'):
                args.cue = file
                break
        if not args.cue:
            print('No cue file found')
            exit()
    if not args.txt:
        args.txt = args.cue.replace('.cue', '.txt')
    if os.path.exists(args.txt) and not args.overwrite:
        print('txt file already exists')
        exit()
    tracks = parse_cue(args.cue)
    write_txt(args.txt, tracks)
