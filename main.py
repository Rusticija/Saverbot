import os
import config
from datetime import datetime
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters 

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {update.message.from_user.first_name}! Send a photo with caption!")


#Utility func, that helps identify the user
def get_user(unique_id):
    if os.path.exists(f'Users/{unique_id}.txt'):
        with open(f'Users/{unique_id}.txt','r') as f:
            return f.read()
    else:
        return False


#funnc that allows the admin to add new users
def add_user(update, context):
    if update.message.from_user.id == 'SOME_ADMIN_TELEGRAM_ID':     #change it before running
        unique_id = update.message.text.split()[1]
        name = update.message.text.split()[2]
        with open(f'Users/{unique_id}.txt',"w") as f:
            f.write(name)
        context.bot.send_message(chat_id=update.effective_chat.id, text= f'User with name: {name} and UniqueID: {unique_id} is created!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= 'You are not allowed to use this command, contact your administrator!')

#Func that allows to upload images
def upload_images(update, context):
    if get_user(update.message.from_user.id):
        
        photo_obj = update.message.photo[-1]
        
        photo_file = photo_obj.get_file()
        user_name = get_user(update.message.from_user.id)
        date = datetime.now()
        job_number = update.message.caption

        
        dir_path = f'Images/{date.strftime("%m.%Y")}/{user_name}/{job_number}'
        file_path = f'Image_from_{date.strftime("%H.%M.%S_%m.%d.%y")}_job_number.{job_number}.jpg'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, file_path)
        photo_file.download(file_path)
        
        context.bot.send_message(chat_id=update.effective_chat.id, text="Uploaded!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No user found!\nContact your system administrator for further information.")
        context.bot.send_message(chat_id=update.effective_chat.id, text= f'Also provide your Unique ID: {update.message.from_user.id}')


def main():
    
    updater = Updater(token=config.TOKEN, use_context=True)

   
    dispatcher = updater.dispatcher

    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    add_user_handler = CommandHandler('adduser', add_user)
    dispatcher.add_handler(add_user_handler)
   
    
    file_handler = MessageHandler(Filters.photo and Filters.caption, upload_images)
    dispatcher.add_handler(file_handler)

    
    updater.start_polling()

    
    updater.idle()

if __name__ == '__main__':
    main()
