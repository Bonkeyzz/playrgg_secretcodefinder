#!/usr/bin/env python

"""
PLAYR.GG Secret code parser v1.0
By: Bonkey (ft. StackOverflow)
Date: 2/6/2021
Python ver: 3.9.1
"""

from json import load
from termcolor import colored
import tweepy
import re
import time
import discord
import argparse
import sys
import colorama

# region ARGPARSER
if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--mode", "-m", help="t = twitter, d = discord, b = hybrid", type=str)
	argparser.add_argument("--prize", "-p", help="Finds all codes that have a specific prize.", type=str)
	argparser.add_argument("--id", "-i", help="Finds all codes that have a specific giveaway id.", type=str)
	try:
		args = argparser.parse_args()
	except:
		argparser.print_help()
		sys.exit(0)
# endregion

# region TWITTER

CODE_REGEX = r"([^\s]+) for \b(?<!\S)(?=.)(0|([1-9](\d*|\d{0,2}(,\d{3})*)))?(\.\d*[1-9])?(?!\S)"

# stackoverflow thx
# This is not fully working, but it will do.
def deEmojify(text):
	regrex_pattern = re.compile(pattern = "["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
						   "]+", flags = re.UNICODE)
	return regrex_pattern.sub(r'',text)

def tweepy_GetTweetsFromID(userID, tweetAmount):
		userTweets = TweepyAPI.user_timeline(screen_name=userID,count=tweetAmount,include_rts=False,tweet_mode='extended',include_entities=True)
		return userTweets


def ParseSecretCodeAlertTweets(tweets_arr):
	SecrCodeTweets = []
	for tweet in tweets_arr:
			tweet_content: str = deEmojify(tweet.full_text).replace("&amp;", "&")
			tweet_content_emoj: str = tweet.full_text.replace("&amp;", "&")
			if "SECRET CODE ALERT" in tweet_content:
				SecrCodeMatch = re.findall(CODE_REGEX, tweet_content, re.MULTILINE)
				PrizeName = deEmojify(re.findall(r'🎁.+', tweet_content_emoj,
									 re.MULTILINE)[0]).lstrip().replace(" (See Details)", "")
				EntryURL = tweet.entities['urls'][0]['expanded_url']
				if SecrCodeMatch:
					SecretCode = SecrCodeMatch[0][0]
					NumOfEntries = SecrCodeMatch[0][1]
					if args.prize is None and args.id is None:
							SecrCodeTweets.append(f'Code: {SecretCode}, Prize: \'{PrizeName}\', Entries: {NumOfEntries}, URL: {EntryURL}')				
					elif args.prize is not None and args.prize in PrizeName:
							SecrCodeTweets.append(f'Code: {SecretCode}, Entries: {NumOfEntries}, URL: {EntryURL}')
					elif args.id is not None and args.id in EntryURL:
							SecrCodeTweets.append(f'Code: {SecretCode}, Entries: {NumOfEntries}')
				else:  # Automatic secret code entry URLS
					if args.prize is None and args.id is None:
						SecrCodeTweets.append(f'[AE] Prize: \'{PrizeName}\', URL: {EntryURL}')
					elif args.prize in PrizeName or args.id in EntryURL:
  						SecrCodeTweets.append(f'[AE] URL: {EntryURL}')
	return SecrCodeTweets
# endregion

# region DISCORD

from discord.ext import commands
SelfBot = commands.Bot(command_prefix='', self_bot=True, fetch_offline_members=False)


async def getChannelMsgs(channelId):
	SecretCodeChannel:discord.TextChannel = SelfBot.get_channel(channelId)
	ChannelMsgs = await SecretCodeChannel.history(limit=200).flatten()
	return ChannelMsgs
	
PrizeRegex = r"🎁 Grand Prize((.*\n){2})"
CodeAndEntryNumRegex = r"Use code ([^\s]+) for \b(?<!\S)(?=.)(0|([1-9](\d*|\d{0,2}(,\d{3})*)))?(\.\d*[1-9])?(?!\S)"
URLRegex = r"Link to enter: (https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"


async def parseSecretCodeMsgs(channelMsg_array):
	retList = []
	for msg in channelMsg_array:
		msgContent: str = msg.content
		msgContent = msgContent.replace("**", "").replace("  ", " ")
		Prize = re.findall(PrizeRegex, msgContent, re.MULTILINE)[0][1].replace("\n", "")
		SecCodeAndEntryRegex = re.findall(CodeAndEntryNumRegex, msgContent, re.MULTILINE)[0]
		SecretCode = SecCodeAndEntryRegex[0]
		NumOfEntries = SecCodeAndEntryRegex[1]
		EntryURL = re.findall(URLRegex, msgContent, re.MULTILINE)[0]
		if args.prize is None and args.id is None:
			retList.append(f'Code: {SecretCode}, Prize: \'{Prize}\', Entries: {NumOfEntries}, URL: {EntryURL}')
		elif args.prize is not None and args.prize in Prize:
			retList.append(f'Code: {SecretCode}, Entries: {NumOfEntries}, URL: {EntryURL}')
		elif args.id is not None and args.id in EntryURL:
			retList.append(f'Code: {SecretCode}, Entries: {NumOfEntries}')	
	return retList
		

@SelfBot.event
async def on_ready():
	if args.mode != "b":
    		print(colored(f'Bot is on ( ͡° ͜ʖ ͡°)\nLogged in as: {SelfBot.user}', 'green'))
	channelMsgs = await getChannelMsgs(679381560104845332) # You must be in the Playr.gg discord server for this to work!!!
	codeList = await parseSecretCodeMsgs(channelMsgs)
	if not codeList:
			print(colored('[*] [D] No codes found! Try again later.', 'red'))
	for code in codeList:
			if args.mode != "b":
				print(colored(f'[{codeList.index(code)}] {code}', 'yellow'))
			else:
				print(colored(f'[D] [{codeList.index(code)}] {code}', 'yellow'))	
	print(colored("[!] [D] Done! logging out of discord...", 'cyan'))
	await SelfBot.close()
	time.sleep(1)

# endregion
colorama.init()
if __name__ == "__main__":
	with open('keys.json') as f:
		privKeys = load(f)
	
	if args.mode == "t":
		print(colored("[!] Mode: Twitter", 'magenta'))
		privTwitterKeys = privKeys['twitterapi']
		API_KEY = privTwitterKeys['API_KEY']
		API_SECRET = privTwitterKeys['API_SECRET']
		ACCESS_TOKEN = privTwitterKeys['ACCESS_TOKEN']
		ACCESS_TOKEN_SECRET = privTwitterKeys['ACCESS_TOKEN_SECRET']

		TweepyAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
		TweepyAuth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		TweepyAPI = tweepy.API(TweepyAuth)
		tweets = tweepy_GetTweetsFromID("PLAYRgg", 200)
		processed_tweets = ParseSecretCodeAlertTweets(tweets)
		if not processed_tweets:
				print(colored('[*] No tweets found! Try again later.', 'red'))
		for tweet in processed_tweets:
				print(colored(f'[{processed_tweets.index(tweet)}] {tweet}', 'yellow'))
		print(colored("[!] Done! Exitting...", 'cyan'))
	elif args.mode == "d":
		print(colored("[!] Mode: Discord", 'magenta'))
		DISCORD_API_TOKEN = privKeys['DISCORD_API_TOKEN']
		print(colored("[!] Initializing discord selfbot...", 'cyan'))
		SelfBot.run(DISCORD_API_TOKEN, bot=False)
	elif args.mode == "b":
		privTwitterKeys = privKeys['twitterapi']
		API_KEY = privTwitterKeys['API_KEY']
		API_SECRET = privTwitterKeys['API_SECRET']
		ACCESS_TOKEN = privTwitterKeys['ACCESS_TOKEN']
		ACCESS_TOKEN_SECRET = privTwitterKeys['ACCESS_TOKEN_SECRET']

		TweepyAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
		TweepyAuth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		TweepyAPI = tweepy.API(TweepyAuth)
		tweets = tweepy_GetTweetsFromID("PLAYRgg", 200)
		processed_tweets = ParseSecretCodeAlertTweets(tweets)
		if not processed_tweets:
				print(colored('[*] [T] No tweets found! Try again later.', 'red'))
		for tweet in processed_tweets:
				print(colored(f'[T] [{processed_tweets.index(tweet)}] {tweet}', 'yellow'))	
		DISCORD_API_TOKEN = privKeys['DISCORD_API_TOKEN']
		SelfBot.run(DISCORD_API_TOKEN, bot=False)
	else:
		argparser.print_help()
