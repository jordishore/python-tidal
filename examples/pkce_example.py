# -*- coding: utf-8 -*-

# Copyright (C) 2023- The Tidalapi Developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""pkce_example.py: A simple example script that describes how to use PKCE login and MPEG-DASH streams"""

import tidalapi
from tidalapi import Quality
from pathlib import Path

session_file1 = Path("tidal-session-pkce.json")

session = tidalapi.Session()
# Load session from file; create a new session if necessary
session.login_session_file(session_file1, do_pkce=True)

# Override the required playback quality, if necessary
# Note: Set the quality according to your subscription.
# Low: Quality.low_96k          (m4a 96k)
# Normal: Quality.low_320k      (m4a 320k)
# HiFi: Quality.high_lossless   (FLAC)
# HiFi+ Quality.hi_res          (FLAC MQA)
# HiFi+ Quality.hi_res_lossless (FLAC HI_RES)
session.audio_quality = Quality.hi_res_lossless
# album_id = "249593867"  # Alice In Chains / We Die Young (Max quality: HI_RES MHA1 SONY360)
# album_id = "77640617"   # U2 / Achtung Baby              (Max quality: HI_RES MQA, 16bit/44100Hz)
# album_id = "110827651"  # The Black Keys / Let's Rock    (Max quality: LOSSLESS FLAC, 24bit/48000Hz)
album_id = "77646169"    # Beck / Sea Change               (Max quality: HI_RES_LOSSLESS FLAC, 24bit/192000Hz)
album = session.album(album_id)
res = album.get_audio_resolution()
tracks = album.tracks()
# list album tracks
for track in tracks:
    print("{}: '{}' by '{}'".format(track.id, track.name, track.artist.name))
    stream = track.get_stream()
    print("MimeType:{}".format(stream.manifest_mime_type))

    manifest = stream.get_stream_manifest()
    audio_resolution = stream.get_audio_resolution()

    print("track:{}, (quality:{}, codec:{}, {}bit/{}Hz)".format(track.id,
                                                                stream.audio_quality,
                                                                manifest.get_codecs(),
                                                                audio_resolution[0],
                                                                audio_resolution[1]))
    if stream.is_MPD:
        # HI_RES_LOSSLESS quality supported when using MPEG-DASH stream (PKCE only!)
        # 1. Export as MPD manifest
        mpd = stream.get_manifest_data()
        # 2. Export as HLS m3u8 playlist
        hls = manifest.get_hls()
        # with open("{}_{}.mpd".format(album_id, track.id), "w") as my_file:
        #    my_file.write(mpd)
        # with open("{}_{}.m3u8".format(album_id, track.id), "w") as my_file:
        #    my_file.write(hls)
    elif stream.is_BTS:
        # Direct URL (m4a or flac) is available for Quality < HI_RES_LOSSLESS
        url = manifest.get_urls()
    break
