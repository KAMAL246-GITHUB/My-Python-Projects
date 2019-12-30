import win32com.client
import pythoncom
import re
import collections
import paramiko
import Credential as c # The credentials to the Linux machine / DB etc are stored in Credential.py file and is imported here 

from IPython.display import display, HTML

class color:
   '''
   This class is to assign python accepted colors into class variables so that they can be used anywhere throughout the program with ease. 
   '''
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Handler_Class(object):
    def OnNewMailEx(self, receivedItemsIDs):
        '''
        This function monitors the emails and looks for the specific subject lines. 
        Upon recieving a specific mail, it connect to a specified Linux server and executes a shell script to perfrom the required action.
        Once done, it sends a mail to the users.
        '''
        # RecrivedItemIDs is a collection of mail IDs separated by a "," : sometimes more than 1 mail is received at the same moment.
        for ID in receivedItemsIDs.split(","):
            mail = outlook.Session.GetItemFromID(ID)
            subject = mail.Subject
            
            try:
#               command = re.search(r"%(.*?)%", subject).group(1) ## Needed in those case where you want to find subject line of specific patterns using regex.
                if str(subject).strip() == 'Test Mail - What is the Production batch Status Today?': ## The subject line of the email which needs to be actioned upon. A set of the subject lines can also be mapped to a their respective scripts in a dictionary and be used here.
                    ssh = paramiko.SSHClient() ## Create SSH object
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(c.MY_HOST, username=c.MY_USERNAME, password=c.MY_PASS, port=c.MY_PORT) ## Establish connection - all the values are defined in Credential.py which was imported in the beginning of the script
                    stdin, stdout, stderr = ssh.exec_command('bash -c "source .my_profile; /home/kamal/shell_scripts/first.sh"') ## Run the profile by creating the bash shell and then execute the shell script in the remote linux server and unpack the values returned into 3 variables
                    lines = stdout.readlines()
                    errors = stderr.readlines()
                    body = ''.join(lines) ## This removes the extra gaps between lines
                    body = "\n".join(list(collections.OrderedDict.fromkeys(body.split("\n")))) ## This command removes all the duplicate lines from the file
                    reply = mail.ReplyAll() ## Created a reply object
                    reply.Body = body ## Assign value to the 'Body' attribute of reply object
                    reply.Send() ## Send reply to all the senders
                    print (color.GREEN + color.BOLD + "Reply sent to the above email" + color.END)
            except:
                pass
outlook = win32com.client.DispatchWithEvents("Outlook.Application", Handler_Class)

# Trigger the infinit loop trhough PumpMessages method that waits for events.
pythoncom.PumpMessages()
