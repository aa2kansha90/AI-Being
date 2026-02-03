from http.server import BaseHTTPRequestHandler
import json
import time
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            user_input = request_data.get('user_input', '')
            session_id = request_data.get('session_id', 'default')
            
            # Generate trace ID
            trace_id = f"trace_{abs(hash(user_input + session_id + str(time.time())))}"
            
            # Safety validation
            content_lower = user_input.lower()
            
            if any(word in content_lower for word in ['kill myself', 'suicide']):
                response_text = "I'm concerned about you. Please reach out to crisis support at 988."
                safety_decision = "escalate"
            elif any(word in content_lower for word in ['hack', 'illegal']):
                response_text = "I can't help with that request."
                safety_decision = "block"
            elif 'weather' in content_lower:
                response_text = "Today's weather is sunny with a high of 75°F."
                safety_decision = "allow"
            elif 'help' in content_lower:
                response_text = "I'm here to help! What would you like assistance with?"
                safety_decision = "allow"
            else:
                response_text = "Hello! How can I assist you today?"
                safety_decision = "allow"
            
            response = {
                "response": response_text,
                "status": "success",
                "trace_id": trace_id,
                "safety_decision": safety_decision,
                "timestamp": datetime.now().isoformat() + "Z"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())