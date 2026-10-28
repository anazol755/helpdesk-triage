import anthropic
import sys #comand line access

#Claude Intructions
SYSTEM_PROMPT = """
You are a help desk triage assistant for a university IT department.
You will receive one IT support ticket. Read it and respond with
a category, a priority, and first troubleshooting steps.

Categories (choose exactly one):
- Network
- Hardware
- Software
- Account/Access
- Printing
- Other

Priority levels (choose exactly one):
- Critical: an entire service is down, OR a shared resource (lab,
  printer, classroom system) is not working for more than one user
- High: one user is completely blocked from working
- Medium: a problem that slows work, but a workaround exists
- Low: a minor issue, question, or request

If the ticket is too vague to categorize confidently, choose the most
likely category, and in Needs info, write the one question you would
ask the user to confirm it. Otherwise write "None".

Troubleshooting steps:
- Give 3 to 5 steps a Tier 1 technician could do first
- Order them from quickest and least disruptive to most involved

Respond in exactly this format:
Category: <category>
Priority: <priority>
Needs info: <question or None>
Steps:
1. <step>
2. <step>
3. <step>
"""

if len(sys.argv) < 2:
    print("Usage: python triage.py <ticket_file>")
    sys.exit(1)

ticket_path = sys.argv[1]
 
#Read the ticket and close the file when the block ends
with open(ticket_path) as f:
    ticket =f.read()

#read the API key from the ANTHROPIC_API_KEY environment so the key never appears in code.
client=anthropic.Anthropic()

#send instructions and ticket to claude
message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1500, #cap reply length
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": ticket}],
)

for block in message.content:
    if block.type == "text":
        print(block.text)

