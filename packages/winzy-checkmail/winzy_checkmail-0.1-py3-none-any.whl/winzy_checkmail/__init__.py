import winzy
import win32com.client


def get_last_subjects(count=10, with_body=False, ith=None):
    """
    Extracts the subjects of the last 'count' emails in Outlook.

    Args:
    outlook_app (Optional[win32com.client.Dispatch]): Optionally provides a custom
        Outlook application object. Otherwise, uses the default instance.

    Returns:
    List[str]: List of last 'count' email subjects.
    """


    outlook_app = win32com.client.Dispatch("Outlook.Application")

    namespace = outlook_app.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)  # 6 refers to Inbox
    messages = inbox.Items
    subjects = []

    mcount = messages.Count
    if ith:
        start = mcount-ith
        amin = mcount-ith -1
    else:
        start = mcount-1
        amin = mcount - count - 1
    for i in range(start, amin, -1):
        message = messages.Item(i + 1)
        subject = getattr(message, "Subject", "<UNKNOWN>")
        if with_body:
            body = getattr(message, "Body", "NA")
            subject = subject + "\n" +body +"\n\n"
        subjects.append(subject)

    return subjects


def safe_join(subjects):
    try:
        return "\n".join(subjects)
    except UnicodeEncodeError:
        # Try to encode and decode each subject to handle unsupported characters
        encoded_subjects = [s.encode('utf-8').decode('utf-8') for s in subjects]
    return "\n".join(encoded_subjects)

class CheckEmail:
    name = "mail"
    @winzy.hookimpl
    def register_commands(self, subparser):
        hello_parser = subparser.add_parser("mail", description="Check outlook email from cli")
        hello_parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=10,
        help="Extracts the subjects of the last 'count' emails in Outlook",
        )

        hello_parser.add_argument(
            "-wb",
            "--with-body",
            action="store_true",
            help="If given returns body text as well."
        )
        
        hello_parser.add_argument(
            "-ith",
            "--ith",
            type=int,
            help="If given returns subject or/and body text of the last ith message"
        )
        

        hello_parser.set_defaults(func=self.checkmail)

    def checkmail(self, args):
        last_subjects = get_last_subjects(count=args.count, with_body=args.with_body, ith=args.ith)

        try:
            for i, subject in enumerate(last_subjects, 1):
                print(i, subject)
        except Exception as ex:
            pass
    
    def hello(self, args):
        # this routine will be called when "winzy "mail is called."
        print("Hello! This is an example ``winzy`` plugin.")

mail_plugin = CheckEmail()