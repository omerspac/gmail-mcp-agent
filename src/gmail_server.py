import os
import json
from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# Initialize FastMCP server
mcp = FastMCP("Gmail MCP Server")

def get_gmail_service():
    """Get authenticated Gmail service"""
    token_json = os.getenv("GMAIL_TOKEN")
    if not token_json:
        raise ValueError("GMAIL_TOKEN environment variable not set")
    
    token_data = json.loads(token_json)
    
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes")
    )
    
    return build('gmail', 'v1', credentials=creds)

@mcp.tool()
def list_emails(max_results: int = 10, query: str = ""):
    """
    List emails from Gmail inbox
    
    Args:
        max_results: Maximum number of emails to return (default: 10)
        query: Gmail search query (e.g., 'is:unread', 'from:someone@example.com')
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', 
            maxResults=max_results,
            q=query
        ).execute()
        
        messages = results.get('messages', [])
        
        email_list = []
        for msg in messages:
            message = service.users().messages().get(
                userId='me', 
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = message.get('payload', {}).get('headers', [])
            email_info = {
                'id': msg['id'],
                'snippet': message.get('snippet', ''),
            }
            
            for header in headers:
                if header['name'] in ['From', 'Subject', 'Date']:
                    email_info[header['name'].lower()] = header['value']
            
            email_list.append(email_info)
        
        return {"emails": email_list, "count": len(email_list)}
    
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def read_email(email_id: str):
    """
    Read a specific email by ID
    
    Args:
        email_id: The ID of the email to read
    """
    try:
        service = get_gmail_service()
        message = service.users().messages().get(
            userId='me', 
            id=email_id,
            format='full'
        ).execute()
        
        headers = message.get('payload', {}).get('headers', [])
        email_data = {
            'id': email_id,
            'snippet': message.get('snippet', ''),
        }
        
        for header in headers:
            if header['name'] in ['From', 'To', 'Subject', 'Date']:
                email_data[header['name'].lower()] = header['value']
        
        # Get email body
        if 'parts' in message['payload']:
            parts = message['payload']['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    email_data['body'] = body
                    break
        else:
            body_data = message['payload']['body'].get('data', '')
            if body_data:
                body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                email_data['body'] = body
        
        return email_data
    
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def send_email(to: str, subject: str, body: str):
    """
    Send an email
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body text
    """
    try:
        service = get_gmail_service()
        
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        return {"success": True, "message_id": result['id']}
    
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_emails(query: str, max_results: int = 10):
    """
    Search emails using Gmail search syntax
    
    Args:
        query: Gmail search query (e.g., 'is:unread from:example@gmail.com')
        max_results: Maximum number of results (default: 10)
    """
    return list_emails(max_results=max_results, query=query)

if __name__ == "__main__":
    mcp.run()
