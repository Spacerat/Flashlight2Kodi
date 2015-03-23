#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, subprocess
import youtubetoxbmc
from youtube import YoutubeSearch
from xbmcjson import XBMC, PLAYER_VIDEO
from soundcloudSearch import SoundcloudSearch

YOUTUBE_KEY = "AIzaSyDYJ8TlWYDc1JYjivcByjJ9gHzZGLP1qNI"
XBMC_URL = "http://localhost:8080/jsonrpc"
XBMC_USER = "ADMIN"
XBMC_PASSWORD = "PASSWORD"

def format_videos(videos, kind):
	return [{
				"title": 'Yt2Kodi: {}'.format(title), 
				"run_args": [kind, vid],
				"webview_transparent_background": True,
				"html": """<html>
				<head>
				<style>
					body {{
						font-family: Sans-serif;
					}}
					.thumb {{
					    margin-left: auto;
					    margin-right: auto;
					    width: 320px;
					}}
				</style>
				</head>
				<body>
					<h3>{}</h3>
					{}
					<p>{}</p>
				</body>
				</html>""".format(title, '<img class="thumb" src={}></img>'.format(thumb) if thumb else "", desc)
			} for title, vid, thumb, desc in videos]

def format_videos_bak(videos, kind):
	return [{
				"title": 'Yt2Kodi: {}'.format(title), 
				"run_args": [kind, vid]
			} for title, vid, thumb, desc in videos]

def results(fields, original_query):
	original_query = original_query.strip()
	commands = {
		'stop': {"title": "Stop Kodi", "run_args": ['stop', '']}, 
		'play': {"title": "Play/Pause Kodi", "run_args": ['p', '']},
	}

	if fields:
		#query = fields.get('~keywords')
		query = "".join(original_query.split()[1:])
		service = original_query.split()[0]

		if service in ["kodiyt"]:
			return format_videos(YoutubeSearch(YOUTUBE_KEY).get(query, 5), 'yt')

		elif service in ["kodisc"]:
			return format_videos(SoundcloudSearch("aa2f5d9818b648290db2e3d3cd3fc3d0").get(query, 5), 'sc')

	elif original_query == "kodi":
		return commands.values()
	else:
		command = original_query.split()[1]
		if command in commands.keys():
			return commands[command]


def getAllPlayers(xbmc):
	return [x['playerid'] for x in xbmc.Player.GetActivePlayers()['result']]

def run(command, arg):
	xbmc = XBMC(XBMC_URL, XBMC_USER, XBMC_PASSWORD)
	if command == 'yt':
		xbmc.Player.Open({"item": {"file" : "plugin://plugin.video.youtube/?action=play_video&videoid={}".format(arg)}})
	if command == 'sc':
		xbmc.Player.Open({"item": {"file" : "plugin://plugin.audio.soundcloud/play/?audio_id={}".format(arg)}})
	if command == 'stop':
		xbmc.Player.Stop(getAllPlayers(xbmc))
	if command == 'p':
		xbmc.Player.PlayPause([PLAYER_VIDEO])
