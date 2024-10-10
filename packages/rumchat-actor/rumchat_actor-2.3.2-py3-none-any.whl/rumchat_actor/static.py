#!/usr/bin/env python3
"""Static variables

Absolute variable definitions not uinque to scripts.
S.D.G.
"""

from cocorum.localvars import RUMBLE_BASE_URL

class Driver:
    """For the Selenium WebDriver"""

    #How long to wait maximum for a condition to be true in the browser
    wait_timeout = 13

    #How long it takes for the Rumble Premium banner to pop up
    premium_banner_delay = 4

    #How often to refresh while waiting for a webpage condition to be met
    page_refresh_rate = 10

    #default path to a Browsermob Proxy executable
    browsermob_exe = 'browsermob-proxy'

class Message:
    "For chat messages"

    #Maximum chat message length
    max_len = 200

    #Message split across multiple lines must not be longer than this
    max_multi_len = 1000

    #Prefix to all actor messages
    bot_prefix = "🤖: "

    #How long to wait between sending messages
    send_cooldown = 3

    #How commands always start
    command_prefix = "!"

    #Effective max length of a message
    effective_max_len = max_len - len(bot_prefix)

class URI:
    """Uniform Resource Identifiers"""

    rumble_base = RUMBLE_BASE_URL

    #Popout chat url. Format with stream_id_b10
    chat_popout = RUMBLE_BASE_URL + "/chat/popup/{stream_id_b10}"

    #Rumble user URL. Format with username
    user_page = RUMBLE_BASE_URL + "/user/{username}"

    #Rumble channel URL. Format with channel_name
    channel_page = RUMBLE_BASE_URL + "/c/{channel_name}"

    #Rumble control service
    service = RUMBLE_BASE_URL + "/service.php"

    #URL of upload page at Rumble
    upload_page = RUMBLE_BASE_URL + "/upload.php"

class Moderation:
    """For moderation and related tasks"""

    #Levels of mute to discipline a user with, keyed to their HTML menu button class names
    mute_levels = {
        "5" : "cmi js-btn-mute-current-5",
        "stream" : "cmi js-btn-mute-current",
        "forever" : "cmi js-btn-mute-for-account",
        }

    #Badges of staff chatters
    staff_badges = ["admin", "moderator"]

class Clip:
    """For clipping"""

    #The filename extension i.e. video container to use for saved clips
    save_extension = "mp4"

    class Download:
        """For downloading clips"""

        #Valid resolutions of a livestream and the bitrates they use / should be saved with
        stream_qualities = {"360p" : "1.2M", "720p" : "2.8M", "1080p" : "4.5M"}

        #The default save quality for clips from a local recording
        default_save_bitrate = stream_qualities["1080p"]

        #How many times to test a TS chunk download to get its average download time
        speed_test_iter = 5

        #TS chunks must be able to download this many times faster than their duration
        #to be usable in a cache. Cannot be less than 1
        speed_factor_req = 2

    class Upload:
        """For uploading clips"""

        #Default primary and secondary category of clips
        category_1 = "Entertainment"
        category_2 = None

    class Record:
        """For locally recorded clips"""

        #Formats that the OBS recording can be in if recording-trimmed clips are to work
        #Must be moviepy loadable even if copied while being recorded to
        #In the format for Tkinter file picking
        input_options = (
            ("Fragmented or hybrid video", " ".join("*." + container for container in ("mp4", "mov"))),
            ("MPEG-TS stream video", "*.ts"),
            ("All files", "*.*"),
        )

        #Filename of the temporary copy of an OBS recording, used for ClipRecordingCommand
        temp_copy_fn = ".temp_recording_copy"

class AutoModerator:
    """For automatic moderation"""

    #LLM system message to moderate messages with
    llm_sys_prompt = "Analyze the following chat messages for appropriate-ness. Respond with either a 0 or a 1: If a message is appropriate for PG-13 SFW and not spam, or you are not sure, respond with a 1. If it is not appropriate for PG-13 or is NSFW or is spam, respond with a 0. You can only respond with these two values. Do not respond with commentary."

    #OLLaMa model to use for auto-modetation
    llm_model = "llama3.1"

class Thank:
    """For saying thank-you in chat"""

    #Default messages for the follow and subscribe thanker
    class DefaultMessages:
        """Default thank-you messages. Format with a Cocorum user object"""
        follower = "Thank you @{.username} for the follow!"
        subscriber = "Thank you @{.username} for the ${.amount_cents / 100 : .2f} subscription!"
