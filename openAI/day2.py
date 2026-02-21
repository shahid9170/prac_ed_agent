from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
import resend
import os
from openai.types.responses import ResponseTextDeltaEvent
import asyncio


load_dotenv(override=True)

@function_tool
def send_email(subject: str, html_body: str) -> str:
    """Send out an email with the given subject and HTML body to all sales prospects using Resend"""
    
    from_email = "onboarding@resend.dev"
    to_email = "shahid739815@gmail.com"
    
    resend.api_key = os.environ.get("RESEND_API_KEY")
    
    print(f"Sending email...")
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"API Key present: {bool(resend.api_key)}")
    
    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_body
        }
        
        email = resend.Emails.send(params)
        print(f"Response: {email}")
        
        if email.get("id"):
            return f"Email sent successfully with ID: {email['id']}"
        else:
            return f"Email failed to send: {email}"
    except Exception as e:
        print(f"Error: {e}")
        return f"Email failed to send due to error: {str(e)}"
    
    
    
instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."


sales_agent1= Agent(
    name="profesional slaes agent",
    instructions=instructions1,
    model="gpt-4o-mini"
)

sales_agent2 = Agent(
    name="Engaging sales agent",
    instructions=instructions2,
    model="gpt-4o-mini"
)

sales_agent3 = Agent(
    name="busy sales agent",
    instructions=instructions3,
    model="gpt-4o-mini"
)

descriptions = "write a cold sales email"

tool1= sales_agent1.as_tool(tool_name="sales_agent1", tool_description=descriptions)
tool2= sales_agent2.as_tool(tool_name="sales_agent2", tool_description= descriptions)
tool3= sales_agent3.as_tool(tool_name="sales_agent3", tool_description=descriptions)


tools= [tool1,tool2,tool3, send_email]

instructions = """
You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
 
3. Use the send_email tool to send the best email (and only the best email) to the user.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must send ONE email using the send_email tool — never more than one.
"""

slaes_manager= Agent(name="sales_manger", instructions=instructions,tools=tools, model="gpt-4o-mini")
message = "Send a cold sales email addressed to 'Dear CEO'"
async def main():
    result= await Runner.run(slaes_manager,message)
    
asyncio.run(main())