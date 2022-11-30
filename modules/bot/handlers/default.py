from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from config import isToxic
from ..functions.functions import clear_MD

from ...logger import log_msg, logger
from ..keyboards.default import add_delete_button


@log_msg
async def start(message: types.Message, state: FSMContext):
    text = "Start message"
    await message.reply(text, reply_markup=add_delete_button())
    await state.finish()


async def help(message: types.Message):
    text = "Help message"
    await message.reply(text, reply_markup=add_delete_button())


async def is_toxic(message: types.Message):
    is_toxic = isToxic.is_toxic(message.reply_to_message.text)

    if is_toxic:
        text = "*YES*"
    else:
        text = "nope"

    await message.reply_to_message.reply(text)


async def get_toxicity_probab(message: types.Message):
    toxicity = isToxic.toxicity_probab_of(message.reply_to_message.text)
    
    text = f"Toxicity probability: *{clear_MD(round(toxicity, 2)*100)}%*"
    await message.reply_to_message.reply(text)


async def delete_msg(message: types.Message):
    try:
        await message.delete()
    except:
        ...


def register_handlers_default(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(help, commands="help", state="*")

    dp.register_message_handler(
        is_toxic, 
        lambda msg: msg.reply_to_message,
        commands="is_toxic",
        state="*"
    )
    dp.register_message_handler(
        delete_msg, 
        commands="is_toxic",
        state="*"
    )

    dp.register_message_handler(
        get_toxicity_probab, 
        lambda msg: msg.reply_to_message,
        commands="get_toxicity_probab",
        state="*"
    )
    dp.register_message_handler(
        delete_msg, 
        commands="get_toxicity_probab",
        state="*"
    )

