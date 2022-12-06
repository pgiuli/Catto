# Catto
Automated pop-up cats!

In order for the script to run correctly create a **.env** file in the root folder with the following:
(yes, you can use other subreddits with image submissions.)
```
subreddit = 'cats'
base64 = 'True'

client_id = ''
client_secret = ''

pic_hotkey = 'right shift'
stop_hotkey = 'control + right shift'
```
client_id, client_secret must be base64 encoded if ```base64 = 'True'```.

## Todo:

    - Rewrite in order to use tempfile instead of creating a 'data' folder, thus reducing clutter
    - Create setup routine
    - Store credentials in AppData folder
    - Customization menu
    - Add 'run on startup' setting
    - Add 'How to create reddit application' in README