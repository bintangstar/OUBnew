""" command: .compress """
#

from telethon import events
import asyncio
import zipfile
from pySmartDL import SmartDL
from userbot.events import register
import time
import os
from userbot import TEMP_DOWNLOAD_DIRECTORY ,bot
from userbot import CMD_HELP
# from uniborg.util import admin_cmd, humanbytes, progress, time_formatter
from userbot.util import admin_cmd, humanbytes, progress, time_formatter

#  @borg.on(admin_cmd("compress"))
@register(outgoing=True, pattern=r"^.compress(?: |$)(.*)")
async def _(event):
    #Prevent Channel Bug to use update
    if event.is_channel and not event.is_group:
        await event.edit("`compress Commad isn't permitted on channels`")
        return
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a file to compress it.")
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = downloaded_file_name
            await event.edit(downloaded_file_name)
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zipfile.ZipFile(directory_name + '.zip', 'w', zipfile.ZIP_DEFLATED).write(directory_name)
    await bot.send_file(
        event.chat_id,
        directory_name + ".zip",
        caption="`File zipped!`",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
    )
    await event.edit("DONE!!!")
    await asyncio.sleep(7)
    await event.delete()


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


CMD_HELP.update({
        "compress":
        ".compress [optional: <reply to file >]\
            \nUsage: make files to zip."
})
