import yagmail
import os
from dotenv import load_dotenv
import click
from handler import add_recipients_to_file, scrape_website

load_dotenv()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="create and send the email immediately",
)
@click.option(
    "-r",
    "--recipients",
    multiple=True,
    default=["list"],
    help="add additional recipients",
)
def create_email(recipients, force):
    # Scrape website here
    scrape_website()
    click.echo(",".join(recipients))
    click.echo("Created email message @ email.txt")


@cli.command()
def send_email():
    yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PW"))
    with open("email.txt", "r") as file:
        file_contents = file.read()
    contents = (
        "This is an automated email. The script is a little wonky so there might be some mistakes. \n"
        + file_contents
    )
    emails = []
    with open("recipients.txt", "r") as file:
        for line in file:
            emails.append(line.strip())
    yag.send(emails, "Events in Durham This Week", contents)
    click.echo("Sent email")


@cli.command()
@click.option(
    "-r",
    "--recipients",
    multiple=True,
    default=["list"],
    help="add additional recipients",
)
def add_recipients(recipients):
    print(list(recipients))
    add_recipients_to_file(list(recipients))


if __name__ == "__main__":
    cli()


"""
some commands:
- create-email:
    - options:
        - -f : sends an email as well
        - --add ["option1", "option2", etc] : adds those emails to the list of recipients
- send-email:
    - options:
        - --add ["option1", "option2", etc] : adds those emails to the list of recipients
- add-recipients ["option1", "option2", "option3"]
- remove-recipients ["option1", "option2", "option3"]
"""
